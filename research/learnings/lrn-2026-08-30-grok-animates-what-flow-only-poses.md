---
id: lrn-2026-08-30-grok-animates-what-flow-only-poses
subject: creative
claim: Google Flow holds character identity across frames but returns a held pose
  rather than the described action; Grok Imagine performs the action but has no character
  system, so the reliable pipeline is Flow for frames and Grok for animation
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

Google Flow holds character identity across frames but returns a held pose rather than the described action; Grok Imagine performs the action but has no character system, so the reliable pipeline is Flow for frames and Grok for animation

## Evidence

- (2026-08-30) Direct A/B on the Riteangle BUILD-YOURSELF-FIRST cut. The same Flow start frame of Meera on her bedroom floor was animated by both engines with the same instruction (lower the phone, shoulders drop). Flow's 4s clip held the phone in position for the entire duration with only a slight head dip; Grok's 6s clip visibly lowered the phone to her lap and broke her expression. Three further Act 1 beats repeated the pattern. Conversely Grok has no saved-character mechanism, so identity came entirely from the Flow frame fed in as the image input, and held perfectly including wardrobe and set. CONSEQUENCE FOR PLANNING: this directly addresses the cast-continuity failure in lrn-2026-08-29-flow-character-reference-is-unreliable. The woman drained in scene 1 WAS the woman lifting her head at the turn, verified across Acts 1 and 2, because identity was carried by the frame rather than by a character reference.
## Promoted (2026-08-30)

This claim is now normative, in `rules/creative-generation.md`. That file is what skills obey; this atom is only its origin.
