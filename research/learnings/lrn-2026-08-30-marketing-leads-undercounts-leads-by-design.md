---
id: lrn-2026-08-30-marketing-leads-undercounts-leads-by-design
subject: tracking
claim: 'marketing_leads undercounts leads by design: its unique indexes on whatsapp_e164
  and lower(email) drop a returning submitter, recordAdLead reports that as duplicate:true,
  and the submission is recorded nowhere. A lead count read from that table alone
  disagrees with the network''s count and nothing surfaces the difference.'
source: source-code
confidence: high
sample_n: null
status: open
created: '2026-08-30'
last_confirmed: '2026-08-30'
review_after: '2026-10-29'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

marketing_leads undercounts leads by design: its unique indexes on whatsapp_e164 and lower(email) drop a returning submitter, recordAdLead reports that as duplicate:true, and the submission is recorded nowhere. A lead count read from that table alone disagrees with the network's count and nothing surfaces the difference.

## Evidence

- (2026-08-30) 2026-08-30: Snap Ads Manager reported 9 leads on RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608 while marketing_leads held 7 for the same window. Webhook ruled out as the cause: registration present on all 7 forms (ad-agent snap-leads forms), receiver alive and rejecting bad signatures (401 on a deliberately mis-signed POST), and Snap's own test delivery returned 200. Unique indexes confirmed in 20260815130000_add_marketing_leads_columns_and_constraints.sql (whatsapp_e164, lower(email)), and recordAdLead maps UNIQUE_VIOLATION to {ok:true,duplicate:true} with no logging. Third instance of the honest-zero shape after lrn-2026-08-28-channel2-rls-blocks-every-read and lrn-2026-08-29-snap-lead-webhook-only. Fixed by marketing_lead_submissions (20260830120000), one PII-free row per delivered submission.
