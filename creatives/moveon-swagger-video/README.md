# MOVE-ON-PROPER — swagger cut (video, Flow round 4)

Bake-off round 4. First Riteangle video asset generated with the aspect ratio
set correctly (`lrn-2026-08-28-google-flow-s-output-aspect`) and the first with
its generation cost recorded: **10 credits, Omni 1.1 Flash**.

Register is deliberately different from `../moveon-properly-w2530` (the live
still, women 25-30, security register). This is the 18-22 swagger register -
loud coral and pink, streetwear, attitude - arrived at after three dull
storyboards. Persona is UNDECIDED: see the note in the session log. It is not
yet attached to an ad set or a recommendation.

## Pipeline

Flow generates picture only, per `rules/creative-generation.md` §2. Every glyph
is set by `typeset_video.py` in real Gabarito.

```bash
# 1. export from Flow, save it here as source.mp4
# 2.
uv run python creatives/moveon-swagger-video/typeset_video.py
# -> asset-a.mp4, 1080x1920, ~8s, audio at -14 LUFS
```

The script conforms to 1080x1920, overlays the timed captions on a soft cream
scrim, appends a 2s cream end card carrying the tagline and the two-tone
wordmark, and normalises audio. It warns if the source is not 9:16 rather than
silently centre-cropping the sides away.

To change a caption, edit `CAPTIONS` and re-run. That is the point of the split
- a new hook costs a string edit, not a regeneration.

## Not done yet

- QA pass against `../_bakeoff/rubric.md` (§10 gate) - needs the real export
- Persona / ad-set decision, and the budget that follows from it
- Comment-moderation stance, still unresolved across every breakup asset
