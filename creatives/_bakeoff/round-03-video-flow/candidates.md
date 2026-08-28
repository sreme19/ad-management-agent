# Round 3 candidate ledger

Scored against `../rubric.md`. QA is a second pass per `creative-generation.md` §10 —
this scoring pass did not write the prompt (the user generated the candidate in Flow;
this assessment is Claude's).

| Candidate | Tool | Spec | Gates | Score | Verdict |
|---|---|---|---|---|---|
| `flow-storyboard-grid-1.mp4` | Google Flow | 1280×720, 24fps, 10.0s, h264 + AAC | pass, 1 concern | **27.75 / 37.5** | hold — see aspect ratio |

## Hard gates

| Gate | Result | Why |
|---|---|---|
| Real man's photo present | **pass** | The man in the cafe two-shot is generated, not a real man's photo |
| AI watermark / label, garbled text, glitched faces | **pass, with concern** | No visible watermark or label. Type is clean — the `riteangle` wordmark and heart render correctly and the tagline is fully legible, which is unusual for AI video. **The concern:** at ~2.5s the woman's expression is a strained, asymmetric grimace that reads as a blend artifact rather than a directed beat (see contact sheet, row 1 cell 3 / row 2 cell 1). Every other face in the piece is clean. This is the frame closest to a §4 fail and it is held in isolation, not buried in a transition |
| Anyone could read under 18 | **pass** | Both characters read clearly adult |
| Negative-list signifier | **pass** | No gown, luxury, cash, kneeling/serving. Coral blazer, street, cafe |
| Woman as OBJECT of the frame | **pass** | She is the POV throughout — reacting, speaking, and in conversation rather than posed for desire |

## Scored dimensions

| Dimension | Weight | Raw | Weighted | Why |
|---|---|---|---|---|
| Stop-scroll | ×2.0 | 3.5 | 7.00 | The grid-motion conceit is genuinely arresting and unlike anything else in-feed. Docked because landscape kills it in a vertical feed |
| Craft / realism | ×2.0 | 3.5 | 7.00 | Character consistency across ~8 panels is the standout — same bob, same blazer, same face structure, and the second character holds too. Docked for the 2.5s grimace and clipping audio |
| Brand-fit register | ×1.5 | 4.5 | 6.75 | Dignified and conversational. The cafe two-shot reads as an actual interaction rather than swipe-app party energy |
| Palette differentiation | ×1.0 | 5.0 | 5.00 | Cream and coral throughout — differentiated in-feed before a word is read |
| Type-safe space | ×1.0 | 2.0 | 2.00 | The grid fills the frame edge to edge. Live panels leave no clean top-third or bottom band; only the endcard has deliberate type space |
| **Total** | | | **27.75 / 37.5** | |

## Blocking issue — aspect ratio

**1280×720 landscape.** Every other asset in this repo is 1080×1920, and both Snap Story
and Meta Reels/Stories want vertical. This cannot be cropped to 9:16: the grid is
*composed* for landscape, so panels would need re-staging, not reframing.

That makes the aspect ratio, not the craft, the reason this does not advance. The
re-run worth doing is the same format with vertical specified from the start — the open
question being whether the grid conceit survives the aspect change at all, since it
depends on having horizontal room to place panels side by side.

## Other notes

- **Audio clips.** Mean −20.4 dB but max hits exactly −0.0 dBFS. Will sound harsh on phone
  speakers; normalising to ~−14 LUFS is a trivial fix.
- **Backgrounds default Western.** Yellow cab, US-style storefronts, brick-and-glass cafe
  exterior. The model was not steered to an Indian city.
- **The pink sparkle swoosh appears twice** and reads as stock Flow flourish rather than brand.
