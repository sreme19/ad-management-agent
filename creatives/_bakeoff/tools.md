# Generation-surface registry

Driven through the user's logged-in Chrome. Login status verified per session —
do not assume. Add a tool the moment it's tried; retire one that keeps failing the
gates.

## Round-1 lineup — face-forward stills (image)
| Tool | Surface | Strength | Login | Notes |
|---|---|---|---|---|
| Grok Imagine | grok.com / x.com/i/grok | photographic, in-house default | ? | watermark lands in corner — croppable |
| ChatGPT (GPT-image) | chatgpt.com | strong prompt adherence, faces | likely (in dl-allowlist) | can garble; good at direction |
| Gemini (Imagen / "nano banana") | gemini.google.com | photoreal people, editing | ? | strong at realistic Indian faces |
| Midjourney | midjourney.com | highest craft ceiling | ? (seat needed) | user-driven if gated |
| Ideogram | ideogram.ai | text-in-image (we overlay text, so lower priority) | ? | keep for end-card tests |

## Round-3 lineup — AI video
Opened 2026-08-28. Sora is retired before use: discontinued, API sunsets 2026-09-24, and it
never launched in India.

| Tool | Surface | Strength | Login | Notes |
|---|---|---|---|---|
| Google Flow (Veo) | labs.google/flow | motion-graphics formats; holds character across panels | yes (used 2026-08-28) | **Rounds 3 and 4.** See the checklist below — the defaults will cost you a round if you don't set them |
| Seedance 1.5 Pro | fal.ai | vertical native, audio included | — | ~$0.58 / 5s at 1080x1920. fal is India-payable (prepaid USD). No Hindi lip-sync |
| Wan 2.2 Animate | fal.ai (Apache-2.0, self-hostable) | motion + expression transfer from a reference video | — | `Move` mode only — `Replace` is face-swap and fails compliance. $0.08/video-sec at 720p |
| Kling | klingai.com | Motion Control, Cinema Studio, first/last-frame | ? | pricing and 9:16 support unverified |
| Runway | runwayml.com | VFX applied to real footage, not full generation | ? | $0.60 / 5s |
| ~~Sora~~ | — | — | — | **Retired unused** — no India availability, API sunsets 2026-09-24 |


## Working with Google Flow — read before generating

Every line here cost a round or a QA concern to learn. Sources:
`note-2026-08-28-google-flow-step-by-step`, `note-2026-08-28-google-flow-nine-features`.

### Set these before you spend a credit

1. **Video aspect ratio.** Sliders icon beside the assistant prompt box → **Agent
   settings** → *Video generation default*. It ships on **16:9** and is a separate
   control from the image default, which already ships on 9:16. This one toggle is
   the entire reason round 3 came out landscape and did not advance
   (`lrn-2026-08-28-google-flow-s-output-aspect`).
2. **Model tier.** There are *two* places to set it: the Agent-settings dropdown,
   and a per-generation **model selector in the prompt box**. Both default to
   **Omni 1.1 Flash**, which is the weakest tier — round 4 scored craft 2.5/5 on
   it. **Veo 3.1 Quality** is available. Omni is also *feature*-limited: it cannot
   take an end frame at all (`lrn-2026-08-28-google-flow-s-model-tier`).
3. **Leave *Confirm before generating* on Always.** It is the credit guard, and it
   can be switched to Never.

### Then check, before approving

4. **9:16 is a canvas, not footage.** Round 4's "9:16" export was a 720×1280 file
   carrying a **720×702 near-square picture inset on white**. `ffprobe` reports
   1080-tall and passes; the picture is half that. Plain `cropdetect` misses it
   because Flow's surround is white, not black — negate first
   (`lrn-2026-08-28-setting-google-flow-s-video`). `typeset_video.py` detects this
   per file.
5. **Resolution.** Round 4 came out 720×1280 against the 1080×1920 every other
   asset here uses. Check it; don't assume.
6. **Backgrounds default Western.** Yellow cabs and US storefronts in round 3.
   Name the Indian city explicitly.

### Prompting, learned on round 4

7. **"Not sad" renders as sad.** A model cannot draw an absence. Round 4's first
   storyboard asked for "calm, not sad" and returned melancholy. Name the emotion
   you want, positively.
8. **Cream ground ≠ cream everything.** Asking for a cream palette *and* cream
   wardrobe *and* empty space returned beige-on-beige, a woman lost in a void.
   Cream is the **ground**; the subject carries the accent — coral or pink.
9. **"Leave empty space" is taken literally.** It made her a speck. Say she fills
   the frame *and* where the space sits.
10. **Give it a turn.** Three contemplative shots with no change between them read
    as a perfume ad. Each beat needs something to happen.
11. **Attitude is free; the lens is not.** Energy, swagger, colour, eye contact
    and streetwear are all permitted and all needed. The `rules/creative-generation.md`
    §1 line is the *camera*: no low angles, no pans along the body, no torso
    crops. Keeping that paragraph while loosening everything else is what turned
    round 4 from dull into shippable.

### Workflow you probably aren't using

12. **Fix one clip, don't regenerate all of it.** Select the clip, describe the
    change, generate. Round 4 shipped with **two pairs of sunglasses** because
    this was not known (`lrn-2026-08-28-a-defect-in-a-finished`).
13. **Storyboard Studio** — `tools` → *prompting* → Storyboard Studio. Approves
    script, then cast/locations/props, *then* pixels. Round 4 burned three
    freeform storyboards before landing.
14. **Text iteration is free.** Only generation costs credits. Be fussy at the
    storyboard stage.
15. **Save the character.** A named character is recalled with `@name` in any
    later prompt, and can be built from an uploaded photo. Round 4's woman was
    named Ananya.
16. **Record the cost and tier every time.** Round 3's went unlogged and cost most
    of a session to re-derive. Round 4: 10 credits, Omni 1.1 Flash.

### One compliance trap

17. **Avatars and photo-built characters.** Flow can build a character from an
    uploaded photo, and an **avatar** from a QR scan of a real face and voice.
    That is a real person's likeness, which `rules/compliance.md` §6.1 governs.
    Never build one from anyone who has not agreed to appear in paid advertising.
