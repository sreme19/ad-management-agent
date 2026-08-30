---
id: lrn-2026-08-30-crop-beats-patch-for-generator-watermarks
subject: creative
claim: Generator watermarks should be removed by cropping and rescaling rather than
  by inpainting, because the patch artefact is more visually distracting than the
  mark it replaces
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

Generator watermarks should be removed by cropping and rescaling rather than by inpainting, because the patch artefact is more visually distracting than the mark it replaces

## Evidence

- (2026-08-30) Grok stamps a wordmark at the bottom right, x610 to x715 and y1232 to y1265 in a 720x1280 frame, and Flow stamps sparkles in the top corners. The ffmpeg delogo filter over the Grok mark on a textured cliffside left a visible horizontal smear that drew the eye more than the logo had; over the Flow sparkles on a smooth ceiling it left soft rectangular patches at both corners. Cropping was clean in both cases and cost nothing because delivery upscales 720x1280 to 1080x1920 regardless, and crop=693:1232 preserves exact 9:16. On the office shot, cropping 220px off the top also improved framing by removing dead ceiling. CONSEQUENCE FOR PLANNING: brief headroom and edge margin into frame prompts so a watermark crop is always available without losing subject.
## Promoted (2026-08-30)

This claim is now normative, in `rules/creative-generation.md`. That file is what skills obey; this atom is only its origin.
