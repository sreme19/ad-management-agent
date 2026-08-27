# Round 02 — /get/w landing imagery, Bumble register

**Goal:** replace the three images on the live women's landing page. Round-1 plates
were cut for a 9:16 Snap Story and re-cropped for web; they read static and
neutral. Sree's note: "the images are not the best," with Bumble named as the
reference.

**Surface:** web landing page, not a Story. This changes the brief in one way that
matters — the PAGE sets the type in real Gabarito, so unlike round 1 these plates
carry **no burned-in words at all**. Compose for a photograph that stands alone.

## What Bumble actually does — from our own observation, not from memory

`research/notes/note-2026-08-27-bumble-tinder-india-13-posts.md`, three posts:

- **B1 "Love Stories: Neha & Mihir" (715 likes).** Black-and-white photograph of a
  couple on a mountain summit above cloud, *both arms thrown wide, laughing*. Large
  yellow display type over it; names in a yellow serif. Real people, named,
  credited, tagged.
- **B2 HYROX (1,690).** Bright yellow branded scaffold; a woman mid-conversation in
  activewear, caught in motion at a real event.
- **B3 indé wild Diwali (1,669).** Six young Indian women packed into frame, posing
  and laughing, festive colour, warm lights.

bumble.com itself reads: white ground, geometric sans, warm saturated portraits
against minimal backgrounds, rounded rectangular cards. Headline "We exist to bring
people closer to love."

**The transferable part is not the yellow.** It is: *people caught mid-motion and
mid-laugh, shot like an editorial rather than a stock portrait, real enough to be
somebody in particular.* Every Bumble frame has energy and a specific person in it.
Our round-1 hero is a well-lit woman holding still — that is the actual gap.

## The palette question, to be settled by score and not by argument

`creative-style.md` says the cream ground IS the differentiator: every major rival
ships dark, so cream reads as different before a word. Bumble's signature is honey
yellow (~#FFC629), and B1's signature treatment is black-and-white photography.
Both trade that differentiator away, and yellow specifically is a direct
competitor's brand colour — wearing it on our own landing page is confusing at
best.

`rubric.md` already prices this: Palette differentiation ×1.0, where 5 is
"cream/warm, different in-feed before a word". So run BOTH directions as
candidates, let the rubric take the hit where it falls, and read the total.

## Lineup — three plates needed

| Slot | Replaces | Brief |
|---|---|---|
| `hero` | a static portrait | One Indian woman, 25–30, Bangalore, caught MID-LAUGH or mid-turn — not holding a pose. Editorial, shallow depth, window light. She is the speaker (§1), addressing the viewer as a friend would. Attractive and put-together; per the agreed guardrail, confident-and-addressing-you, never posed-for-desire. |
| `moment` | the café phone-down | Her, in motion, in an ordinary Bangalore setting — stepping out of a doorway, walking, mid-conversation. Energy over stillness. No face required. |
| `interface` | the composited shortlist | KEEP round-1's `clean-b` composite. It scored well and no competitor shows an interface. Regenerate only if a candidate beats it outright. |

## Prompt skeleton — per `creative-generation.md` §3

```
[SUBJECT + POV]   one Indian woman, 25-30, whose eyes we are behind or who is
                  speaking to us; never the object of the frame
[ACTION/MOMENT]   a MOMENT, not a pose — mid-laugh, mid-turn, mid-step
[SETTING]         ordinary Bangalore: a cream-walled flat, a doorway, a street in
                  warm afternoon light. Never nightclub, never luxury
[LIGHT/GRADE]     warm natural colour, high-key, cream ground. Variant B
                  (black-and-white) WITHDRAWN — the palette does not change
[WARDROBE]        unbranded contemporary, muted
[COMPOSITION]     web landing image, 4:5 and 3:4 crops must both work. NO text
[NEGATIVE]        no text, no watermark, no logo, no luxury signifier, no man in
                  frame, no couple, no glossy studio look, no dark background
```

## Tools

Per `tools.md`: Gemini fresh chat and ChatGPT are the cream lane (both reproduce
it; Grok defaults dark and is out for variant A). For variant B's black-and-white,
Grok's dark/cinematic default becomes an advantage rather than a fault — worth one
candidate there.

**Fresh chat per distinct face** — round 1 established that Gemini edits anchor
hard to the established subject.

## Sharpened 2026-08-27 — five reference frames, and two constraints

Sree supplied five Bumble frames after this brief was first written. They change
it. See `prompts.md` for the frame-by-frame read and the dispatch-ready prompts;
the short version is that the reference is not a colour, it is that **not one
person in any of those frames is holding a neutral pose** — every one is mid-laugh,
mid-motion or mid-activity, several with eyes shut.

Two constraints settle what looked like open questions:

- **The page palette does not change.** Sree, explicitly, this session. So the
  yellow is out — no yellow ground, no yellow accents in CSS — and so is
  black-and-white. `t1-bw` had already lost 3.5 rubric points for abandoning cream;
  this closes it. Variant B is withdrawn from the lineup below.
- **No couples.** Two of the five references are couples, and §1 names the couple
  shot as the default failure mode. What transfers from them is the laughing, not
  the pairing.

## Status

Brief written 2026-08-27. **Not dispatched.** Generation runs through the user's
logged-in Chrome and neither browser surface was reachable in this session: the
in-app browser blocks by policy and the Claude-in-Chrome extension reported not
connected. Nothing below `candidates/` is a generated candidate yet — the files
there are treatments of round-1 plates, marked as such in the ledger, run to test
the palette question while generation is blocked.
