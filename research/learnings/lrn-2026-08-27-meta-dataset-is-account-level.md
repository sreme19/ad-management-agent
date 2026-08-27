---
id: lrn-2026-08-27-meta-dataset-is-account-level
subject: tracking
claim: Meta binds the conversion dataset at ad-account level, not per ad set, so a
  landing-page-views ad set needs no pixel_id and no promoted_object.
source: live-data
confidence: low
sample_n: 1
status: open
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-12-25'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Meta binds the conversion dataset at ad-account level, not per ad set, so a landing-page-views ad set needs no pixel_id and no promoted_object.

## Evidence

- (2026-08-27) CONFIDENCE LABEL IS A GATE ARTIFACT — see q-2026-08-27-min-sample-and-config-facts. Ad set FB_W_20-25_ID_Romantic (id 6980035162081) reads performance goal 'Maximise number of landing page views' with no dataset bound at ad-set level and Website events unchecked, and the ad under it reported 36 landing page views. Meta's own Tracking panel states: 'This ad account's selected conversion dataset will be tracked by default.' This CORRECTS meta.py's first cut, which mirrored snap.py's hard pixel requirement and asserted 'Meta has no fallback, no pixel means no signal at all' — the opposite of what the account shows. Snap genuinely needs its pixel per ad squad; Meta does not. The same ad set also confirms the account settles in INR ('Cost per result goal in Indian Rupee'), so MetaClient.require_inr passes rather than blocking.
