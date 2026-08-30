# BUILD-YOURSELF-FIRST — Snap lead carousel (13 stills)

Re-cuts `creatives/buildyourself-lead-w1830/asset-a.mp4` (the shipped 25.2s video)
into 13 still photos, at Sree's direction (2026-08-30) to try the same argument as
a photo format rather than video. Same story, same lines, same lead-gen objective
— the difference is delivery: not one video, not one Story-Ad sequence, but 13
independent single-image `LEAD_GENERATION` ads under the standing squad
(`WOMEN_18-30_CASUAL_MOVEON-LEAD`, campaign `RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608`).
Shipped this way on Sree's explicit call — see "Format decision" below.

## Argument (unchanged from the video)

Act 1, four beats of being let down (ghosted, catfished, "how long," "enough") →
Act 2 hinge ("khud ko bana sakti ho" — you can't change him, you can build
yourself) → Act 3, six "pehle apni ___" self-development beats → close ("pehle
tum, phir koi aur") → wordmark/CTA card. Full reasoning for this arc, including
why the thesis is deliberately *not* "you weren't focused on yourself" (that
reads as blaming her for being catfished), is in
`buildyourself-lead-w1830/brief.md` and isn't repeated here.

## Format decision, recorded

Two ways to ship 13 images on Snap were on the table:
1. A true **Story Ad** — one tappable sequence a viewer swipes through. `snap.py`
   has never built a `STORY` creative, and Snap's own docs describe Story-tile CTAs
   as App Install / Website, not Lead Gen — unverified whether a Story tile can
   carry `lead_generation_form_id` at all. Would need a `snap.py` change and an
   unconfirmed API capability.
2. **13 separate single-image lead ads**, same squad — buildable today with zero
   code changes (`upload_media` IMAGE + `create_lead_creative` + `create_lead_ad`,
   looped 13 times). No user-facing swipe-through; each is its own ad in Snap's
   own reporting.

Sree chose (2), explicitly: "ship these as 13 separate ads under the same squad
for now." Per `rules/funnel.md`'s rung ladder, a true carousel/Story format stays
rung 1 — a `snap.py` change not taken here.

## Sourcing — no new generation

Every plate is re-cut from stills this account already generated for the video
(`buildyourself-lead-w1830/_source/frames/`), plus one frame pulled from that
asset's Grok animation (`asset-g-win.jpg` — see `_derived/README.md`). No new Grok
prompt was written for this creative; `sourcing.md` maps every slide to its exact
source file, in place of a `prompts.md` (which is for new generations).

## Naming

Ad names use variant letters A–M for what's really 13 sequential story beats, not
a true A/B test of one hook — a stated deviation from `naming.md`'s letter-per-a/b-
variant convention, chosen because the alternative (13 distinct hook slugs) is
worse: these are one story, not 13 unrelated ideas. Recorded here rather than
silently reusing the convention's letter for something it wasn't written for.

`BUILD-YOURSELF-FIRST` is added to `creative-style.md`'s registered hook
vocabulary in this same session, closing a gap the shipped video already opened
(it used this slug before the thread was registered).

## Compliance — re-checked per slide, not just inherited from the video

Every slide passed `creative-generation.md` §1 (POV rule) and §4 (negative list)
individually, not merely because the source video passed as a whole:

- **`asset-c-alone.jpg`** replaces a frame that would have put a man in sharp,
  prominent focus in the foreground (the "raja beta" gaming-couch beat) — swapped
  for a solo restaurant still instead. That gaming-couch frame exists and is
  arguably closer to the video's actual Act 1, but wasn't used here; ask before
  reintroducing it.
- **`asset-g-win.jpg`** carries the video's known wardrobe deviation (jeans, not
  tennis kit) forward — see `_derived/README.md`.
- No AI-tool watermark on any slide: Grok's mark is cropped on `asset-g-win.jpg`
  per the standing convention; the Flow stills used elsewhere don't carry Flow's
  sparkle mark in the crops used (checked per-slide, not assumed).
- Wordmark on `asset-m-endcard.jpg` is lowercase `riteangle`, correct spelling, set
  in real Gabarito (the shipped video had to fall back to Futura — Gabarito is
  available on this machine now).

Full per-slide QA checklist in `qa.md`.
