---
id: lrn-2026-08-28-google-flow-s-output-aspect
subject: creative
claim: Google Flow's output aspect ratio is a persistent Agent-settings default, not
  a prompt clause, and its video default ships on 16:9 independently of its image
  default
source: platform-doc
confidence: high
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2027-02-24'
derived_from: note-2026-08-28-google-flow-step-by-step
questions:
- q-2026-08-28-flow-aspect-ratio-control
recs: []
promoted_to: null
---

## Claim

Google Flow's output aspect ratio is a persistent Agent-settings default, not a prompt clause, and its video default ships on 16:9 independently of its image default

## Evidence

- (2026-08-28) (2026-08-28) Read directly off the Flow UI by the app owner - the platform's own settings screen, not an inference: sliders icon beside the assistant prompt box -> 'Agent settings'. Two independent controls. 'Image generation default' offers 16:9 / 4:3 / 1:1 / 3:4 / 9:16 and was already set to 9:16. 'Video generation default' offers only 16:9 or 9:16 and was sitting on 16:9. That toggle - not the prompt, not the storyboard-grid format - is the sole cause of the round-3 candidate arriving at 1280x720 landscape, which was the only reason it did not advance at 27.75/37.5. No amount of writing 'vertical 9:16 1080x1920' into a prompt would have fixed it. The same dialog names the tier: video runs 'Omni 1.1 Flash', image runs 'Nano Banana 2', both dropdown-selected, so round 3 was scored on Google's weakest video model. Also present: an x1-x4 generation-count multiplier per media type, and 'Confirm before generating' = Always, which means the approve-before-spend gate described in the tutorial is a setting that can be switched to Never, not a guarantee.
