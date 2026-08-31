---
id: q-2026-08-30-why-has-no-snap-lead
kind: tracking
status: open
asked: '2026-08-30'
raised_by: lrn-2026-08-30-marketing-leads-undercounts-leads-by-design
answered: null
learning: null
---

## Question

Why has no Snap lead ever been stored via the live webhook, when the integration is registered, the receiver validates signatures, and Snap's test delivery returns 200?

## Why it matters

Leads are being lost right now. The integration was created 2026-08-29T15:09:53Z; every lead submitted after that (HashLy Mk 01:38Z and Suraj Hyalij 02:31Z on 08-30) is absent from marketing_leads, and the 7 that are present were bulk-imported hours after submission. Snap's test payload is discarded by isSnapTestPayload before it reaches recordAdLead, so the one green check we have never exercised the storage path. Until this is answered every lead costs Rs 47 and lands nowhere.

## New evidence (2026-08-30, later session)

Narrowed further from Vercel production logs on `www.riteangle.dating` (`vercel logs --query "snap-lead" --since 24h --expand`), cross-checked against `ad-agent snap-leads forms`:

- **Registration is not the problem.** All 7 lead forms, including `RA_LEAD_WOMEN_18-30_CASUAL_MOVEON-LEAD_SNAP` (the form behind the live `VID_MOVE-ON-PROPER_A_20260829` ad, `campaigns/moveon-lead-w1830-snap/record.md`), have a webhook integration pointed correctly at `https://www.riteangle.dating/api/marketing/snap-lead`.
- **The receiver is reachable and logging correctly.** The `a7ed73c9` deploy (live since 12:08 IST) added an unconditional log line on every inbound POST; cron jobs and other routes are logging normally on the same deployment.
- **In the trailing 24h, exactly 5 requests hit this endpoint: 3 `GET`s (Snap's `/test` connectivity probe, or a manual `ad-agent snap-leads test` call) and 2 `POST`s — both carrying the identical synthetic sample `lead_id` (`13cbb197-9274-401d-aa87-0482bad1a307`), i.e. the same test delivery re-fired twice, not two different real leads.**
- **Zero POSTs in that window contain a real lead** — no signature-mismatch, no missing-header, no parsing-error, no stored/duplicate/no_usable_contact log line. The receiver has never once been asked to process a real submission.
- Meanwhile Snap's own Ads Manager shows 10 delivered leads on that exact ad (₹447.47 spent, ₹44.75/lead) as of this check.

**Conclusion, tightened:** this is not a receiver bug (signature, parsing, storage, dedupe have all been ruled out at various points and none of them has ever even been exercised by a real payload). Snap is registered to call us and demonstrably *can* reach us — the synthetic test proves that — but is not forwarding real form submissions. The fault is on Snap's delivery path, not this repo's code, unless there is an account/campaign-level "enable lead sync" toggle in Ads Manager's UI that is separate from the API-level webhook registration and has not been checked.

**Next actions, not yet done:**
1. Check Snap Ads Manager's own UI for the lead form / integration for a delivery-health or error state the API doesn't surface.
2. Do not wait on this to protect against loss: pull today's leads by hand (Ads Manager → Download → Account leads) — 90-day clock, and nothing has landed automatically since the integration was created.
3. If the UI shows nothing wrong, this looks like a Snap support case — our side has no further diagnostic to run against a channel that isn't calling us.

## UI evidence (2026-08-30, browser check of Ads Manager)

Drove the live Ads Manager UI (Riteangle - Primary, Chris - Organisation admin) with Claude-in-Chrome. Path: Manage Ads → campaign `RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608` → ad set `WOMEN_18-30_CASUAL_MOVEON-LEAD` → Ads → edited (view-only, nothing saved) ad `VID_MOVE-ON-PROPER_A_20260829`.

- The ad's **Lead form** panel names the form `RA_LEAD_WOMEN_18-30_CASUAL_MOVEON-LEAD_SNAP`, **form ID `1897accc-cd6b-4f60-9269-d76ec149842d`**, and its CRM control is a button reading **"Connect form to CRM"** — i.e. the UI presents the form as **not connected to any CRM**, not "Connected" / "Manage connection".
- The ad-level result column showed this ad at **11 Leads / ₹488.97** (the sibling ad `VID_BUILD-YOURSELF-FIRST_A_20260830` at 0 leads / ₹38.80). So Snap counts 11 delivered leads on a form the UI shows as CRM-unconnected.
- Opening "Connect form to CRM" launches a **partner picker only**: Google Sheets (Direct integration), LeadsBridge, Zapier, Datahash, Driftrock, Intuit Mailchimp, Zoho LeadChain, HubSpot. **No "custom webhook" option exists in this UI, and none of the partners is marked connected.** (Closed without connecting anything — a CRM connection is a standing config change for Sree to approve.)

**What this adds:** our pipeline is an **API-registered custom webhook** (→ `https://www.riteangle.dating/api/marketing/snap-lead`), created via the Snap Marketing API `/lead_gen` endpoints. That webhook is **not visible, not manageable, and not shown as connected** anywhere in the Ads Manager UI, which only supports the named partner CRMs above. This is the UI-vs-API discrepancy hypothesised earlier, now confirmed: the form the buyer-facing UI drives has no CRM delivery binding it recognises, even though our API call reports a webhook integration registered on it.

**Caveat (do not overclaim):** absence from this partner picker is *not* proof the API webhook is dead — Snap may simply not render API-created webhooks in this UI. But paired with zero real deliveries in production logs, the most probable read is that Snap's lead delivery for this form is not actually firing our API webhook.

**Likely fix (Sree's call — none executed):**
- **A. Google Sheets direct integration** (Snap-native push) → then sync Sheet → Supabase. Lowest risk, uses Snap's own supported path.
- **B. Zapier** → Supabase.
- **C.** Keep the API webhook and open a Snap support case to learn why it isn't honoured / re-register it.
Sree's stated instinct is to "re-initiate the entire process"; A or B replaces the unrecognised API webhook with a delivery path Snap's UI actually drives.

## Fix applied (2026-08-30) — Google Sheets direct integration

Chose path A. Connected the MOVEON lead form to a Google Sheets direct integration via Ads Manager
(Connect form to CRM → Google Sheets), signed in as `chris@wardrobeofamonk.com`, and bound a dedicated
sheet `Riteangle Snap Leads (MOVEON W18-30)` (`11Aed7GGnrdIFVsz6cGNUmBMia3p1KxRJpZgHBEf7QMQ`). Snap
confirmed "Successfully connected" and the form now shows a green **Google Sheets** status. Triggered
**Send test report**.

Encoded as a standing rule so future lead ads get the same treatment: `rules/lead-delivery.md`, named
in `ad-setup-loop/SKILL.md` (new step 8b), plus memory `project_snap_lead_delivery`.

**Still open / to verify (not done in this session):**
1. The test-report row had not appeared in the sheet at time of writing (Snap's test can lag minutes,
   or only writes on the first real lead) — re-check the sheet and confirm a row lands.
2. Build the **sheet → `marketing_leads` sync** in `pocket-dating-coach` (that repo owns the DB write).
   Not started.
3. **Backlog: PULLED and RECONCILED 2026-08-30 — see correction below.**
4. Connect the remaining active lead forms the same way (only MOVEON is done).

## CORRECTION — the data loss was ~5 leads, not a large backlog (2026-08-30)

The "leads are being lost right now / every lead lands nowhere" framing at the top **overstated the
loss**, and this session's early note (7 rows in `marketing_leads`, newest 29 Aug) was an artifact of
`daily-ad-leads.ts`'s 1-day `submitted_at` filter — not the table's real contents.

Verified directly against the live DB: `marketing_leads` already held **380 rows** (259
`snap_lead_form` + 121 `meta_lead_form`), all **bulk-imported 2026-08-29 ~17:00**. The historical
backlog was already saved by hand back then; the webhook's silence only cost the leads submitted
*after* that import.

Pulled the fresh 90-day account-leads export (269 Snap rows → `~/Downloads/83d2fc63-…xlsx`) and
reconciled against the DB by `ad_lead_id`: **259 already present, 10 absent** — of which **5 were
person-duplicates** (already in the DB under a different lead-id, matched on email/phone) and **5
genuinely new** (the post-import gap, mostly 30 Aug MOVEON leads). Imported those **5** via
`pocket-dating-coach/scripts/import-snap-leads-backlog.ts --commit` (idempotent on `ad_lead_id`;
mirrors `recordAdLead`). **DB now 385 (264 snap.)** Gender inferred from first name where confident
(dictionary coverage only ~25% — empirical confirmation of the repo's no-name-inference caution),
stored in `utm.inferred_gender`, never `audience`.

**Net:** actual loss to date ≈ 5 leads, now recovered. The Sheets integration automates the manual
bulk-import that was already keeping the gap small. Ongoing sheet→DB sync still to build.
