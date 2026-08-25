# QA gate — FOURTEEN-SUITORS, women 18–22

Run per `rules/creative-generation.md` §10. Checked as an image, not as copy.

## Variant B — `STORY_FOURTEEN-SUITORS_B_20260824` · over her shoulder

**Reviewed:** 2026-08-25 · first generation · **Verdict: `pass` — plate only, blocked on one post step**

| § | Check | Result |
|---|---|---|
| §1 | POV rule — who is the object of the frame? | **Pass.** Textbook. Camera sits behind her head, face never visible, hands and phone are the subject. Nobody is being looked at. |
| §4 | Negative-list signifiers | **Pass.** No formalwear, jewellery, luxury interior, marble, chandelier, vehicle, cash, branded goods, nobody serving. Ordinary shared-room setting exactly as briefed. |
| §4 | AI-tool watermark | **FAIL — "Grok" watermark, lower right.** See below. |
| §4 | Artefacts / hands / invented text | **Provisional pass.** Both hands read plausibly at this size; the sleeve treatment differs left vs right, which is probably drape. Re-check at full resolution before the type pass. |
| §2 | No typography baked in | **Pass.** Clean plate, as intended — this one is re-cuttable for another hook without regenerating. |
| §5 | Cream, not dark | **Strong pass.** Cream bedding, pale wall, warm daylight. This is the in-feed differentiator the palette rule exists to buy. |
| §7 | Type-safe space | **Pass.** Upper third is uncluttered wall — the hook line lands there. Bottom carries no load-bearing content. |
| §6 | Blank screen for the composite | **Pass, first attempt.** Bright, evenly lit, sharp, correctly proportioned. This was the clause flagged as most likely to fail; it held. |

### The blocking defect

The **Grok watermark** violates `creative-generation.md` §4 and `compliance.md` §6.2 directly — Sree's
Aug 21 note is literally "No grok label." As delivered this asset cannot ship.

It is **not** a `regenerate`: the plate itself is correct, and the watermark sits in a corner that gets
composited over during the type pass anyway. Remove it by crop or clone at that stage, or export
without it if the Grok tier allows. Re-checked on the finished asset, not here.

### Also fix before use

- **Letterboxing.** The render carries black borders. Crop to true full-bleed and confirm the result is
  still 1080×1920 — a 9:16 asset that isn't actually 9:16 gets re-cropped by the platform, usually
  through the type.
- **Watermark corner** overlaps Snap's CTA zone (§7), so the crop has to happen regardless.

### Deviation from brief, accepted

Briefed as "sitting on the edge of an unmade bed"; delivered as reclining on it. **Keep it.** Scrolling
in bed is the truer behaviour for this audience and this hook, and it costs nothing on any rule above.

## Variant A — `STORY_FOURTEEN-SUITORS_A_20260824` · the closed tab

**Reviewed:** 2026-08-25 · first generation · **Verdict: `pass` — plate only, same post step as B**

| § | Check | Result |
|---|---|---|
| §1 | POV rule | **Pass.** Her seat at the table, her hand, her lap. Nobody in frame to be looked at. |
| §4 | Negative-list signifiers | **Pass.** Nothing on the list. Plain wood, plain glass, bare wall. |
| §4 | AI-tool watermark | **FAIL — "Grok" watermark, lower right.** Same defect as B, same fix. |
| §4 | Artefacts / hands | **Verify at full resolution.** The hand is the focal element of the lower third and hands are the most common failure — count the fingers at 100% before the type pass. Plausible at this size, not confirmable. |
| §4 | Indian-context setting | **Soft flag.** The chai in a plain glass tumbler carries it; nothing else does. The room reads culturally neutral where B's paisley dupatta anchored it. Not a fail — worth a beat if the set is meant to read as one campaign. |
| §2 | No typography baked in | **Pass.** |
| §5 | Cream, not dark | **Strong pass.** Cream wall, warm wood, and a terracotta band at right that happens to sit on the brand's coral. |
| §7 | Type-safe space | **Best of the set.** The upper two-thirds is clean uninterrupted wall — more usable headline room than B. |

