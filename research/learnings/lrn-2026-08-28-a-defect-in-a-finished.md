---
id: lrn-2026-08-28-a-defect-in-a-finished
subject: creative
claim: A defect in a finished Flow clip can be fixed by prompting that clip alone,
  and Storyboard Studio approves script, cast, locations and props as text before
  any pixel is generated
source: platform-doc
confidence: high
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2027-02-24'
derived_from: note-2026-08-28-google-flow-nine-features
questions: []
recs: []
promoted_to: null
---

## Claim

A defect in a finished Flow clip can be fixed by prompting that clip alone, and Storyboard Studio approves script, cast, locations and props as text before any pixel is generated

## Evidence

- (2026-08-28) (2026-08-28) Same Flow walkthrough. Two workflow affordances the round-4 session did not know about and was materially hurt by. (1) Per-clip editing: 'You don't have to regenerate an entire clip every time you want to make a change' - select the clip, describe the change in the prompt field, generate; the demo swapped a basketball for a cookie inside an existing clip. Round 4 shipped with two pairs of sunglasses on the same woman in shot 3, recorded as a QA concern in creatives/moveon-swagger-video/qa.md and left in on the assumption that fixing it meant regenerating the whole 10-credit clip. It did not. (2) Storyboard Studio, at tools > prompting > Storyboard Studio: pick a style, paste a script or describe the video, and it returns title, scenes, dialogue and transitions as editable text; then an assets tab enumerates every character, location and prop, autofills them as images that can each be renamed, re-described and regenerated individually; only then is the visual storyboard generated, and every panel references the same approved assets. This is the control ladder from note-2026-08-28-two-ai-video-tutorials given a dedicated interface. Round 4 went straight to a freeform prompt and burned three storyboards on dull output - beige-on-beige, an empty void, a woman lost in the frame - before landing.
