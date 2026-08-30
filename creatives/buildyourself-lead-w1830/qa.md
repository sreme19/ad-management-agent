# QA — `VID_BUILD-YOURSELF-FIRST_A_20260830`

**Verdict: `pass`**

**Pass type:** run by the app owner on 2026-08-30, independent of the session that
built the asset. `rules/creative-generation.md` §10 requires the check to come from
someone other than whoever wrote the prompts; the building session did not judge its
own output. The owner reviewed the finished 25.2s cut and returned `pass`.

**Asset:** `asset-a.mp4` — 1080x1920, 9:16, 25.17s, h264 + AAC stereo 48 kHz.

---

## Machine-verified facts supplied to the pass

These were measured by the building session and offered as inputs. They are
instrument readings, not a substitute for the owner's judgement.

- **No visible AI-tool watermark** (`compliance.md` §2, sentence two). Grok stamps a
  wordmark at roughly x610-715, y1232-1265 of each 720x1280 source; every clip was
  cropped `693:1232` before upscaling, which removes it. Google Flow's sparkle marks
  appeared on the office shot only, at x55-145 and x987-1060, y90-190; that segment
  was cropped 220px off the top. All other segments were checked and were clean.
  Patching with `delogo` was tried and rejected — it left visible soft rectangles.
- **No speech anywhere.** The cut carries no dialogue track. Every clip's source
  audio was discarded and replaced with two instrumental beds, so no generated person
  narrates a first-person experience of Riteangle (`compliance.md`).
- **Safe areas clear** (`creative-generation.md` §7). All type falls between y1235 and
  y1606 of 1920. The top 10% ends at y192 and the bottom 15% begins at y1632, so the
  tightest margin is 26px at the end card.
- **Wordmark** present, lowercase `riteangle`, correct spelling.
- **Music licensing.** Both beds are Flow-generated, which
  `moveon-lead-w1830/edit-script.md` permits for paid ads ("Meta Sound Collection or
  Flow-generated audio only").

## Deviations recorded, not hidden

1. **Type is set in Futura, not Gabarito** (`creative-style.md`; §10 checklist item 4).
   Gabarito is not installed on the build machine. The wordmark is lowercase and
   correctly spelled, but the face is wrong. Accepted for this cut; fix before this
   becomes the house template.
2. **25.2s against "six seconds is short"** (`creative-generation.md` §7). The
   emotional beat lands at 0:02 as the rule requires, but this is far longer than
   anything this account has run and the format is unproven at this length.
3. **Wardrobe undercuts two Act 3 beats** — tennis played in jeans, a boardroom
   presentation given in a vest top. Both inherited from the source frames rather
   than introduced by the animation. Accepted for this cut; the rule to name kit
   explicitly is now carried in the Grok prompt notes.
4. **Romanised Hinglish, not Devanagari**, consistent with
   `lrn-2026-08-29-roman-script-is-an-audience-signal`.
