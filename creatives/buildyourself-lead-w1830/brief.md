# BUILD-YOURSELF-FIRST — Snap lead video

A 25.2s vertical film for the MOVE-ON lead funnel. Four women, four bad dating
experiences, one shared decision, then six beats of self-development, closing on
`riteangle` and an APPLY_NOW form.

## Argument

Act 1 (0:00–0:06) names the drain, one beat each: ghosting, catfishing,
inattention, low-effort dating. Act 2 (0:06–0:08.5) is the hinge — a four-panel
split screen where all four women lift their heads into the lens and the grade
flips from cool blue-grey to warm gold inside the shot. Act 3 (0:08.5–0:20.5) is
six "Pehle apni ___" beats. Act 4 closes on the wordmark.

The thesis is deliberately **not** "this happened because you weren't focused on
yourself" — that reads as blaming a woman for being catfished. Act 2 carries
"Khud ko bana sakti ho" instead: you can't change them, you can build yourself.
Same arc, no accusation.

## Production

Google Flow generated the frames; Grok Imagine animated them. Identity carried
because each Flow frame was fed into Grok as an image input, taking face, wardrobe
and set with it — **not** because Flow's character references held. They did not:
Flow's Characters ingredient list was empty, and Meera's saved character asset was
broken and unresolvable, which failed her frame repeatedly until the reference was
dropped and the frames themselves were attached instead
(`lrn-2026-08-30-grok-animates-what-flow-only-poses`).

The distinction matters. The compromise recorded against `moveon-swagger-video` —
the cast not carrying between scenes, so the ad read as "this happens / this is the
alternative" rather than "this happened to *her*" — was caused by relying on exactly
those character references (`lrn-2026-08-29-flow-character-reference-is-unreliable`).
What fixes it is the frame-into-Grok pipeline, not the character system. Here Meera
on the bedroom floor is the same Meera who lifts her head at the turn, verified
across Acts 1 and 2.

The frames, the Grok clips, the audio generations and the Flow project export are
kept in `_source/` — see the README there. None of it is reproducible, so it is the
only copy of this cast.

Audio is two Flow-generated instrumental beds. Prior practice permits this:
`moveon-lead-w1830/edit-script.md` says "Meta Sound Collection or Flow-generated
audio only; a commercial track is a licensing problem on a paid ad."

## Compliance checks done, not assumed

- **No visible AI-tool watermark** (`compliance.md` §2, sentence two). Grok's
  wordmark was cropped from every clip; Flow's sparkles appeared only on the
  office shot and were removed by cropping the top 220px.
- **No generated person narrates a first-person experience of Riteangle**
  (`compliance.md`). Nobody speaks at all — the cut is silent but for music, and
  every line is on-screen type.
- **Safe zones** (`creative-generation.md` §7). All type falls between y1235 and
  y1606 of 1920; the top 10% ends at 192 and the bottom 15% starts at 1632.
- **1080x1920, 9:16.**

## Known deviations, recorded

1. **25.2s against "six seconds is short"** (`creative-generation.md` §7). The
   emotional beat still lands at 0:02 as the rule requires, but this is a long
   asset by this account's standards and the format is unproven at this length.
2. **Wardrobe undercuts two Act 3 beats.** She serves at tennis in jeans, and
   presents to a boardroom in a vest top — both inherited from the source frames.
   Accepted for this cut; the rule is now written into the Grok prompt notes.
3. **Romanised Hinglish, not Devanagari.** Consistent with
   `lrn-2026-08-29-roman-script-is-an-audience-signal`.
4. **Type is set in Futura, not Gabarito** (`creative-style.md`). Gabarito is not
   installed locally. Cosmetic, and worth correcting before this becomes the
   house template.
