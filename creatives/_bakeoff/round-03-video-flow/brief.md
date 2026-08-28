# Bake-off round 3 — first video round (Google Flow)

**Opened 2026-08-28.** `tools.md` registered AI video for "later rounds — revisit after
stills prove the loop." Rounds 1 and 2 were stills; this is the first video candidate.

## How this round differs from 1 and 2

It is **not brief-driven**. Rounds 1 and 2 started from a written brief dispatched to a
lineup. This candidate came the other way round: the user generated it in Google Flow
exploratorily and brought the file back. There was no `brief.md` before the pixels
existed, and no tool lineup — one tool, one output.

That is worth stating plainly rather than back-filling a brief to make the round look
tidy. What it costs us: no controlled comparison, and no way to attribute the result to
a prompt clause. What it still buys: the first real evidence about whether AI video
clears the gates at all, and — more usefully — a **format** finding that generalises.

## The candidate

`candidates/flow-storyboard-grid-1.mp4` — 1280×720, 24fps, 10.005s, 240 frames, h264,
with a stereo AAC track. Filename from Flow: `Animate_storyboard_grid_sequence_...`.

Contact sheet at `candidates/flow-storyboard-grid-1-frames.jpg` (12 frames, ~0.83s apart)
so specific moments can be pointed at without re-deriving them.

Content: a woman in a coral blazer carried across ~8 panels — street exterior, isolated
reaction shots on cream, then a cafe two-shot with a man — resolving to a `riteangle`
endcard reading "Verified, not vibes / Minutes, not months."

## Not known

Recorded as unknown rather than guessed. Both bear on whether this repeats:

1. **What it cost.** Flow credits consumed, and which model tier (Veo 3.1 vs 3.1 Fast vs
   the free Omni Flash) — unrecorded at generation time.
2. **Whether a character reference was supplied**, or Flow invented the woman from the
   prompt. This is the whole question behind the consistency result below. If she was
   referenced, the finding is about Flow's reference adherence; if invented, it is about
   the storyboard-grid format holding a face the model made up.

## The format, which is the actual finding

"Storyboard grid sequence" sits at rung 2–3 of the control ladder in
`research/notes/note-2026-08-28-two-ai-video-tutorials.md`: panels behave as pre-approved
stills, and the model supplies only pans, reveals and re-crops rather than inventing
motion. Because no single shot is held continuously, temporal artifacts have no runway to
accumulate. That is the most plausible explanation for the consistency result, and it is a
repeatable pathway rather than a lucky generation.
