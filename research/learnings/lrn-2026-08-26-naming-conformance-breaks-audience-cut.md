---
id: lrn-2026-08-26-naming-conformance-breaks-audience-cut
subject: tracking
claim: Conforming to naming.md and tracking.md removes the only signal audienceOf()
  classifies on, so every ad set created through snap-push inherits an unknown audience
source: source-code
confidence: high
sample_n: null
status: open
created: '2026-08-26'
last_confirmed: '2026-08-26'
review_after: '2026-10-25'
derived_from: note-2026-08-26-audience-classification-break
questions: []
recs: []
promoted_to: null
---

## Claim

Conforming to naming.md and tracking.md removes the only signal audienceOf() classifies on, so every ad set created through snap-push inherits an unknown audience

## Evidence

- (2026-08-26) pocket-dating-coach's audienceOf() infers audience by finding gender words in the campaign name and utm_* values, because the landing page has no identity signal and deliberately never will. Older non-conforming ad sets carried readable names in utm_campaign (sc_men_28_38_blr_casual) and classified cleanly. Under the rules, utm_term is a UUID and utm_campaign is RA_TRAFFIC_GET_IN_PAN_TOF_202608 - no gender word anywhere in the URL. The ID-based scheme is what made ad-level attribution work the same afternoon, so the scheme is not the thing to change.

## Reclassified (2026-08-26)

- Reason: Filed as own-research/medium only because no source-code kind existed. The claim is a statement about what pocket-dating-coach's audienceOf() does, verifiable by reading the function, not an inference about the world.
- `confidence`: 'medium' -> 'high'
- `source`: 'own-research' -> 'source-code'
