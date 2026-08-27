---
id: lrn-2026-08-27-meta-ads-carry-no-utms
subject: tracking
claim: Riteangle's live Meta ads carry no UTM parameters at all, so Meta spend has
  never been joinable to Meta traffic.
source: live-data
confidence: low
sample_n: 7
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

Riteangle's live Meta ads carry no UTM parameters at all, so Meta spend has never been joinable to Meta traffic.

## Evidence

- (2026-08-27) CONFIDENCE LABEL IS A GATE ARTIFACT, NOT AN EPISTEMIC ONE — see q-2026-08-27-min-sample-and-config-facts. This is a first-party census, not a sample: I read the fields directly in Ads Manager on 2026-08-27 for ad FB_STORY_GET_WAITING_V1_20260814 (id 6980035161881, 36 landing page views). Website URL is the bare 'https://www.riteangle.dating/get' with no query string; the Tracking section's URL parameters field is empty (placeholder only); Website events and App events both unchecked. All 7 ads in account 1561367575690055 are Off and none shows tracking configured. This is NOT the snap/snapchat mis-spelling failure — there is nothing to join on at all. Two consequences: q-2026-08-27-meta-utm-source-spelling cannot be settled by reading precedent off the account, because none exists, which makes utm_source a convention to AGREE with pocket-dating-coach rather than discover; and meta-push will be the first thing ever to put UTMs on a Meta ad here, so its output defines the convention rather than matching one.
