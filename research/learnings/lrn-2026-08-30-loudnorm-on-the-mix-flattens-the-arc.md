---
id: lrn-2026-08-30-loudnorm-on-the-mix-flattens-the-arc
subject: creative
claim: Applying loudness normalisation to a finished mix destroys an intentional quiet-to-loud
  dynamic arc, so each bed should be set to its own target with only peak limiting
  across the sum
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

Applying loudness normalisation to a finished mix destroys an intentional quiet-to-loud dynamic arc, so each bed should be set to its own target with only peak limiting across the sum

## Evidence

- (2026-08-30) The Riteangle cut is designed so the drain is near-silent and the build comes forward. Normalising the assembled mix to -16 LUFS with loudnorm collapsed the difference between the two halves to 1.1 dB, -17.2 against -16.1, erasing the effect. Rebuilding with the two beds normalised to different targets, -28 and -14 LUFS, and only a limiter across the sum preserved an 11 dB lift, -27.8 in the drain against -16.6 in the build, while still landing at -15.9 LUFS integrated which is correct for Meta and Snap. CONSEQUENCE FOR PLANNING: loudness compliance and dynamic contrast are set at different stages. Never normalise last.
## Promoted (2026-08-30)

This claim is now normative, in `rules/creative-generation.md`. That file is what skills obey; this atom is only its origin.
