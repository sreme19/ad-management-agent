# The video pipeline — Flow, four stages, demonstrated end to end 2026-08-29

Written from the MOVE-ON lead funnel session (`creatives/moveon-lead-w1830/`), which produced four
usable clips in one sitting after four earlier rounds produced one. **This file is the workflow;
`tools.md` is the tool.** Read `tools.md` for what Flow can do and this for the order to do it in.

**The pipeline exists because freeform prompting does not work.** Round 4 went straight to a prompt
and burned three storyboards on dull output. Every stage below is cheaper than the one after it, and
each catches a class of failure the next stage cannot.

```
1. CHARACTERS  (free, text)     → who
2. SCRIPT      (free, text)     → what happens
3. STRIP       (cheap, 1 image) → does the beat read
4. ANIMATE     (expensive)      → the clip
```

**Text iteration is free. Only generation costs credits. Be fussy at stages 1 and 2.**

---

## Stage 1 — Characters

Two fields, and they do different jobs. Most people fill the first and skip the second; the second is
where the rules live.

**Main description** — appearance. Ordinary prompt.

**Character Info** — "describe how your character acts". Flow's agent reads this when it *invents*
scenes, so a constraint written here propagates into every later generation instead of being
re-argued per prompt. Put the POV rule here:

> She is ALWAYS caught mid-action, never posing. She does not stand still for the camera, does not
> put a hand on her hip, and does not look into the lens. Photograph her the way a friend would, on a
> phone, in available light. Never a fashion lookbook, never a studio backdrop, never a styled
> editorial.

Also put wardrobe rules, an at-home/dressed-up split, and settings named by their objects.

### Four prompt techniques that measurably worked

1. **Describe the garment, don't just forbid the wrong one.** "Wide full shoulder straps that cover
   the shoulders, falling well past her waistband" beat "no crop top, no strapless", which had failed
   twice. The model renders what you describe and only weakly avoids what you forbid — and when the
   reference image contains the wrong garment, a bare exclusion always loses to it.
2. **Age by feature, not by number.** "Fine lines at her eyes when she smiles, a grown woman not a
   teenager" beat "27 years old". Models render what they can picture and largely ignore an integer.
   This matters: one reference plate came back reading under 18, which is `compliance.md` §6.3 and a
   platform-policy risk on a dating ad, not a taste note.
3. **Ask for plain before excluding text.** "The fabric is plain and unmarked" beat "no lettering",
   which returned garbled nonsense across the chest.
4. **Name the failure, not just the target.** "No beige hotel interiors, no upholstered headboards"
   fixed a drift that "an ordinary Indian bedroom" had not.

---

## Stage 2 — Storyboard Studio

`tools` → *prompting* → Storyboard Studio. Paste a script; it returns title, scenes, dialogue and
transitions as editable text, then an assets tab enumerating every character, location and prop.
Only then does it generate.

**Four checks in the assets tab before you let it generate anything:**

1. Did it reuse your saved characters or silently invent lookalikes?
2. Are props right — a phone that must be blank must be blank *here*.
3. Are locations Indian? This is where Flow's Western default gets baked in permanently.
4. **Delete every line of dialogue it wrote.** It returns dialogue by default regardless of
   instructions. See "The audio rule" below — this is not a style preference.

### Script-level blocks that fixed real failures

- **`EVERY SCENE MUST CONTAIN AN EVENT`** with three named emotional states per scene. The single
  biggest fix of the session. Without it every scene is a slow push-in and reads as a perfume ad —
  `tools.md` #10.
- **`TONE: wry, not sad`** as a top-level block, plus *sadness, tears, vacant expressions* in the
  EXCLUDE. You cannot prompt an absence, so name the positive state at every beat: `INTERESTED →
  FLAT → EYE-ROLL`.
- **`EXPOSURE`** as its own block. First generation came back near-black. Ads are watched outdoors
  on bright phones: *"bright enough to read on a phone in daylight; moody is fine, underexposed is
  not."*

---

