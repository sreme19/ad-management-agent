# Creative generation rules — Grok Imagine prompts and the plate/type split

Source: Sree's 2026-08-24 session, working back from the first four live Snap/Meta assets
(`SC_AD_IMG_CONNECTION`, `SC_AD_IMG_V1_DONTSETTLE`, `RA_LEAD_WOMEN_SNAP1_20260818`,
`SC_LEAD_CASUAL_MEN_SNAP1_20260817`) and the lead-flow result they produced: **98% of lead-form
submissions were men, and 100% of the `/get` → Play Store taps were men.** Three of those four assets
put a woman in the frame as the object of it; two carry luxury/provider signifiers that
`compliance.md` rule #1 forbids. Both failures are generation-time failures — they were decided by the
prompt, not by the targeting — which is why this file exists as a rule rather than as advice.

Subject to `compliance.md` first, always. `creative-style.md` owns tone, taglines, quotable stats and
palette; this file owns how an asset actually gets produced from them.

## 1. The POV rule — read this before writing a single prompt

**The person the ad is targeting is the person whose point of view the frame occupies.** They are not
the thing being looked at.

This is the whole diagnosis of the 98/2 split. An ad that depicts a desirable woman recruits men,
whatever the ad set's gender targeting says — and on a submit-optimized objective the delivery
algorithm compounds it, because men submit dating lead forms far more readily.

- **Women's creative: no woman as the object of the frame.** Not a better-styled woman, not a more
  tasteful one — none. Occupy her POV instead: what she sees, what she's sick of, what she gets. The
  strongest available material is her *interface* (the ranked shortlist, the AI vetting him on her
  behalf) and her *frustration* (the flood, the closed tab), both already written up in
  `creative-style.md`'s ad-ready threads.
- **Men's creative:** the same rule applied symmetrically. His POV is the desert and the silence — "like
  the Martian stranded on Mars," then real choice. A woman shown as the reward is off-limits here too;
  it is the same giver/receiver framing `compliance.md` rule #1 bans, just pointed the other way.
- **Couple shots are the default failure mode.** A glamorous couple reads as an aspirational tableau
  addressed to nobody in particular. `RA_LEAD_WOMEN_SNAP1_20260818` is named for women and does exactly
  this. If a couple appears at all, one of them is the viewer, and the frame has to make that obvious.

## 2. Generate the plate, never the typography

**Prompt Grok for the scene only. Overlay every word yourself** (Canva/Figma), as a separate layer.

Reasons, in order of how much they cost when ignored:

1. `creative-style.md` makes lowercase **riteangle** in Gabarito a non-negotiable brand mark. A sampler
   cannot be trusted to hold casing, spelling, or typeface — and the lowercase "rite" spelling is what
   carries the pun.
2. Image models garble text, and garbled text on a paid asset is unshippable — but you often only see
   it at Story size, after spend.
3. A plate with no baked-in type is **re-cuttable**. All four current assets have their headline burned
   into the pixels, so testing a new hook against the same scene means regenerating the image. That is
   the single biggest drag on variant throughput, and it's self-inflicted.

The plate carries: subject, setting, lighting, wardrobe, palette, composition, and deliberate empty
space where type will land. Say where the empty space goes in the prompt.

## 3. Prompt skeleton

Write every prompt in this order. It keeps the compliance-relevant clauses in fixed positions so QA can
find them.

```
[SUBJECT + POV]  who is in frame, and whose eyes we're behind
[ACTION/MOMENT]  what is happening — a moment, not a pose
[SETTING]        ordinary Indian-context specifics (see §4)
[WARDROBE]       plain, contemporary, unbranded
[LIGHT]          natural, warm, soft; daylight over nightclub
[PALETTE]        cream/warm neutrals; brand pink only as a small accent
[COMPOSITION]    9:16 vertical, and where the type-safe empty space sits
[RENDER]         photographic, clean, no artefacts
[NEGATIVE]       the standing avoid-list from §4, verbatim
```

## 4. The standing negative list — non-negotiable, paste into every prompt

`compliance.md` rule #1 covers **visual** signalling, not just copy, so the avoid-list has to name
signifiers rather than concepts — a model cannot act on "no provider framing," but it can act on "no
ballroom, no gown."

**Never generate:**

- Gowns, tuxedos, evening formalwear, ballrooms, grand staircases, marble lobbies, chandeliers, hotel
  corridors, luxury cars, cash, jewellery presented as display, designer-branded goods.
