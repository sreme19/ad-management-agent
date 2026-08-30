# `_derived/` — one frame pulled from a Grok clip, not from Flow's stills

`tennis-jump-serve-contact.jpg` is the only asset in `asset-g-win.jpg`'s chain that
didn't come from `buildyourself-lead-w1830/_source/frames/`. None of the pristine
Flow stills show the serve *in the air* — Sree asked for that specific moment
(2026-08-30), and the only place it exists is inside the Grok animation of the
serve beat, which shows the full toss-arch-contact motion Flow's held-pose stills
don't.

**Source:** `buildyourself-lead-w1830/_source/clips/grok-video-90565286-8cef-4b0b-92fe-dedb49b674d1.mp4`,
frame at t=8.2s — the racquet-meets-ball contact point, arm at full extension.
Reproducible exactly:

```
ffmpeg -ss 8.2 -i buildyourself-lead-w1830/_source/clips/grok-video-90565286-8cef-4b0b-92fe-dedb49b674d1.mp4 \
  -frames:v 1 -vf "crop=693:1232:0:0,scale=1080:1920" tennis-jump-serve-contact.jpg
```

The `crop=693:1232:0:0` is the same watermark-crop the shipped video used throughout
(`creative-generation.md` §7) — Grok's wordmark sits at roughly x610-715, y1232-1265
of the clip's native 720x1280, and this crop removes it before the upscale to
1080x1920. Checked on this frame specifically: clean.

Carries the same wardrobe deviation already logged against the shipped video and
`asset-g-win.jpg`'s prior draft (jeans, not tennis kit) — inherited from the source
frame, not introduced here. Also carries visible motion blur on the ball, which is
real (a video frame, not a still generation) and was left in rather than
sharpened out.
