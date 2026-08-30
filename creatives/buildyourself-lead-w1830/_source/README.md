# `_source/` — production inputs for `asset-a.mp4`

Everything Google Flow and Grok Imagine produced on the night of 2026-08-29 →
2026-08-30 that fed the shipped BUILD-YOURSELF-FIRST cut, kept because **none of it
is reproducible**. Flow and Grok are non-deterministic: re-running the same prompt
returns a different woman, a different room, a different grade. The frames here are
the only copies of this cast that will ever exist, and every one of them cost
credits. That is the reason this folder exists at all — `../../moveon-swagger-video/`
gitignores its `_build/` because ffmpeg can rebuild it, and that argument does not
apply to anything below.

Copied in from `~/Downloads` on 2026-08-30, timestamps preserved.

## What's here

| Folder | Count | Size | What it is |
|---|---|---|---|
| `frames/` | 41 | 6.5M | Flow-generated stills: 31 landscape 1376×768, 10 portrait 768×1376. The still frames that were fed into Grok as image inputs. |
| `clips/` | 19 | 63M | Grok Imagine animations, 720×1280, 6–10s. The moving footage the cut was assembled from. **Grok wordmark still present** at roughly x610-715, y1232-1265 — cropped `693:1232` during the edit, not here. |
| `flow-video/` | 4 | 3.2M | Flow's own video generations of the Act 1 beats, 720×1280 4s. Superseded by the Grok clips but kept as the alternate take. |
| `audio-beds/` | 9 | 3.5M | Flow music generations. Flow returns audio wrapped in a video container of an unrelated static scene (an empty room, sunlight on a wall) — **the picture is throwaway, the AAC track is the asset.** Two of these nine are in the finished cut. |
| `storyboard-flow-export.json` | 1 | 30M | The Flow project export ("Untitled Story", 2026-08-29 15:44) — `fullMarkdown` holds the full BUILD-YOURSELF-FIRST script, `assets` holds the Meera character record with its supporting images inlined, which is most of the 30M. |

Filenames are Flow's own auto-generated descriptions plus a `YYYYMMDDHHMM` stamp, left
unrenamed so they still match the Flow library. ` (1)` suffixes are second generations
of the same prompt, not duplicates.

## Reading the frames against the film

`brief.md` has the four-act structure. The frames map onto it by timestamp:

- **23:51–23:56 — Act 1**, the four bad experiences. `Woman_sitting_on_bedroom_floor`
  is Meera, the identity that had to carry into Act 2; `Woman_covering_mouth_at_cafe`,
  `Woman_looking_at_food`, `Woman_sitting_alone_at_table`,
  `Woman_looking_away_in_restaurant`, `Tired_woman_looking_at_phone` are the rest.
- **00:00–00:08 — Act 3**, the six "Pehle apni ___" beats: barbell/chalk (gym),
  tennis (serve, grip, toss), `Woman_presenting_in_meeting_room` and
  `Woman_smiling_in_modern_office` (work), balcony/meditation, cliff/coast.
- **`Four_women_looking_into_camera` / `Four_women_standing_in_space`** are the Act 2
  hinge — the four-panel lift into the lens.
- **01:30–01:42 — the beds.**

## Two cautions before reusing any of this

1. **The wardrobe faults are baked into the frames, not the edit.** `qa.md` deviation 3
   — tennis played in jeans, a boardroom presentation given in a vest top — came from
   these source frames. Reusing `Woman_serving_tennis_ball` or
   `Woman_presenting_in_meeting_room` carries the fault forward. Name the kit
   explicitly when regenerating instead.
2. **Nothing here has passed compliance on its own.** The `pass` in `qa.md` is against
   the finished 25.2s cut, where the watermarks were cropped and the audio replaced.
   These files still carry Grok's wordmark and their original generated audio, so no
   file in this folder is shippable as-is — `../README.md` and `rules/compliance.md`
   both apply on the way back out.

The ENERGY-DRAIN storyboard that was in the same Downloads folder belongs to a
different creative and went to `../moveon-lead-w1830/_source/` instead.