## Stage 3 — The vertical strip

**Three panels stacked TOP TO BOTTOM with thin clean gutters, vertical 9:16.** One image, one credit
class, and it tells you whether the beat reads before you pay for motion.

**This closed `q-2026-08-28-storyboard-grid-vertical`.** Round 3's grid scored well and was held back
solely because 1280×720 landscape cannot crop to 1080×1920. The premise was subtly wrong: the
constraint was never that a grid needs horizontal room, it was that round 3 put panels *side by
side*. Stack them and the constraint disappears. See `lrn-2026-08-29-vertical-strip-format-works`.

**The reframe that matters: the strip is a preview, not a deliverable.** Round 3 tried to ship the
grid as the ad. Used as a check, its resolution stops mattering.

Judge a strip on whether the **beat** and the **light arc** read. Not on panel beauty.

---

## Stage 4 — Animate

Image-to-video from the approved strip. Four blocks, all load-bearing:

- **MOTION** — the three named states again, as a continuous arc with rough timings.
- **CAMERA** — *"handheld, static framing with natural micro-movement. No push in, no pull out, no
  pan, no zoom, no orbit."* Veo adds a slow push-in unprompted, and a drifting camera over a
  performance beat re-creates the perfume-ad problem the strip just solved.
- **CONSISTENCY** — name what must not change mid-clip. A hairband that appears in one panel will pop
  into existence mid-shot.
- **AUDIO** — see below.

### The audio rule, and why it is not negotiable

**Veo generates speech by default.** `compliance.md` §6.2 bars a generated person from narrating a
first-person experience of Riteangle — that is exactly what blocked the MOVE-ON *video* while
clearing the still. A silent cut has no first person to rewrite, which is why this whole format is
shippable at all.

So every animation prompt carries:

> AUDIO: ambience only. ABSOLUTELY NO SPEECH, no dialogue, no words, no conversation, no voiceover,
> no narration, no singing, no lyrics. Nobody says anything intelligible in any language.

Laughter and breath are fine — non-verbal, so they cannot constitute a claim.

**Verify by measurement, then by ear.** `ffmpeg -i clip.mp4 -af volumedetect -vn -f null /dev/null`.
Across this session: three near-silent clips read −35 to −46 dB mean; the wedding scene read
**−19.6 dB**, the profile of continuous content. Group and party scenes are where chatter appears.
A number is a screen, not a verdict — listen to anything above about −25 dB.

---

## Finishing every clip

1. **Trim to the beat.** Every 10s generation had ~4s of usable material and a tail that sagged —
   the performance peaks and then the model relaxes the face. End on the peak.
2. **Crop the watermark.** Flow leaves a visible mark bottom-right; §6.2 forbids a visible AI-tool
   watermark. It sits inside the bottom 20% that Reels UI covers anyway.
3. **Check resolution.** Everything came back **720×1280**, under Meta's recommended 1080×1920.
   Costed and untested at higher tiers — `q-2026-08-29-what-does-one-move-on-video`.
4. **Fix defects with per-clip editing, never a regenerate.** Select the clip, describe only the
   change. Round 4 shipped two pairs of sunglasses on one woman because this was not known.
5. **Record the model tier and the credit cost.** Not done in round 3, not done in round 4, not done
   in this session either. Three rounds, no numbers — which is why nobody can yet say whether this
   pipeline is affordable per variant.

## The one thing that does not work

**Cast consistency across scenes cannot be relied on** — `lrn-2026-08-29-flow-character-reference-is-unreliable`.
Single-character scenes hold the face and drift on wardrobe and props; the four-character scene lost
every face, added a fifth woman and changed the garment category despite explicit instructions.

**Consequence for planning, not just for prompting:** do not build a cut whose argument depends on
the same face recurring across scenes. The MOVE-ON film was designed so the woman drained in scene 1
is the woman laughing in scene 4, and that did not survive generation. Prefer three figures to four
in a group shot, and treat a recurring face as a bonus rather than a premise.
