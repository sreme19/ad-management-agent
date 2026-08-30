---
id: lrn-2026-08-30-flow-extend-is-gated-on-veo-and-resolution
subject: creative
claim: Google Flow's Extend function is unavailable below 720p and unavailable for
  non-Veo models, so continuous audio or video longer than one generation requires
  choosing Veo at 720p or above at the first generation
source: own-research
confidence: medium
sample_n: null
status: promoted
created: '2026-08-30'
last_confirmed: '2026-08-30'
review_after: '2026-12-28'
derived_from: null
questions: []
recs: []
promoted_to: rules/creative-generation.md
---

## Claim

Google Flow's Extend function is unavailable below 720p and unavailable for non-Veo models, so continuous audio or video longer than one generation requires choosing Veo at 720p or above at the first generation

## Evidence

- (2026-08-30) Attempting to extend a 360p Omni 1.1 Flash music bed returned '360p videos cannot be extended'. Regenerating the same bed at 720p and retrying returned 'Only Veo-generated videos can be extended'. Flow's direct generation bar also offers 4s, 6s, 8s and 10s durations and 360p or 720p, which is easy to miss: the default 360p and 8s combination had been silently returning 4s clips. CONSEQUENCE FOR PLANNING: if a bed longer than 10s is needed, select Veo and at least 720p up front. Retrofitting is not possible and the clip must be regenerated.
## Promoted (2026-08-30)

This claim is now normative, in `rules/creative-generation.md`. That file is what skills obey; this atom is only its origin.
