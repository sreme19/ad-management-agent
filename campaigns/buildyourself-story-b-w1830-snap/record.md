---
rec_id: rec-2026-08-30-buildyourself-story-b-w1830-snap
network: snap
status: proposed
campaign_name: RA_TRAFFIC_GETW_IN_PAN_TOF_202608
ad_set_name: WOMEN_18-30_CASUAL_MOVEON-STORY
ad_name: STORY_BUILD-YOURSELF-FIRST_B_20260830
campaign_id: null
ad_set_id: null
ad_id: null
targeting_summary: "Women 18-30, India pan-India, Android only, expansion off \u2014\
  \ reuses the existing MOVEON-STORY squad under RA_TRAFFIC_GETW_IN_PAN_TOF_202608\
  \ (TRAFFIC/WEB_VIEW Story Ad, SWIPES goal). Corrected re-cut of variant A: watermark\
  \ cropped, CTA APPLY_NOW, audio to be added in UI."
targeting:
  gender: FEMALE
  min_age: '18'
  max_age: '30'
  countries:
  - in
  os: ANDROID
  expansion: false
  regulated_content: true
creative_ref: creatives/buildyourself-carousel-w1830
destination_url: https://www.riteangle.dating/get/w
budget_cap_inr_per_day: 300.0
duration_days: 5
from_idea: null
created: '2026-08-30'
campaign_daily_cap_inr: null
campaign_lifetime_cap_inr: null
campaign_caps_verified: '2026-08-30'
last_note: '2026-08-30'
---

## Brief (proposed)

# BUILD-YOURSELF-FIRST — Snap Story Ad, corrected re-cut (variant B)

Replaces `STORY_BUILD-YOURSELF-FIRST_A_20260830` (rec-2026-08-30-buildyourself-story-w1830-snap),
which shipped live with three defects Sree caught on the Approved ad (2026-08-30):

1. **Google/Flow "made with AI" sparkle** was baked into several plates. Every Flow
   source still now passes through `strip_flow_watermark` (150px off the bottom, where
   the sparkle sits at a fixed offset); all 13 plates + the preview tile re-checked
   clean at full resolution. Cropped, not inpainted — Sree's explicit call.
2. **CTA button read "More."** The leaf snaps now carry `APPLY_NOW`, matching the ad's
   own "Apply now →" end card and the /get/w-apply funnel.
3. **No music.** One track from Snap's own audio library is to be added across the
   tiles — a UI-only step in Ads Manager (not in the Marketing API), done after push.

Everything else is unchanged from variant A: same 13-beat argument, same sequence,
same targeting (Women 18-30, India, Android, expansion off), same destination
(/get/w), same squad (WOMEN_18-30_CASUAL_MOVEON-STORY), same SWIPES optimisation.
Same creative folder, rebuilt. Variant letter B marks the corrected re-cut, not a new
hook — same A→M beat convention deviation recorded in the creative's brief.md.

## Note — creative (2026-08-30)

AUDIO NOT AVAILABLE for this format. Inspected the live Snap Ads Manager creative editor for this COMPOSITE Story Ad (via Claude-in-Chrome, 2026-08-30): every one of the 13 snaps exposes only Attachment/Website URL/Call-to-action/favouriting/button-colour/Smart-Prefetching — there is NO music/audio/sound control at the story level or per snap. Snap's audio library is offered for Single Image/Video ad formats, not for a tap-through web-view Story Ad. The 'one music bed across the tiles' request cannot be met on this ad type. Confirmed live: every snap's CTA reads 'Apply now', and the first snap's bottom-right corner is clean (watermark cropped).
