# Round 02 prompt pack — dispatch-ready

Paste these as-is. One fresh chat per plate (round 1 established that Gemini edits
anchor hard to the established subject, so a new face needs a new chat). Save
outputs to `candidates/<tool>-<slot>-<n>.png` and log a row in `candidates.md`.

## The reference, read off five Bumble frames Sree supplied

| # | What it is | What transfers |
|---|---|---|
| 1 | Overlapping rounded photo cards, yellow pills hanging off the edges reading "Outdoors" / "Running" / "Dog parent". Woman with a skateboard, laughing, park. | Candid **activity**, not a portrait. She is holding an object and doing something. |
| 2 | Yellow cards, cream inner panels, phone mock plus layered profile cards with blue "ID verified" badges. | Layered depth; verification shown as a visible badge. |
| 3 | Couple laughing over fries in a restaurant, warm light, yellow circular "MEMBER CIRCLE" seal. | Real, unposed, mid-laugh, eyes creased. Nobody looking at the lens. |
| 4 | High-key black-and-white couple, white ground, her laughing hard, eyes shut. | **Eyes shut, laughing.** The most alive frame in the set. |
| 5 | Three phones on flat colour, centre one showing a woman shot from below against sky, tilted back mid-laugh. | Low angle, sky behind, upward tilt. The in-app photo is itself a candid. |

**The single common factor: not one person is holding a neutral pose.** Every frame
is mid-laugh, mid-motion or mid-activity. Our round-1 hero is a woman sitting still
looking pleasant, and that — not colour — is the whole gap.

## Two constraints that override the reference

**Cream stays.** Sree, this session: do not change the page's colour palette. So no
yellow ground and no black-and-white, whatever frames 4 and 5 do. `t1-bw` already
lost 3.5 points on the rubric for exactly this. Plates come back warm and high-key,
with the cream ground intact.

**No couples.** Frames 3 and 4 are couples, and `creative-generation.md` §1 calls
the couple shot the default failure mode — "a glamorous couple reads as an
aspirational tableau addressed to nobody in particular." The frame Riteangle can
borrow from them is the *laughing*, not the pairing. Solo, every time. No man in
frame at all keeps §6.1 out of the conversation entirely.

---

## SLOT 1 — `hero`. Replaces the static portrait.

```
A candid editorial photograph of one Indian woman, 27, in an ordinary sunlit
Bangalore flat. She is caught MID-LAUGH — head tipped slightly back, eyes creased
almost shut, a real laugh and not a smile held for a camera. She is not posing and
not looking into the lens.

Light: bright warm afternoon daylight from a large window, high-key, airy, soft
shadows. Cream and off-white walls, pale wood, a plant. The whole frame reads warm
cream, never grey and never dark.

Wardrobe: unbranded contemporary Indian-urban, muted — a plain tee or a simple
cotton kurta in a soft dusty tone.

Camera: 50mm, shallow depth of field, shot slightly below eye level looking
gently up. Photojournalistic, natural skin texture with visible pores, no beauty
retouching, no glossy studio finish.

Composition: she sits in the lower two-thirds with clean uncluttered wall above
her. Vertical, must crop cleanly to both 3:4 and 4:5.

NEGATIVE: no text, no watermark, no logo, no captions, no man, no couple, no
second person, no dark or moody background, no nightclub, no studio backdrop, no
luxury or designer signifiers, no jewellery beyond small studs, no direct
to-camera posed smile, no black-and-white, no yellow.
```

## SLOT 2 — `moment`. Replaces the café phone-down still.

```
A candid editorial photograph of one Indian woman, 27, in motion on an ordinary
Bangalore street in warm late-afternoon light. She is mid-step, walking and
laughing at something out of frame, bag over one shoulder, hair moving. Her face
may be partly turned away — this is a moment, not a portrait.

Light: golden warm daylight, high-key, airy. Cream and sand-coloured walls behind,
softly out of focus.

Camera: 35mm, shot from slightly behind and to the side so we travel with her.
Slight motion blur in the hands and hair. Natural, unposed, documentary.

Composition: she occupies one third of the frame with open warm space beside her.
Vertical, crops cleanly to 4:5.

NEGATIVE: no text, no watermark, no logo, no man, no couple, no crowd, no traffic
chaos, no dark background, no posing to camera, no black-and-white, no yellow.
```

## SLOT 3 — `interface`. Only if it beats what we have.

Round-1's `clean-b` composite currently holds this slot and no competitor shows an
interface, so the bar is high. Reference frame 5 is the shape to beat: three phones
overlapping at depth, the centre one forward.

```
A photograph of three modern smartphones overlapping at slight angles on a plain
warm cream background, the centre phone forward and upright, the outer two angled
behind and partly cut off by the frame edges. Studio product photography, soft
even light, gentle contact shadows.

EVERY SCREEN MUST BE PURE FLAT WHITE AND COMPLETELY BLANK — no interface, no text,
no icons, no status bar. The screens are placeholders that will be composited
afterwards.

Vertical, crops cleanly to 4:5.

NEGATIVE: no text anywhere, no watermark, no logo, no brand marks, no app UI, no
content on any screen, no hands, no people, no dark background, no yellow.
```

Blank screens on purpose: `prep-get-w-images.py` finds a pure-white screen by
threshold and perspective-warps our own shortlist render into it. That is how the
current `shortlist.jpg` was made, and it is why the plate must arrive empty.

---

## Routing, per `tools.md`

- **Slots 1 and 2** → Gemini fresh chat first, ChatGPT second. Both reproduce cream;
  Grok defaults dark and is out for these.
- **Slot 3** → ChatGPT first. Cleanest at plain object studio shots, and its
  weakness (garbling text) cannot bite on a plate that must carry none.
- Aim for 3–4 candidates per slot. Score every one, including the losers — a
  candidate with no verdict taught nothing.

## Scoring reminder

`rubric.md`, hard gates first. For this round, watch two in particular: eyes shut
mid-laugh is exactly where samplers produce distorted teeth and collapsed eye
sockets (craft gate), and "candid attractive woman" is the prompt most likely to
drift into posed-for-desire (§1 gate → escalate, not a re-cut).
