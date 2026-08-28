---
id: note-2026-08-28-google-flow-nine-features
title: 'Nine Google Flow features: the model selector, per-clip edits, Storyboard
  Studio, and four motion-preserving transforms'
source: own-research
captured: '2026-08-28'
learnings:
- lrn-2026-08-28-google-flow-s-model-tier
- lrn-2026-08-28-a-defect-in-a-finished
---

# Nine Google Flow features, brought in by the app owner 2026-08-28

Second Kevin Stratvert Flow transcript of the day, after
`note-2026-08-28-google-flow-step-by-step`. Same provenance and same caveat: a
mechanics walkthrough, commercially clean, no affiliate link, demonstrating only
Google's own tool. Not evidence about performance.

Brought in immediately after round 4 shipped
(`rec-2026-08-28-moveon-swagger-w2530-snap`). Three of the nine features bear
directly on defects recorded in that round's QA, and one of them answers the
model-tier question that has been open since round 3.

## The one that matters most: the model selector is in the prompt box

> "in the prompt box, click on the model selector, and right over here, let's
> choose frames. To select both a start frame and an end frame, we need to switch
> the model to Veo. So right over here, let's go with Veo 3.1 - Quality. Omni
> doesn't currently support an end frame."

Two facts we did not have:

1. **Veo 3.1 Quality is selectable**, and the selector lives in the prompt box —
   not only in the Agent-settings dropdown found earlier today
   (`lrn-2026-08-28-google-flow-s-output-aspect`).
2. **Omni is feature-limited, not merely lower quality.** It does not support an
   end frame at all.

This is the fix for round 4's weakest dimension. `creatives/moveon-swagger-video/qa.md`
scored craft 2.5/5 and attributed it to the Omni 1.1 Flash tier rather than to the
prompt or the format. The tier was changeable the whole time and nobody looked.

## Per-clip editing without regenerating the whole thing

> "You don't have to regenerate an entire clip every time you want to make a
> change."

Select the clip, describe the change in the prompt field, generate. The demo
swapped a basketball for a cookie in an existing clip.

Directly applicable: round 4 shipped with **two pairs of sunglasses** on the same
woman in shot 3, recorded as a QA concern and left in because a fix appeared to
mean a full regeneration. It did not.

## Storyboard Studio — a more structured route than the one we used

Left nav -> `tools` -> the `prompting` category -> **Storyboard Studio**. Pick a
storyboard style, then either paste a script or describe the video. It returns a
title, scenes, dialogue and transitions, all editable as text.

Then an **assets** tab lists every character, location and prop the script needs,
initially empty. `autofill characters` generates them; each can be opened, its
name and visual description edited, and the image regenerated. Only then is the
visual storyboard generated, and because every panel references the same approved
assets, they stay consistent.

This is the control ladder from `note-2026-08-28-two-ai-video-tutorials` with a
dedicated interface: approve the script, then approve the cast and sets, then
generate. Round 4 went straight to a freeform prompt and burned three storyboards
on dull output before landing.

## Constrain-what-the-model-invents, four more instances

All four keep a real recording's motion and let the model alter only appearance —
the principle in `lrn-2026-08-28-constrain-what-the-model-invents`:

- **Transform an existing video.** Drag a video in, agree to a rights prompt,
  describe the change. Demo put a real dunk into a packed arena.
- **Style transfer by ingredient.** Add the source video AND a style reference
  image as two ingredients, then prompt. Demo turned a real walk into a Lego
  world and carried across pathway colour, a background car, the shirt colour and
  the subject's wave.
- **Extra camera angles from one take.** Add the video as an ingredient, turn on
  the agent, name the angles wanted. Demo produced two additional angles from one
  desk recording, and Flow confirmed the count and cost before generating.
- **Replace the subject, keep the motion.** Demo replaced the presenter with a
  robot while keeping his own walk.

The camera-angle one is the most useful here: it manufactures coverage from a
single generation, which is exactly what a 6-second three-beat ad needs.

## Characters, and the avatar

Characters confirms what `lrn-2026-08-28-google-flow-gates-spending-behind`
already records, and adds that a character can be created **from an uploaded
photo** as well as from a description. Named, given a voice, recalled with `@`.

**Avatar** is new and carries a rule. Profile picture -> `create avatar` ->
`get started` -> scan a QR code with a phone -> capture **your own face and your
own voice**. The avatar is then usable in images and videos, added via the prompt
box's plus icon.

That is a real person's likeness and voice, which is the territory
`rules/compliance.md` §6.1 governs. No Riteangle creative should carry an avatar
built from anyone who has not agreed to appear in paid advertising, and the tool
makes producing one a two-minute job — which is the risk, not the feature.

## What this does NOT say

- No prices. Veo 3.1 Quality's credit cost per generation is never stated, so
  whether it fits the Rs 9,400/month envelope at ad volume is unknown. Round 4 on
  Omni cost 10 credits; the Veo figure has to be read off the confirmation dialog
  before committing.
- No aspect-ratio discussion, again. Neither transcript mentions it. The
  vertical-canvas-not-vertical-footage behaviour recorded in
  `lrn-2026-08-28-setting-google-flow-s-video` is undocumented in both.
- Nothing about Indian faces, Hindi or Hinglish dialogue, or whether the
  character voices support Indian accents.
- The demos are cookies, basketball and Lego. Nothing about whether any of this
  holds up under a paid-social QA gate.