- Anyone kneeling, serving, fastening, carrying, paying, or gifting — any giver/receiver staging.
  (`SC_AD_IMG_V1_DONTSETTLE` — a man fastening a woman's shoe under the word "exclusive" — is the
  reference failure. It is rule #1 rendered literally.)
- A woman posed as an object of desire: back-to-camera reveals, over-the-shoulder glances at the
  viewer, lingerie or slip-dress framing, cropped bodies.
- AI-tool watermarks or labels of any kind. Glitched hands, extra fingers, melted jewellery, warped
  faces, invented text anywhere in the frame.
- A man's real, unenhanced photograph (`compliance.md` §6.1) — if a man appears, he is rendered the way
  the product's own AI-enhanced portraits render him.
- Anyone who could read as under 18. No exceptions, no ambiguity — Snap's dating category enforces this
  on top of our own rule.

**Always specify:** Indian models, Indian-context setting, contemporary and ordinary rather than
aspirational-luxury, 18+ and unambiguously adult.

## 5. Palette, and the dark-creative trap

`creative-style.md` says the light palette is a deliberate differentiator: every major rival ships dark
dating creative, so cream reads as different in-feed before a word is read. **All four current assets
are dark.** In-feed they are indistinguishable from a Tinder ad, which forfeits the one visual
advantage the brand has decided to buy.

- Ground: cream `#FFF3F0`, surface `#FBEEE9`. Ask for warm daylight, not neon or nightclub.
- Accent: brand pink `#FF3B6B`, sparingly, and in the type layer where you control it exactly.
- Ink: `#1B1020` for all text.
- Amber `#F59E0B` and red `#EF4444` are functional status colours in-product and **must not appear as
  decorative accents** in creative.
- Teal, not pink, for anything aimed at networking season / platonic mode.

## 6. When not to use Grok at all

Grok Imagine generates photographic scenes. It does not generate the product.

**Route to Figma/CSS mockup instead** whenever the asset *is* an interface: her ranked shortlist, the AI
vetting him on her behalf, the hand-off banner, his four-stage progress bar, the Date/Network toggle.
`creative-style.md` records that these renders already exist — brief from them rather than commissioning
illustration, and check with whoever holds the mockups first.

This matters most for the women's lane, because §1 pushes the strongest women's asset toward *her
interface* — which means the highest-value women's creative is a mockup, not a generation. A prompt pack
is allowed to say "variant B is a UI render, not a Grok asset" and stop there.

## 7. Format and duration

- **9:16 vertical**, 1080×1920, for Snap Story and Meta Stories/Reels. Meta feed placements get a
  separate 4:5 or 1:1 crop from the same plate — plan the type-safe space so one plate survives both.
- **Six seconds is short** (`creative-style.md`'s production constraint). Where video is used, the
  emotional beat lands in the first two seconds; anything that needs a build lands better as a still.
- Keep the bottom ~15% and top ~10% clear of anything load-bearing — the platform's own chrome, CTA
  pill and profile row sit there. All four current assets crowd the CTA.

## 8. Variant discipline

Per `naming.md`, `[VARIANT]` is A/B/C on the **same hook**. A variant set changes **one** variable at a
time — the hook line, or the scene, or the CTA — never several at once, or the read is uninterpretable
at the sample sizes this account actually gets (`budget.md`'s `MIN_SAMPLE = 30`).

Three variants per hook is the working default: enough to see a spread, few enough that each one clears
the floor when the ad set is funded at ₹800–1,200/day.

## 9. What gets written down, and where

- **This file** holds the conventions — refined in place whenever a pass teaches something, the same way
  every other file under `rules/` works.
- **`creatives/<slug>/prompts.md`** holds the instances: one block per variant, each carrying the hook
  slug (from `creative-style.md`'s ad-ready threads vocabulary), the full prompt text as pasted into
  Grok, the type-layer copy kept separate from it, and the `rec_id` it was generated for.
- **`creatives/<slug>/qa.md`** holds the second-pass verdict per §10.
- When `log-review` lands a verdict on the rec, **write that verdict back onto `prompts.md`.** The point
  of keeping the exact prompt text is that a ranked prompt library accumulates across campaigns — which
  prompt patterns produce assets that earn taps, per persona. A prompt with no outcome attached to it
  taught nothing.

## 10. The QA gate — a second pass, not the same one

`compliance.md` §8 requires an independent check, and generated imagery is exactly where it earns its
keep: the pass that wrote the prompt is the worst possible judge of whether the output honoured it.

Check the rendered asset **as an image**, not as copy:

1. §4's negative list — any signifier present?
2. §1's POV rule — who is the object of this frame?
3. AI artefacts, watermark, garbled text, hands.
4. Wordmark: present, lowercase, Gabarito, correct spelling.
5. Legible at actual Story size on a phone, not just at desktop zoom.
6. Cream or dark — and if dark, is there a stated reason?
7. Safe areas (§7) clear of the platform's chrome.

Verdict is one of **`pass`** · **`regenerate`** (naming the exact prompt clause to change) ·
**`escalate`** (a `compliance.md` hit — the app owner's decision, never a quiet edit). Record it in
`creatives/<slug>/qa.md`. Nothing reaches `ad-agent propose` without a `pass`.
