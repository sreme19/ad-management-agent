---
id: lrn-2026-08-30-per-person-attribution-from-a-lead
subject: tracking
claim: 'Per-person attribution from a lead to a landing-page visit or an install is
  not wired on either network: marketing_leads.visit_id and marketing_apply_gate.ra_lead
  are null on every row, and those are the only keys that could join them.'
source: live-data
confidence: low
sample_n: 9
status: open
created: '2026-08-30'
last_confirmed: '2026-08-30'
review_after: '2026-12-28'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Per-person attribution from a lead to a landing-page visit or an install is not wired on either network: marketing_leads.visit_id and marketing_apply_gate.ra_lead are null on every row, and those are the only keys that could join them.

## Evidence

- (2026-08-30) 2026-08-30, live query over the 2-day window: 9 lead rows (7 Snap, 2 Meta), visit_id null on all 9; 8 marketing_apply_gate rows, ra_lead null on all 8. Snap is structural — its form end-page URL carries ad-squad UTMs plus ra_src=form and no per-lead id, because Snap documents no macro for one. Meta ships ra_lead={{lead_id}} on the form button URL and it is not resolving; Command-Cheatsheet.md says not to enable until an apply-gate row carries a real ra_lead, and the campaign was enabled anyway. Consequence: landing-page arrivals, store taps and installs can only be reported campaign-level.
