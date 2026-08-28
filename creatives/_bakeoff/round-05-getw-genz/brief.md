# Round 05 brief — Gen Z women imagery for /get/w

**Opened 2026-08-28 by Sree, on sight of the live page:** "this picture on the
landing page looks pretty bad." The picture is `hero.jpg` — the round-02 winner
`gemini-hero-1`, which scored 34.0/37.5 and shipped on 2026-08-27. The owner's
read of the live page overrides the rubric score; the rubric measured the plate
in isolation, he is looking at it in the page.

## What is actually wrong with it, beyond "bad"

Named here so the prompts have something to fix, not just something to replace.

1. **It is a room, not a life.** She sits still on a sofa. Round 02's own brief
   diagnosed the round-1 plate as "a woman sitting still looking pleasant" and
   fixed the *face* (mid-laugh) without fixing the *body* — she is still seated
   and static. The Bumble reference the round was built from is people mid-motion.
2. **The props are generic.** Potted plant, framed prints, beige sofa. It could
   sell insurance, a therapy app or a sofa. Nothing in it is 22-to-27, Indian,
   urban, or 2026.
3. **She is alone, and the page's promise is social.** "Vetted before he reaches
   you" is about what other people are like. One woman alone in a flat carries
   none of that.
4. **It eats the fold.** The image occupies a full screen between the promise and
   the CTA, so the first-party proof (`14 suitors ranked`, `proof never stored`)
   is pushed further down — the exact defect
   `note-2026-08-26-competitor-landing-pages` recorded and recommendation 2 was
   supposed to fix.
5. **Age register is wrong for the audience it fronts.** It reads late-twenties
   domestic. The women's ad sets running against this page are `w1822` and
   `w2530`.

## The goal for this round

A set — not one plate — of Gen Z women images for `/get/w`: **solo and group**.
Group is the new material; nothing in `creatives/` has ever shown more than one
person, and the page has room for a band of friends where it currently has a
sofa.

## Tool

**Google Flow**, per Sree. First use of Flow for stills — rounds 03 and 04 used
it for video. Its advantage here is `Characters`: cast three women once, save
them, then recall with `@name` so the group shots and the solo shots show the
same people. Nothing else in `tools.md` holds identity across plates.

Read `tools.md` § *Working with Google Flow* before generating. The image
default is 9:16 and the Western-background default bit round 03.

## Hard gates for this round specifically

- **`compliance.md` §6.3 — 18+.** "Gen Z" in 2026 reaches down to fourteen. Every
  prompt names an explicit adult age and no plate showing anyone who could read
  as a minor advances, however good it looks.
- **`creative-generation.md` §1 — POV.** Women's surface: she is never the object
  of the frame. Attitude, energy and eye contact are permitted (`tools.md` #11);
  posed-for-desire is not. Solo or all-women groups only — no man in frame keeps
  §6.1 out of the conversation.
- **`compliance.md` §6.2 + `tools.md` #17** — characters built from *descriptions*
  only. Never upload a real person's photo into Flow, and never build an avatar.
- **Cream stays.** Sree, 2026-08-27, still standing. Cream is the ground; the
  subject carries the coral/pink accent (`tools.md` #8).
- **No typography in the plate** (`creative-generation.md` §2).

## Deliverables

`prompts.md` holds the pack. Save outputs to `candidates/flow-<slot>-<n>.png`,
log a row in `candidates.md`, score on `rubric.md` in a pass that did not write
the prompt, and record Flow's model tier and credit cost per generation
(`tools.md` #16).