### Brief compliance

Phone genuinely face-down, chai present and unsteaming, hand withdrawing — all as briefed. One
deviation: a knee and lap are visible bottom-right, where the brief said hand only, no body. **Keep
it.** It reinforces that the viewer is the one sitting there, which is the POV rule's whole objective.

### The strategic read, separate from the gate

A is the quieter of the two. A face-down phone is a subtle signal at Story scale, and without the type
this frame could be any café ad — **A's hook depends entirely on the headline doing the work**, where B
communicates "person, phone, scrolling" before a word is read. That is not a QA failure and I'm not
overruling it: it is precisely the question the A/B exists to answer. Worth knowing which way you'd
expect it to go before the numbers arrive.

### Same two fixes as B

- Remove the Grok watermark (crop or clone during the type pass).
- Crop off the black letterboxing and confirm the export is a true 1080×1920.

## Variant C — `STORY_FOURTEEN-SUITORS_C_20260824` · no photograph

Not applicable — Figma build, no generation step.

## Finished-asset gate — `asset-a.jpg`

**Reviewed:** 2026-08-25 · **Verdict: `pass` — cleared to ship**

| Check | Result |
|---|---|
| AI-tool watermark | **Gone.** Removed by crop, not inpainting — see below. |
| Dimensions | **1080×1920 exactly.** Snap/Meta Story spec. |
| Type legible at in-feed size | **Pass, verified not assumed.** Rendered down to 216×384 (thumbnail scale) — headline fully readable, wordmark readable. |
| Wordmark | **Pass.** Lowercase `riteangle`, real Gabarito, correct spelling, ink + brand pink. Set programmatically, so casing cannot drift between variants. |
| Safe areas §7 | **Pass.** Headline y250–570, wordmark y632–690; both inside the 192–1632 band. Bottom 288px is table and hand — nothing load-bearing. |
| Banned vocabulary §6.4 | **Pass.** All 39 patterns from `pocket-dating-coach`'s `check-banned-strings.sh` run against the finished copy. Zero hits. |
| §1 POV rule, post-type | **Holds.** Type sits on empty wall; nothing added a subject to the frame. |

### Watermark: cropped, not painted out

First attempt was diffusion inpainting, which worked but left a visibly soft patch where it had
invented pixels. Replaced with a crop: the watermark sits in the bottom 4% of the frame, and both
plates carry dead space there (her lap in A, bedding in B). Cropping to 965×1716 and scaling to
1080×1920 removes it with **no invented pixels at all** — 43px of width and 76px of height lost,
none of it load-bearing.

**Prefer this order in future: crop first, inpaint only if the watermark overlaps real content.**

### Composition change during the type pass

The wordmark was first set bottom-left, per convention. It landed on the table and phone, where an
ink mark loses contrast — barely readable at in-feed size. Moved to sit directly under the headline
on clean cream, where it reads as a signature to the statement. **On a plate whose foot is busy, the
wordmark goes with the type block, not at the bottom edge.**

## Variant B — finished asset **blocked**

`preview-b.jpg` shows the type placement and it works — the headline sits cleanly on the wall above
the pillow. But B cannot ship: the phone screen is still blank, and per `creative-generation.md` §6
that screen receives the ranked-shortlist render, which is a Figma asset nobody has produced or
located yet.

**B is blocked on that render, not on anything in this repo.** `creative-style.md` says the interface
already exists — the next step is finding who holds it.

## What this pass taught the rules

§10 currently reads as though the gate runs once, on "the rendered asset." This run splits cleanly in
two: a **plate check** (POV, signifiers, palette, safe space, artefacts) that can happen the moment
Grok returns something, and a **finished-asset check** (watermark gone, type legible at Story size,
wordmark casing, crop dimensions) that can only happen after the type pass. Worth writing that split
into the rule — a watermark verdict on a plate is not the same claim as a verdict on a shippable ad.
