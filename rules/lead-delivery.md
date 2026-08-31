# Lead delivery (Snap lead-form → our data)

Source: `q-2026-08-30-why-has-no-snap-lead`. Every Snap lead submitted after the API webhook
integration was created (2026-08-29T15:09Z) was **lost** — zero reached `marketing_leads`. Read this
before setting up any Snap lead-objective ad, and before quoting a lead count from our DB.

## What was actually wrong — the API webhook does not deliver

The pipeline relied on a **custom webhook registered through Snap's Marketing API** (`/lead_gen`),
pointing at `https://www.riteangle.dating/api/marketing/snap-lead`. Two independent checks on
2026-08-30 showed it never fires:

- **Production logs** (`vercel logs --query "snap-lead"`): in a 24h window the receiver saw only 3
  connectivity `GET`s and 2 `POST`s — both Snap's own synthetic sample lead (identical `lead_id`).
  **Not one real submission ever arrived.** Signature/parse/storage/dedupe were never even exercised.
- **Ads Manager UI**: the live lead ad's form showed **"Connect form to CRM"** (i.e. *not* connected),
  and the only integrations Snap's UI offers are named partner CRMs — Google Sheets (Direct),
  LeadsBridge, Zapier, Datahash, Driftrock, Mailchimp, Zoho LeadChain, HubSpot. **There is no
  "custom webhook" option in the UI, and the API-created webhook is not shown or honoured there.**

Conclusion: Snap's lead delivery does not fire our API webhook. Do not spend more time debugging the
receiver — the fault is that Snap never calls it.

## The delivery path of record — Google Sheets direct integration

Snap lead-form delivery uses Snap's **native Google Sheets "Direct integration"**, connected in Ads
Manager **per form**. Snap pushes each submission as a row; a sync in `pocket-dating-coach` reads the
sheet and upserts into `marketing_leads` (that repo owns the DB write path — never write leads from
`ad-management-agent`; see `[[project_db_write_path]]`).

Why Sheets and not a partner CRM: it is the only **free, direct** (non-"External link") option, it is
drivable without a third-party account, the sheet is a **durable buffer** (a lead survives even if our
sync is down), and it keeps the Supabase write in our own code. None of the partner options write to
Supabase anyway, so we would still own a sync regardless — Sheets is the simplest reliable pipe out.

**First connection, done 2026-08-30 (MOVEON W18-30):**
- Ad account: `Riteangle - Primary` (`5c43c7ee-097b-41d5-b5b3-6917d56dacc9`)
- Google account bound to Snap: `chris@wardrobeofamonk.com`
- Form: `RA_LEAD_WOMEN_18-30_CASUAL_MOVEON-LEAD_SNAP` (id `1897accc-cd6b-4f60-9269-d76ec149842d`)
- Sheet: `Riteangle Snap Leads (MOVEON W18-30)` (id `11Aed7GGnrdIFVsz6cGNUmBMia3p1KxRJpZgHBEf7QMQ`)

Snap adds a `leadStatus` column to the sheet and expects it kept current with each lead's funnel stage
so it can optimise the lead ad — the sync can write funnel stage back into that column.

## The sync — implemented 2026-08-31 (Apps Script → endpoint)

The sheet→Supabase sync is a **Google Apps Script time-driven trigger (every 30 min) on each lead
sheet** that POSTs new rows to **`/api/marketing/snap-sheet-sync`** in `pocket-dating-coach`. The
endpoint upserts via `recordAdLead` (idempotent — dedupes on ad_lead_id / phone / email) and counts
every delivered row in `marketing_lead_submissions` so the daily readout can reconcile.

- Endpoint + tests: `src/routes/api/marketing/snap-sheet-sync/+server.ts` (in `pocket-dating-coach`).
- Apps Script (tracked copy) + setup: `scripts/apps-script/snap-sheet-sync.gs` and its `README.md`.
- Secrets: `SNAP_SHEET_SYNC_SECRET` (Vercel env) must equal the sheet's `SYNC_SECRET` script property.
- **Per form:** each new lead sheet needs its own copy of the `.gs` + script properties; the endpoint
  is shared. Run `installTrigger()` once, then `syncSnapLeads()` to backfill.

Until a sheet has the trigger installed, its leads sit in the sheet unsynced — pull them once by hand
via `import-snap-leads-backlog.ts`, then install the trigger so it never happens again.

**Inferred gender (2026-08-31).** The sync derives a submitter gender from the first name
(`src/lib/server/infer-gender.ts`, dictionary-only, null on unknown) and stores it in
`utm.inferred_gender` (+ `inferred_gender_source`) — **never** `audience`, which means the ad's TARGET
gender. It is a hint with a real error rate: coverage on the real backlog was ~28%, and the resolved
split ran ~91% male (110:11), consistent with the known lead-form skew. Existing rows were backfilled
via `scripts/backfill-inferred-gender.ts`. Do not treat a null as a signal, and never present the
split without its coverage.

## The mandatory step for every new Snap lead-objective ad

**Before a Snap lead-objective ad goes live, its form must be connected to a Riteangle leads Google
Sheet via the Ads Manager "Connect form to CRM → Google Sheets" flow.** This is a **manual UI step**:
`snap-push` cannot build lead-form ads at all (`rules/funnel.md` §2 rung 3 — `snap.py` has no
lead-form call), and the API webhook is unreliable, so there is no code path for this. Treat it like
the pre-launch tracking check: the ad is not "set up" until the form is connected and a test report
has landed in the sheet.

Steps: Ads Manager → the ad → Edit → **Lead form** → **Connect form to CRM** → **Google Sheets** →
sign in with the Riteangle Google account → create/select a dedicated, clearly-named sheet (one per
form; do not reuse an unrelated sheet — lead PII) → **Send test report** → confirm the row lands.

## Two things that are easy to get wrong

1. **The direct integration is not retroactive.** It only pushes leads submitted *after* connection.
   Any leads collected before it (e.g. the MOVEON ad's backlog visible in Ads Manager) must be pulled
   by hand: **Ads Manager → Download → Account leads** — on a 90-day retention clock.
2. **Never quote a lead count from `marketing_leads` alone.** Reconcile against the network's own
   number (Ads Manager result column, or the sheet) and show the delta —
   see `[[feedback_reconcile_before_presenting]]` and `[[project_lead_data_paths]]`.
