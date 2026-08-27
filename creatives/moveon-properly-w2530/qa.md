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
| §6.4 banned vocabulary | **Pass.** 2026-08-27 — all 39 patterns from `pocket-dating-coach/scripts/check-banned-strings.sh` (31 phrase, 3 exact, 5 referral) applied to the on-asset copy AND the `script.md` spoken lines. Zero hits. See "Banned-vocabulary check" below. |
| Dimensions | **Pass.** 1080×1920 exactly. |

**No open items on this asset.** The §6.4 check is done (below); everything else passes.

## Banned-vocabulary check — 2026-08-27

The gate script scans *repo paths* in `pocket-dating-coach`, so it cannot be pointed
at ad copy. Per `rules/compliance.md` §6.4 ("or its wordlist, manually, until this
repo has a direct way to invoke it") the three pattern arrays were extracted verbatim
from the script and run against the copy: 31 `PATTERNS_PHRASE` (case-insensitive),
3 `PATTERNS_EXACT` (case-sensitive), 5 `PATTERNS_REFER`.

Strings checked — the finished asset's burned-in type, from `typeset.py`:
- "Move on toh karna hai —" / "par dhang se."
- "Verified, not vibes."
- `riteangle` wordmark

...and the video copy in `script.md`, so the check covers the testimonial cut too:
- "Breakup ke baad, sab bole — bas move on karo, start swiping again."
- "Par wahi swipe pile, wahi type ke log… nahi. Move on karna tha — par dhang se."
- "Yahan har koi verified hai. He's vetted before he ever reaches me — main scroll nahi karti."
- "He's vetted before he ever reaches you." (second-person variant)
- CTA `More`

**Result: 0 hits across all 39 patterns.**

### What the wordlist does not cover — read before propose
The gate is a *regression* gate: every pattern in it was live in the rejected build
1.0.5 (591). Passing it is not the same as passing `rules/compliance.md`. Judged
separately against that file:
- **#1 money / provider** — clean. No income, luxury, spending, or giver/receiver framing.
- **#4 "high-earning"** — clean, but note "verified" / "vetted" is doing quality-of-
  membership work here. That reads as identity verification (the sanctioned lane),
  not an earnings claim. Worth one line of confirmation at propose rather than an
  assumption, since it is the phrase closest to the rule.
- **#2 purchase language, #3 rupee referral, #5 rankings** — none present.
- **§8 independent second pass** — still outstanding, and deliberately not satisfied
  by this check: the same session that wrote the copy ran the wordlist. A fresh
  session or different model should review the finished asset against
  `rules/compliance.md` before handoff.

## Note on Grok text overlay (Sree raised it)
Grok can overlay text, and it's fine for a fast rough comp. But `creative-generation.md` §2 keeps type programmatic on purpose: a sampler cannot be trusted to hold the lowercase `rite` spelling and Gabarito casing that carry the brand pun, and garbled type on a paid asset is unshippable. So: Grok overlay = ok for throwaway comps; `typeset.py` = the shippable path.

## Provenance
- Plate: `../_bakeoff/round-01-moveon/candidates/gemini-3-beautiful.png` (c5, Gemini, bake-off round 2 winner)
- Type: `typeset.py` (Pillow + real Gabarito). Re-run to re-cut: `uv run python creatives/moveon-properly-w2530/typeset.py`
