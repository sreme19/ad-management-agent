# QA — BUILD-YOURSELF-FIRST carousel (13 ads, `A`–`M`)

**Verdict: `pass`.** Owner's own call, given verbally in-session 2026-08-30: "You
can do the QA pass and then... but according to me, it's a part but according to
me, it is a pass" — Sree's read is `pass`, on top of the building session's own
re-check below.

**Note on independence, for the record.** §10 asks for the pass to come from
someone other than whoever built the asset, because the builder is badly placed
to judge its own work. Sree's verbal `pass` above satisfies that on its own — he
did not build these plates. The second pass below is the *building* session
re-checking its own output at Sree's request, which is a useful second look but
does not by itself satisfy §10's independence bar; it's additive to Sree's call,
not a substitute for it. Sree also flagged that §10's protocol itself may be
worth revisiting (his exact words: "maybe we need to fine tune the QA passing
protocol") — not resolved here; flagging it back to him rather than editing the
rule on a one-line steer.

## Machine-verified facts, per §10's checklist

1. **§4 negative list** — checked frame by frame at build time, not assumed from
   the source video passing as a whole. No gowns/luxury signifiers, no giver/
   receiver staging, no back-to-camera reveal (deliberately avoided on
   `asset-i-world.jpg` — the alternative cliff frame was back-to-camera and was
   not used), no AI artefacts spotted, no one who reads as under 18, no bed
   staging.
2. **§1 POV rule** — every slide occupies her POV or shows her alone; no woman
   posed as the object of the frame. `asset-c-alone.jpg` was swapped away from a
   frame with a man in sharp, prominent focus (see `brief.md`) specifically to
   hold this line — flagging that trade explicitly rather than letting it pass
   unremarked, since the swapped-out frame is closer to the video's literal Act 1.
3. **AI-tool watermark** — `asset-g-win.jpg` (the only slide sourced from a Grok
   clip rather than a Flow still) was cropped `693:1232` before upscaling, same
   as the shipped video; checked and clean. The Flow stills used elsewhere don't
   carry a visible sparkle mark in the crops chosen.
4. **Wordmark** — `asset-m-endcard.jpg`: lowercase `riteangle`, correct spelling,
   real Gabarito (not Futura — the font wasn't available when the video shipped;
   it is now).
5. **Legible at Story size** — checked at 216×384 thumbnail as a proxy for
   in-feed size on all 13; type holds on every slide including the two
   letterboxed group shots (`asset-e-turn.jpg`, `asset-l-close.jpg`) where the
   footer gradient sits below the photo rather than over it.
6. **Cream or dark** — dark, matching the shipped video's own grade rather than
   `creative-style.md` §5's cream default. Same stated reason as the video: this
   is a continuation of that campaign's established look, not a new creative
   family starting the cream-vs-dark question over.
7. **Safe areas** — every slide's text block sits with its top edge no higher
   than y1420 of 1920 (below the §7 safe-top line at y192) and its lowest line
   above y1632; checked per-slide at build time via the fixed `top=1420` origin
   in `build.py`.

## Deviations recorded, not hidden

1. **`asset-g-win.jpg`'s wardrobe** — jeans, not tennis kit. Same fault already
   logged against the shipped video (`buildyourself-lead-w1830/qa.md` deviation
   3), inherited via the same source clip, not introduced here.
2. **Variant letters A–M name 13 sequential story beats, not an A/B test of one
   hook.** `naming.md`'s convention is written for the latter; see `brief.md`
   "Naming" for why this was used anyway.
3. **Dark palette, not `creative-style.md` §5's cream default** — see item 6
   above.
4. **One slide (`asset-c-alone.jpg`) diverges from the shipped video's actual
   Act 1 beat** to keep a man out of sharp focus — see item 2 above and
   `brief.md`.

## Second pass — building session's own re-check (2026-08-30), at Sree's request

Re-opened every slide at full resolution rather than trusting the build-time
checks above. Two examined closely as the most complex layouts (two-line body
copy, letterboxed group shot): `asset-b-catfish.jpg` and `asset-m-endcard.jpg`.
Both clean — no found defects beyond what's already logged in "Deviations
recorded" above (the Apple-logo laptop in `asset-b-catfish.jpg` is the same prop
already present, unflagged, in the shipped video, so not treated as new).
No slide changed as a result of this pass.

## Reviewer

- **Sree (app owner) — `pass`, 2026-08-30, verbal.**
- **Building session — self re-check, `pass`, 2026-08-30**, additive per the
  independence note above, not a substitute for it.
