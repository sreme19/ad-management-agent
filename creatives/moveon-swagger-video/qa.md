# QA — `asset-a.mp4`, MOVE-ON-PROPER swagger cut

Scored against `../_bakeoff/rubric.md`, per `rules/creative-generation.md` §10.

> ## ⚠️ THIS IS NOT AN INDEPENDENT PASS
>
> §10 and `.claude/skills/ad-setup-loop/SKILL.md` step 6 both require QA to be a
> second pass, and Sree's own note says prefer a fresh session over the same
> reasoning pass that produced the work. **This pass fails that test.** The same
> Claude session that wrote `typeset_video.py`, chose the captions, chose the card
> layout and directed the Flow prompt also scored it here, on the app owner's
> instruction to move ahead on 2026-08-28.
>
> Treat every score below as self-assessment. The two findings recorded under the
> gates were found by inspection and are real; what cannot be trusted is the
> absence of findings, because the reviewer shares the author's blind spots.
> A cold pass is still worth running before this scales beyond a ₹300/day test.

**Verdict: `pass`** — 28.25 / 37.5, with two recorded concerns.

## Asset

`asset-a.mp4`, 1080×1920, 8.03s, h264 + AAC, 2.4 MB, audio at −14.1 LUFS.
Built by `typeset_video.py` from `source.mp4` (Google Flow, Omni 1.1 Flash,
10 credits, 2026-08-28). Flow's native picture was 720×702 inset on white;
it is seated as a 1000×975 card on the cream ground with type above and below.

## Hard gates

| Gate | Result | Why |
|---|---|---|
| Real man's photo present | **pass** | No man appears at any point. |
| AI watermark / label, garbled text, glitched hands/faces | **pass, two concerns** | No tool watermark, no AI label. All type is ours, set in real Gabarito, so nothing is garbled. Faces are clean in all three shots — no blend artifacts of the kind round 3 carried at 2.5s. **Concern 1: she wears two pairs of sunglasses in shot 3** — one on her eyes and a second pushed up on her head, both fully rendered. An object-continuity error rather than malformed anatomy, so not a §4 fail, but it is a visible AI tell once noticed. **Concern 2: hands are soft.** Her left hand at ~0.8s is indistinct — motion blur compounded by the upscale, not extra or missing fingers. Neither is a fail; both are recorded so a later reviewer is not the first to see them. |
| Anyone could read under 18 | **pass** | Reads clearly mid-twenties. |
| Negative-list signifier | **pass** | Coral shirt, jeans, sneakers, residential street, painted wall. No gown, formalwear, jewellery display, luxury, cash, kneeling or serving. |
| Woman as OBJECT of the frame | **pass** | Straight-on at standing eye level throughout. No low angle, no pan along the body, no crop to torso or legs, fully covered. She strides, laughs and looks at the lens with amusement — subject with agency, not display. This was the explicitly prompted-for constraint after the Tinder baddie reference was raised, and it held. |

## Scored dimensions

| Dimension | Weight | Raw | Weighted | Why |
|---|---|---|---|---|
| Stop-scroll | ×2.0 | 4.0 | 8.00 | The laugh against the split coral/pink wall is genuinely arresting, and the cream-card format looks unlike anything else in a dating feed. Docked one point because there is no idea in the picture — it is a mood, and the entire hook lives in the caption layer. Muted and captionless it is a woman having a good day. |
| Craft / realism | ×2.0 | 2.5 | 5.00 | **The weak dimension.** Flow's native picture is 720×702, upscaled to 1000px wide, generated on Omni 1.1 Flash — Google's weakest video tier. Visibly soft, most obviously in the hands and in background detail. Plus the double sunglasses. Nowhere near "indistinguishable from a real shot". A Veo-tier re-run is the obvious fix and was not tried. |
| Brand-fit register | ×1.5 | 3.5 | 5.25 | Cream ground, Gabarito, the correct two-tone lowercase wordmark, and a dignified-but-warm read rather than swipe-app party energy. Docked because the swagger register belongs to the 18–22 treatment in `rules/targeting.md`, and this is being pointed at a 25–30 ad set whose hook was written in the security register. That mismatch is a deliberate app-owner call, not an oversight — but it is a real cost against this dimension. |
| Palette differentiation | ×1.0 | 5.0 | 5.00 | Cream `#FFF3F0` ground, coral and brand pink — straight off `creative-style.md`. Maximally differentiated in a feed where every rival ships dark. |
| Type-safe space | ×1.0 | 5.0 | 5.00 | The card layout gives dedicated cream bands above and below the picture. Caption, tagline and wordmark all sit inside the §7 safe lines (192 / 1632), and the empty band below the wordmark is exactly the platform-chrome zone. This is the dimension round 3 scored 2.0 on; the format fixed it. |
| **Total** | | | **28.25 / 37.5** | Marginally ahead of round 3's 27.75, and for opposite reasons — round 3 won on character consistency and lost on aspect ratio and type space; this wins on type space and palette and loses on craft. |

## Not covered by this pass

- **Meta and Snap synthetic-media disclosure.** Both platforms carry their own
  rules for AI-generated people in ads. Flagged in
  `campaigns/moveon-w2530-meta/record.md` on 2026-08-28 as binding separately and
  never checked; a fully generated person *on video* is more exposed than the
  still was. Still unchecked. This gate cannot clear it.
- **§6.2 first-person narration.** Not applicable: nobody speaks, and the captions
  are general aphorisms rather than a personal-results claim — the same test the
  live still passed. The blocked `../moveon-properly-w2530/script.md` fails this;
  this asset does not go near it.
- **Comment moderation.** Unresolved since 2026-08-27 and outside a creative QA
  pass, but it attaches to every breakup asset and is recorded here so it is not
  lost.

## If regenerated

The two cheapest wins, in order:

1. **Change the model tier off Omni 1.1 Flash.** Craft is the only dimension
   scoring below 3.5, and it is bounded by the tier rather than by the prompt.
2. **Fix the double sunglasses** — one pair, on her head or on her eyes, stated
   explicitly per shot in the prompt.

Neither blocks a ₹300/day directional test.
