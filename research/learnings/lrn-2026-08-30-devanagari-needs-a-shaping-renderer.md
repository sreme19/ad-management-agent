---
id: lrn-2026-08-30-devanagari-needs-a-shaping-renderer
subject: creative
claim: Devanagari overlay type cannot be rendered by a text pipeline without complex-script
  shaping, which reinforces romanised Hinglish as the practical default for overlay
  type
source: own-research
confidence: low
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

Devanagari overlay type cannot be rendered by a text pipeline without complex-script shaping, which reinforces romanised Hinglish as the practical default for overlay type

## Evidence

- (2026-08-30) Rendering the Hinglish overlay line 'phir se ghost kar diya' in Devanagari through Pillow returned mis-ordered matras, with the i-matra placed after its consonant rather than before, because the available Pillow build reports raqm as false and so performs no shaping. ffmpeg drawtext has the same limitation. Latin script renders correctly in the same pipeline. CONSEQUENCE FOR PLANNING: this is a tooling constraint that happens to agree with lrn-2026-08-29-roman-script-is-an-audience-signal, which chose roman for audience reasons. If a Devanagari cut is ever tested, the type pass must be done in an editor with a shaping text engine, not in this pipeline.
## Promoted (2026-08-30)

This claim is now normative, in `rules/creative-generation.md`. That file is what skills obey; this atom is only its origin.
