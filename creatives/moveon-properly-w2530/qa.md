# QA gate — MOVE-ON-PROPER, women 25–30

Per `rules/creative-generation.md` §10. Plate = bake-off winner c5 (Gemini),
type set programmatically by `typeset.py`.

## Finished-asset gate — `asset-c5-a.jpg`
**Reviewed:** 2026-08-27 · **Verdict: `pass` — cleared to reference in propose**

| Check | Result |
|---|---|
| §1 POV — object or speaker? | **Pass.** She addresses the camera mid-sentence, chest-up, dusty-rose tee. Speaker, not object. Attractiveness raised per Sree without crossing into object-of-desire (no seductive angle, no body crop). |
| §4 negative-list signifiers | **Pass.** Ordinary Indian home — cream walls, window, plant, framed art. No luxury, cash, formalwear, nobody serving. |
| §6.1 real man's photo | **Pass.** No man in frame. Framed wall art is abstract/landscape, no identifiable male face. |
| §4/§6.2 AI watermark | **Pass.** Gemini ✦ watermark removed by the opaque cream footer (`scrim(solid_from=1700)`) — covered, not inpainted, no invented pixels. |
| §4 artefacts / hands / face | **Pass.** Face and visible arm read clean at Story size. |
| §2 wordmark | **Pass.** Lowercase `riteangle`, real Gabarito, correct spelling, ink `rite` + pink `angle`. Set programmatically so casing cannot drift. |
| §5 cream not dark | **Strong pass.** Cream ground throughout — the in-feed differentiator. |
| §7 safe areas | **Pass.** Hook y236–410 (below top-safe 192); tagline+wordmark y1466–1590 (above bottom-safe 1632). Foot below 1632 is cream footer, nothing load-bearing. |
| Type legible at Story size | **Pass.** Verified by reading the 1080×1920 asset; hook, tagline, wordmark all readable. |
| §6.4 banned vocabulary | **TODO before propose** — run copy ("Move on toh karna hai — par dhang se.", "Verified, not vibes.") through `pocket-dating-coach`'s check-banned-strings wordlist. |
| Dimensions | **Pass.** 1080×1920 exactly. |

**One open item:** the §6.4 banned-vocabulary check on the Hinglish + English copy. Everything else passes.

## Note on Grok text overlay (Sree raised it)
Grok can overlay text, and it's fine for a fast rough comp. But `creative-generation.md` §2 keeps type programmatic on purpose: a sampler cannot be trusted to hold the lowercase `rite` spelling and Gabarito casing that carry the brand pun, and garbled type on a paid asset is unshippable. So: Grok overlay = ok for throwaway comps; `typeset.py` = the shippable path.

## Provenance
- Plate: `../_bakeoff/round-01-moveon/candidates/gemini-3-beautiful.png` (c5, Gemini, bake-off round 2 winner)
- Type: `typeset.py` (Pillow + real Gabarito). Re-run to re-cut: `uv run python creatives/moveon-properly-w2530/typeset.py`
