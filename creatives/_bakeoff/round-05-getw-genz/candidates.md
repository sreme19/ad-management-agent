# Round 05 ledger — Gen Z women for /get/w

**Round status: TWO PLATES GENERATED AND SHIPPED, 2026-08-28.** Sree generated
slots 2 and 4 in Google Flow himself and handed them over with "use this" — so
these advanced on the app owner's direct approval, not on a rubric score. That is
the same authority that opened the round (his read of the live page overrode
round 02's 34.0), and it is recorded here rather than back-filled as a score.

Slots 1, 3, 5 and 6 are still unshot.

## Generated candidates

| id | slot | tier | credits | rubric score | disposition |
|---|---|---|---|---|---|
| `flow-group-three-1.jpeg` | group-three | **unrecorded** | **unrecorded** | not scored | **SHIPPED** as `hero.jpg` |
| `flow-moment-street-1.jpeg` | moment-street | **unrecorded** | **unrecorded** | not scored | **SHIPPED** as `moment.jpg` |

Neither carries a rubric score, and this session cannot supply one — it wrote the
prompts, and `creative-generation.md` §10 puts the judging in a second pass. What
follows is the mechanical QA (measurable defects), not the scoring pass. **The
scoring pass is still owed.**

Tier and credit cost went unrecorded — `tools.md` #16 exists precisely to stop
this and it happened anyway, because the plates were generated outside the repo's
own dispatch loop. Ask Sree what tier these ran on before assuming Veo 3.1
Quality.

## Mechanical QA

### Both plates
- **Arrived 1536×2752 (9:16), not 3:4.** The preflight in `prompts.md` was written
  after they were generated, so Flow's image default was still in force. Both are
  cut to 1080×1350 (4:5) in `_web/prep-get-w-images.py`.
- **Flow stamps the same four-point star Gemini does**, bottom-right. Both cropped
  out, never inpainted. Verified absent from the shipped files.
- **SynthID is not touched by any of this.** Cropping removes the *visible* mark,
  which is what `compliance.md` §6.2 asks for; the invisible provenance watermark
  stays in the pixels and should stay.
- **No typography, no garbled text, no visible signage** in either. Hands and
  faces are clean at full resolution — the failure mode that killed candidates in
  earlier rounds did not appear, including across three sets of hands.

### `flow-group-three-1` (hero)
- **A pasted flat cream rectangle covered the top-left**, x 0–1334 by y 0–666,
  with a hard edge (row-seam score 41.6 at y=666 against 3.5 for the next
  strongest row in the plate). The prompt's "clean cream wall across the top third
  for a headline" was read as *paste a cream fill*, not *render a wall*. Removed by
  the top crop, and no loss: the page sets its headline in HTML above the image, so
  the plate never needed in-frame type space. **Prompt fix recorded in `tools.md`
  #18** — don't ask a landing-page plate for type space at all.
- A repeating tyre-tread-like artefact in the pavement below y≈2650. Same crop.
- **Men are present in the background** — several blurred figures inside the café
  and a street crowd through the pillar gap on the right. The prompt said to
  exclude them and the plate did not. Unlike round 02's `gemini-moment-1`, **no
  crop removes these** — they are behind the subjects, centre-frame.
  Reading: not a `compliance.md` §6.1 hit. That rule bans *a real man's real,
  unenhanced photo*; these are generated, unfocused, unidentifiable and none is
  the object of the frame. Same reasoning round 02 applied to its two distant
  figures. **Recorded as a caveat, not cleared as a non-issue** — if the second
  pass disagrees, the fix is a regeneration, not an edit.
- Palette 4-ish, not 5: golden-hour terracotta rather than the flat cream ground.
  The wardrobe carries coral/rust/pink correctly (`tools.md` #8 held).
- POV (`creative-generation.md` §1): passes cleanly. All three are looking at each
  other, nobody addresses the lens, nobody is posed for the viewer.

### `flow-moment-street-1` (moment)
- Straight replacement for round 02's `gemini-moment-1` and better on every axis
  that plate was marked down for: no garbled signage, the two background figures
  are women, full figure in motion, pink against a cream street.
- Lowest shoe pixel y=2308; the star sits at y 2504–2656, so the bottom crop
  clears her feet by ~180px. The top crop comes off dead sky and tightens the
  frame.
- The round-02 alt text still describes it exactly, so the page's alt was left
  alone.

## What shipped, and where

`uv run python creatives/_web/prep-get-w-images.py` writes
`pocket-dating-coach/static/get-w/`:

| file | from | crop | out |
|---|---|---|---|
| `hero.jpg` | `flow-group-three-1` | rows 666–2586 | 1080×1350, 263 KB |
| `moment.jpg` | `flow-moment-street-1` | rows 570–2490 | 1080×1350, 196 KB |
| `shortlist.jpg` | round-02 `gemini-phones-1` | unchanged | 928×970, 62 KB |

Both plates are downscaled from 1536 to 1080 wide before encoding — new in this
round, and the reason is in the script: Flow returns 1536 and a 480 KB hero on the
paid destination is an LCP regression on the networks this page is bought for.

The page's `<img>` intrinsic dimensions were 896×1050 and 760×1152 from round 02
and are now wrong for 4:5 — updated in
`pocket-dating-coach/src/routes/get/[[audience=aud]]/+page.svelte`, along with the
hero's alt text, which still described one woman at home. **Uncommitted in both
repos.**
