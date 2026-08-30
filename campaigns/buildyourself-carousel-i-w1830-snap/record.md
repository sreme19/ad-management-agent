---
rec_id: rec-2026-08-30-buildyourself-carousel-i-w1830-snap
network: snap
status: abandoned
campaign_name: RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608
ad_set_name: WOMEN_18-30_CASUAL_MOVEON-LEAD
ad_name: IMG_BUILD-YOURSELF-FIRST_I_20260830
campaign_id: 1326aa05-902c-4cec-be92-0a7440ac536d
ad_set_id: 85c2e782-ea07-4216-8986-f272bdb5d4d7
ad_id: c7282ea3-e135-4bc3-bca8-443fa7dcfd32
targeting_summary: "Women 18-30, India pan-India, Android only, expansion off, segment\
  \ 4673160157025603 excluded \u2014 inherited unchanged from the live ad squad (reused,\
  \ not created)"
targeting:
  gender: FEMALE
  min_age: '18'
  max_age: '30'
  countries:
  - in
  os: ANDROID
  expansion: false
  regulated_content: true
creative_ref: creatives/buildyourself-carousel-w1830/i-world
destination_url: https://www.riteangle.dating/get/w-apply
budget_cap_inr_per_day: 300.0
duration_days: 5
from_idea: null
created: '2026-08-30'
campaign_daily_cap_inr: 300.0
campaign_lifetime_cap_inr: null
campaign_caps_verified: '2026-08-30'
executed: '2026-08-30'
last_note: '2026-08-30'
abandoned: '2026-08-30'
---

## Brief (proposed)

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
asset's Grok animation (`g-win/asset-a.jpg` — see `_derived/README.md`). No new Grok
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

- **`c-alone/asset-a.jpg`** replaces a frame that would have put a man in sharp,
  prominent focus in the foreground (the "raja beta" gaming-couch beat) — swapped
  for a solo restaurant still instead. That gaming-couch frame exists and is
  arguably closer to the video's actual Act 1, but wasn't used here; ask before
  reintroducing it.
- **`g-win/asset-a.jpg`** carries the video's known wardrobe deviation (jeans, not
  tennis kit) forward — see `_derived/README.md`.
- No AI-tool watermark on any slide: Grok's mark is cropped on `g-win/asset-a.jpg`
  per the standing convention; the Flow stills used elsewhere don't carry Flow's
  sparkle mark in the crops used (checked per-slide, not assumed).
- Wordmark on `m-endcard/asset-a.jpg` is lowercase `riteangle`, correct spelling, set
  in real Gabarito (the shipped video had to fall back to Futura — Gabarito is
  available on this machine now).

Full per-slide QA checklist in `qa.md`.

## Execution

- Date: 2026-08-30
- Campaign ID: 1326aa05-902c-4cec-be92-0a7440ac536d
- Ad set ID: 85c2e782-ea07-4216-8986-f272bdb5d4d7
- Ad ID: c7282ea3-e135-4bc3-bca8-443fa7dcfd32

## Note — observation (2026-08-30)

ATTRIBUTION, verified not assumed: the shared lead form 1897accc-cd6b-4f60-9269-d76ec149842d was checked live after this push — updated_at is still 2026-08-29T07:51:37.920Z (unchanged) and its default_end_page URL still carries utm_content=VID_MOVE-ON-PROPER_A_20260829, the ad that originally created the form, not this ad and not any of the other 12 in this carousel set (or the BUILD-YOURSELF-FIRST video ad, which reused the same form earlier today). So leads from all 13 carousel ads, the video ad, and MOVE-ON-PROPER itself land on /get/w-apply carrying the SAME utm_content. Ad-level attribution among any of these exists only in Snap's own per-ad delivery reporting (impressions/spend/submissions by ad_id), never in the pocket-dating-coach beacon. The per-ad utm_content this push printed in its plan is what WOULD be on the URL if this ad had created the form — it did not, so don't trust that line, same caveat rec-2026-08-30-buildyourself-lead-w1830-snap already recorded.

## Abandoned

- Date: 2026-08-30
- Reason: Wrong ad format. Sree's original ask was one Snap carousel ad — a single ad the viewer taps/swipes through image by image (his phrase: 'the images go from one to another when clicking'), which Snap calls a Collection Ad or Story Ad depending on layout. This was built and pushed instead as 13 separate single-image LEAD_GENERATION ads under the standing squad — misreading 'ship these as 13 separate ads under the same squad for now' (Sree's own words, in response to a question this session posed) as the full answer, when what Sree actually meant only became clear once he saw the result and named the real format. All 13 ads were deleted from Snap via DELETE /ads/{id} (confirmed successful, verified 0 remain under the squad beyond the 2 pre-existing ads). Their creative and media objects cannot be deleted through Snap's API at all (no DELETE endpoint exists for /creatives or /media — confirmed against developers.snap.com and by a live 400/E3003 on every attempt) and are permanently orphaned but inert: not attached to any ad, no spend, no delivery, invisible in Ads Manager's ad list. Superseded by a rebuild of this creative as an actual Collection/Story ad, once that formats's requirements are confirmed.
