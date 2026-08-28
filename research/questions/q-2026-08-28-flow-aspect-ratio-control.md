---
id: q-2026-08-28-flow-aspect-ratio-control
kind: creative
status: answered
asked: '2026-08-28'
raised_by: note-2026-08-28-google-flow-step-by-step
answered: '2026-08-28'
learning: lrn-2026-08-28-google-flow-s-output-aspect
---

## Question

Where in Google Flow is output aspect ratio set, and can it produce 1080x1920 vertical at all? Also still unnamed: which model tier Flow runs (Veo 3.1, 3.1 Fast, or Omni Flash) and whether that is selectable.

## Why it matters

The round-3 candidate scored 27.75/37.5 and was held back for exactly one reason - 1280x720 landscape, uncroppable to the 1080x1920 that Snap Story and Meta Reels need. The step-by-step walkthrough in note-2026-08-28-google-flow-step-by-step covers the entire workflow from new project to export and never shows or mentions an aspect-ratio control anywhere. So the one setting that decides whether any Flow output is shippable is undocumented in the only procedure we have. This must be answered in the interface before the next generation spends credits, not after.

## Answer (2026-08-28)

Answered 2026-08-28 from the Flow UI itself. Aspect ratio lives in Agent settings (sliders icon beside the assistant prompt box), as a persistent default rather than a prompt clause, and video and image have separate controls. Video was sitting on 16:9 - which is the whole explanation for round 3 arriving landscape. Video offers only 16:9 or 9:16. Tier is also named there: video Omni 1.1 Flash, image Nano Banana 2, both dropdowns.
