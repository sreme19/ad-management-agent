---
id: note-2026-08-28-google-flow-step-by-step
title: 'Google Flow step by step: the storyboard-first workflow, reusable characters,
  and credit confirmation'
source: own-research
captured: '2026-08-28'
learnings:
- lrn-2026-08-28-google-flow-gates-spending-behind
- lrn-2026-08-28-google-flow-s-output-aspect
- lrn-2026-08-28-setting-google-flow-s-video
---

# Google Flow, step by step — a third tutorial brought in by the app owner

Transcript brought in by Sree 2026-08-28, same day as
`note-2026-08-28-two-ai-video-tutorials`. Kevin Stratvert, "How to use Google Flow",
~9m20s. **Commercially clean** — unlike the two tutorials in that earlier note, this one
sells nothing, pushes no affiliate link, and demonstrates only Google's own tool. It is a
mechanics walkthrough, not evidence about performance.

Why it is worth storing rather than watching once: round 3 of the bake-off
(`creatives/_bakeoff/round-03-video-flow`) was generated in Flow exploratorily, and three
things about it went unrecorded — cost, model tier, and whether a character reference was
supplied (`q-2026-08-28-storyboard-grid-vertical`). This transcript names the interface
affordance that answers the third and shows where the second is confirmed. It converts
"we used Flow once" into a repeatable procedure.

## The workflow, in the order the tool imposes it

1. **flow.google**, sign in with a Google account. Homepage lists recent projects,
   Google's featured examples, and a **New Project** button.
2. **New Project** opens the workspace: media / characters / scenes / AI tools down the
   left, canvas in the middle, AI assistant on the right, prompt box along the bottom.
3. **Type the concept as a sentence.** Flow does *not* generate on the first prompt. It
   asks follow-up questions — in the demo: overall vibe, hero feature, visual style — and
   waits for a text answer.
4. **It returns a written storyboard**, not pixels: named characters with ages and
   descriptions, locations, props, wardrobe, set, then a frame-by-frame breakdown. Per
   frame: context, action, camera angle, lighting, dialogue. Six frames in the demo.
5. **Refine the storyboard in text.** Stated explicitly in the transcript: *"You're only
   editing text at this stage, and it won't consume any credits."*
6. **Ask for the visual storyboard.** Still-image previews of each frame. Feedback loop
   again — the demo asked for text on a product box and got it, and the tutorial's point
   was that catching it here is cheaper than catching it after generation.
7. **Ask it to generate the clips.** Flow shows a **confirmation with the credit cost
   before spending** — six scenes, 90 credits, an explicit Approve button.
8. **Assemble in `scenes`.** Right-click the canvas → New scene → `+` to add clips to a
   timeline. Clips can be trimmed on the way in, reordered by dragging, and trimmed again
   on the timeline.
9. **Per-clip regeneration from the timeline.** Select one clip, describe the change in
   the prompt box, and Flow updates only that clip.
10. **Export** — download icon top right for the assembled scene, or `all media` → hover a
    clip → three dots → download that clip alone, for editing elsewhere.

## The three features that bear on our open questions

**Characters — this is the answer to "referenced or invented".** The left-hand
`characters` panel creates a persistent, named, reusable character three ways: from a text
description, **from an uploaded reference image**, or by turning yourself into an avatar. A
character can be given a **name** and an assigned **voice**. Once saved, it is recalled in
any prompt by typing **`@`** and picking it from the list. The demo generated Silas from a
description, saved him, then prompted "@Silas eats a chocolate chip cookie at a busy train
station" and got the same face in a completely different setting.

This is Flow's own implementation of the "ingredients" rung from
`note-2026-08-28-two-ai-video-tutorials`, and it makes bake-off idea **C** — cast one
Indian woman once and reuse her — a built-in feature rather than a workaround.

**Credits are confirmed before spend, and text iteration is free.** Both matter for the
₹9,400/month generation envelope. The unrecorded cost of round 3 was an operator omission,
not a tool limitation: Flow states the price and waits. There is no excuse for the next
generation to go unrecorded.

**Video-to-video transformation.** An existing video can be uploaded (with an "I agree"
consent step) and altered by instruction — the demo turned a real backyard walk into a
snowy winter day. This is the same shape as Runway's VFX-on-real-footage and Kling's Motion
Control from the earlier note: the human performance is real, the model only reskins. It is
a fourth instance of **constrain what the model invents**
(`lrn-2026-08-28-constrain-what-the-model-invents`), and the first one available inside a
tool we already have a login for.

## What the transcript does NOT say

Recorded as unknown rather than inferred:

- **No model tier is ever named.** No mention of Veo 3.1, 3.1 Fast, or Omni Flash, and no
  visible tier selector in the described workflow. So this does not close the tier half of
  `q-2026-08-28-storyboard-grid-vertical`.
- **No aspect-ratio control is shown or mentioned anywhere.** The blocking defect on round 3
  was 1280x720 landscape, and nothing in this walkthrough demonstrates where vertical is
  selected. Whether 1080x1920 is a setting, a prompt clause, or unavailable remains open —
  and it is the single thing we most need to know before the next generation.
- **90 credits for six clips** is the only price quoted (15/clip, consistent with the Omni
  Flash figure in `tools.md`), with no statement of what a credit costs or what the free
  tier allows.
- Nothing about India availability, Hinglish or Hindi dialogue, Indian faces, or whether the
  assigned character voices support Indian accents.

## The compliance reading, which is not in the transcript

The character feature accepts an **uploaded reference image**. That is a capability with a
rule attached: `compliance.md` §6.1 forbids a real man's photograph in Riteangle creative,
and uploading one as a character reference would breach it at generation time rather than
at QA. Separately, §6.2 as scoped by the app owner on 2026-08-28 means a Flow character
with an assigned **voice** must not be scripted to narrate first-person experience of using
Riteangle — which is exactly what blocked `creatives/moveon-properly-w2530/script.md`. The
easier the tool makes a talking synthetic person, the more load those two rules carry.
