---
id: lrn-2026-08-31-meta-lead-ingestion-both-paths-broken
subject: tracking
claim: Meta lead-form leads are being lost because BOTH ingestion paths fail — the
  real-time webhook rejects every delivery with an X-Hub-Signature-256 mismatch
  (wrong/other-app META_APP_SECRET), and the Graph-API backfill 502s because the
  system-user token cannot act as the Page. Ads Manager showed 26 leads for
  RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608 while marketing_leads held 2.
source: own-research
confidence: high
sample_n: 1
status: open
created: '2026-08-31'
last_confirmed: '2026-08-31'
review_after: '2026-11-29'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## What we saw

On 2026-08-31, Meta Ads Manager reported **26 Leads (Form)** for campaign
`RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608`; `marketing_leads` held **2** for it (Rosy +
the `chris@` test, both 29 Aug). ~24 real leads never reached the DB. Same silent-gap
shape as the Snap sheet, but a different root cause — and there are **two** faults, not one.

Diagnosed from Vercel production runtime logs (`vercel logs https://www.riteangle.dating --json`).

## Fault 1 — the real-time webhook rejects every lead (the live leak)

```
POST /api/marketing/meta-lead → 401  "[meta-lead] signature mismatch"
userAgent: Webhooks/1.0 (https://fb.me/webhooks)   hasSignature: true
```

Meta **is** delivering leads in real time. The endpoint verifies
`X-Hub-Signature-256 = HMAC-SHA256(rawBody, META_APP_SECRET)`
(`src/routes/api/marketing/meta-lead/+server.ts`, `signatureOk`). A persistent mismatch
means the **`META_APP_SECRET` in Vercel does not match the Meta app that owns the webhook
subscription** — wrong value, or the webhook was created under a different app than the
secret belongs to. Every delivery is 401'd and dropped. This has been leaking since ~29 Aug.

## Fault 2 — the Graph-API backfill 502s (the recovery path is also down)

A 15-min Vercel cron on `/api/marketing/meta-lead-backfill` was added 2026-08-31 (commit
`911e5090`, GET handler so Vercel Cron's auto-authed GET reaches it). The plumbing fires on
schedule, but:

```
GET /api/marketing/meta-lead-backfill → 502
```

`pageToken()` (`src/lib/server/meta-leads.ts`) reads `/{PAGE_ID}?fields=access_token` with the
system-user token and gets nothing back. Its own thrown message is the fix: *"the system-user
token cannot act as the Page… Assign the Page to the system user in Business Settings
(Users → System users → Assign assets, with Manage permission)."* Likely compounded by the
token missing `leads_retrieval` (flagged unverified in `rules/lead-delivery.md`).

## The plumbing is fine — the fault is Meta-side config + one secret

Nothing in our code is wrong. Both fixes are Meta credentials/config that only the app owner
can set:

1. **Correct `META_APP_SECRET`** — Meta App → Settings → Basic → App Secret. Update the Vercel
   env var (confirm it is the app the webhook is subscribed under), redeploy. → resumes
   **real-time** capture.
2. **Assign the Page to the system user** (Manage) + ensure the token carries `leads_retrieval`
   — Meta Business Settings → Users → System users → Assign assets. → makes the **backfill**
   work: recovers the ~24 already-missed (within Meta's 90-day retention) and gives an ongoing
   15-min backstop.

Fixing either starts closing the gap; fix both for live capture + automatic recovery.

## How to confirm the fix

After the change + redeploy, re-run the reconciliation:
`marketing_leads` count for the campaign should climb toward Meta's 26, and
`marketing_lead_submissions` (network=`meta_lead_form`) should show new `stored` rows. The
backfill is idempotent (dedupes on ad_lead_id / phone / email), so re-running is safe.

## Related

- `rules/lead-delivery.md` — Snap's parallel silent-gap and the reconcile-before-quoting rule.
- `lrn-2026-08-30-marketing-leads-undercounts-leads-by-design.md` — the dedupe that hides shortfalls.
- Snap's fix (2026-08-31): sheet → Apps Script 30-min trigger → `/api/marketing/snap-sheet-sync`.
