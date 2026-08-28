---
id: lrn-2026-08-26-snap-and-beacon-disagree-on-lpv
subject: tracking
claim: Snap and our own beacon report materially different landing-page-view counts
  for the same ad squad, so the number the live women's test is judged on depends
  on which system you ask
source: live-data
confidence: high
sample_n: 96
status: supported
created: '2026-08-26'
last_confirmed: '2026-08-28'
review_after: '2026-12-26'
derived_from: note-2026-08-26-lpv-count-discrepancy
questions: []
recs:
- rec-2026-08-27-moveon-w2530-meta
promoted_to: null
---

## Claim

Snap and our own beacon report materially different landing-page-view counts for the same ad squad, so the number the live women's test is judged on depends on which system you ask

## Evidence

- (2026-08-26) Snap reported 59 landing page views at Rs 5.91 each for WOMEN_18-22_CASUAL_LPV on 2026-08-26; pocket-dating-coach counted 96 for the same ad squad. A ~39% gap on the metric this record declares as its success metric. The magnitude is one point-in-time reading and may move - reporting lag is one candidate cause among several - but the disagreement itself is two measured counts of the same thing, not an inference. See q-2026-08-26-why-the-lpv-counts-disagree.
- (2026-08-28) **supported** (from rec-2026-08-27-moveon-w2530-meta): The disagreement generalises to Meta, same direction: for ad 6984036525881 on 2026-08-28, Meta reported 111 link clicks and 87 landing_page_view while the beacon recorded 138 distinct get_w visits carrying the ad's utm_content. Platform LPV under beacon count on both networks — the platform metric is the stricter render-complete event, the beacon fires earlier. Cross-network now, so treat it as a property of the measurement pair, not a Snap quirk.
