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

**One open item — see the §8 independent pass below, which returned `escalate` on §6.2 (labelling AI imagery).** The §6.4 banned-vocabulary check is done and clean.

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

## §8 independent second pass — 2026-08-27, fresh session

Requested by the §6.4 check above ("a fresh session or different model should review the
finished asset against `rules/compliance.md` before handoff") and required by
`rules/compliance.md` §8. Done by reading the rendered `asset-c5-a.jpg` itself, not the
notes about it.

**Verdict: `escalate` — one item for the app owner. Everything else confirmed clean.**

| Rule | Independent finding |
|---|---|
| §1 money / provider | **Confirmed clean.** Cream domestic interior, window, plant, framed art, plain dusty-rose tee. No luxury signifier, no cash, no car, no formalwear, nobody being served. Nothing implies being kept or provided for. |
| §2 purchase language | **Confirmed clean.** Nothing implies a purchase, subscription or credit. |
| §3 rupee referral | **Confirmed clean.** Not present. |
| §4 "high-earning" | **Confirmed clean, and the flagged phrase holds.** The prior pass asked for explicit confirmation on "Verified, not vibes." It stays on the right side of the rule for a specific reason worth writing down: it names the *check* (identity verification) rather than the *attribute* (income). §4's approved phrasing is "identity-verified and established professionals", and "verified" is the sanctioned half of it. Had it read "vetted professionals" or leaned on "established", it would be closer to the line. |
| §5 ranking | **Confirmed clean.** No percentile, no score, no top-N claim. |
| §6.1 man's real photo | **Confirmed clean.** No man in frame. Three framed pictures on the walls; the right-hand one is abstract, the others are blurred beyond any identifiable face. |
| §6.3 18+ | **Confirmed clean.** Subject reads clearly late-20s. |
| §6.4 banned vocabulary | **Confirmed** — re-read the three pattern arrays against the burned-in type independently. 0 hits. |
| **§6.2 label AI imagery** | **ESCALATE — see below.** |

### §6.2 — the one item, and why it is a decision rather than an edit

`rules/compliance.md` §6.2 opens with **"Label AI imagery"** and adds that creative
showing a portrait "must not imply it's an untouched snapshot". The gate above marked
§6.2 `pass` on the grounds that the Gemini ✦ watermark was covered by the cream footer.

That reasoning satisfies one half of the rule and moves *away* from the other. Removing
a tool watermark is the opposite of labelling: the asset is now a fully AI-generated
portrait of a woman, carrying no indication that she is generated, and nothing in frame
signals it.

What sharpens it is the format. `script.md` describes her as "the *speaker* — her story,
her eyes, her decision", and the burned-in line is first person: "Move on toh karna hai —
par dhang se." A face plus a first-person account of a breakup reads as **testimony from
a real customer**. That is a stronger implicit claim than an AI illustration makes, and it
is the claim §6.2's second sentence is about.

This is not a copy tweak to make and move on — `SPEC.md`'s compliance non-negotiables say
a hit is "a decision for the app owner". Three ways it could go, all his call:

1. **Label it** — an on-asset "AI-generated" / "Illustrative" mark. Costs stop-scroll and
   partly undoes the point of the cream-UGC look.
2. **Change the framing** so it is not implied testimony — drop first person, or use the
   still as a statement rather than a quote. Keeps the plate, loses the Tinder-Move-On-Salon
   reference the idea was built on.
3. **Rule that §6.2 means only "no visible AI-tool watermark"** for paid social, and that
   labelling is an in-product obligation. Defensible, but it should be written into
   `rules/compliance.md` as an explicit scope, not left as an inference — otherwise the next
   asset re-litigates it.

Note also that this is independent of Meta's own synthetic-media rules, which have not been
checked here and are the platform's to enforce.

## Note on Grok text overlay (Sree raised it)
Grok can overlay text, and it's fine for a fast rough comp. But `creative-generation.md` §2 keeps type programmatic on purpose: a sampler cannot be trusted to hold the lowercase `rite` spelling and Gabarito casing that carry the brand pun, and garbled type on a paid asset is unshippable. So: Grok overlay = ok for throwaway comps; `typeset.py` = the shippable path.

## Provenance
- Plate: `../_bakeoff/round-01-moveon/candidates/gemini-3-beautiful.png` (c5, Gemini, bake-off round 2 winner)
- Type: `typeset.py` (Pillow + real Gabarito). Re-run to re-cut: `uv run python creatives/moveon-properly-w2530/typeset.py`
