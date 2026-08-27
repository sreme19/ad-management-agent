---
rec_id: rec-2026-08-27-moveon-w2530-meta
network: meta
status: proposed
campaign_name: RA_TRAFFIC_GETW_IN_BLR_TOF_202608
ad_set_name: WOMEN_25-30_CASUAL_MOVEON-LPV
ad_name: STORY_MOVE-ON-PROPER_A_20260827
campaign_id: null
ad_set_id: null
ad_id: null
targeting_summary: "Women 25-30, Bangalore, Advantage Audience off. CASUAL-SELECTIVE\
  \ persona \u2014 the security-register end of the 18-28 band per the Aug-5 age split.\
  \ The breakup re-entry hook (MOVE-ON-PROPER thread): moving on is not in question,\
  \ how is. Expansion deliberately off because the premise is a specific age band\
  \ and Meta broadens unless told not to."
targeting:
  gender: FEMALE
  min_age: '25'
  max_age: '30'
  countries:
  - in
  os: null
  expansion: false
  regulated_content: true
creative_ref: creatives/moveon-properly-w2530
destination_url: https://www.riteangle.dating/get/w
budget_cap_inr_per_day: 1000.0
duration_days: 5
from_idea: idea-2026-08-27-breakup-reentry-second-chapter
created: '2026-08-27'
last_note: '2026-08-28'
campaign_daily_cap_inr: null
campaign_lifetime_cap_inr: null
campaign_caps_verified: '2026-08-28'
---

## Brief (proposed)

# Deployment brief — MOVE-ON-PROPER, women 25–30, Meta

Reconstructed 2026-08-27 from `SESSION-RESUME-2026-08-27.md` §1, which recorded the
original as `/tmp/brief-moveon.md` and explicitly ephemeral. Written into the creative
folder this time so it survives the session.

**Network changed from the original brief.** The session that wrote it targeted Snap.
This proposes the same creative on **Meta**, because Meta creation became available on
2026-08-27 (`SPEC.md` decisions #3/#10, extended) and the asset is 1080×1920, which
serves Meta Reels/Stories as readily as Snap Story.

## The bet

The breakup re-entry hook, in her register: moving on is not in question, *how* is.
From `idea-2026-08-27-breakup-reentry-second-chapter` (verdict `recommend`), against the
`MOVE-ON-PROPER` thread in `rules/creative-style.md`. Reference format is Tinder's Move On
Salon — a woman narrating her own breakup rather than posed.

## Plan

| Field | Value |
|---|---|
| Campaign | `RA_TRAFFIC_GETW_IN_BLR_TOF_202608` |
| Ad set | `WOMEN_25-30_CASUAL_MOVEON-LPV` |
| Ad | `STORY_MOVE-ON-PROPER_A_20260827` |
| Targeting | Women, 25–30, India / Bangalore, Advantage Audience OFF |
| Persona | CASUAL-SELECTIVE — security-register end of the 18–28 band, per the Aug-5 age split |
| Destination | `https://www.riteangle.dating/get/w` (audience women — destination gate passes) |
| Budget | ₹1,000/day × 5 days |
| Creative | `asset-a.jpg` (1080×1920, bake-off round-1 winner c5, type set by `typeset.py`) |

Expansion is off deliberately: the whole premise is a specific age band, and Meta broadens
unless told not to. An ad set that quietly widened would answer a different question.

## Carried risks — surface these again before enabling

1. **§6.2 AI-labelling is escalated, not settled.** The §8 independent pass in `qa.md`
   returned `escalate`: the asset is an AI-generated portrait with a first-person breakup
   line, which reads as testimony from a real customer, and nothing labels it as generated.
   Covering the Gemini watermark addressed the "no tool watermark" half of §6.2 and moved
   away from the "label it" half. **App owner's decision, per `SPEC.md`'s compliance
   non-negotiables.** Note the push gate will NOT stop this: it greps `qa.md` for the string
   `pass`, and the finished-asset header still reads `pass`.
2. **No comment-moderation policy exists** for the hostility a public breakup hook attracts.
   Carried from the original brief, still unaddressed.
3. **Tracking on Meta is unproven.** Per `lrn-2026-08-27-meta-ads-carry-no-utms`, the live
   Meta ads carry no UTM parameters at all, so this will be the first Meta ad here ever to
   have them — meaning `utm_source: meta` is a convention this sets rather than matches, and
   `q-2026-08-27-meta-utm-source-spelling` is unresolved. If the spelling disagrees with
   `pocket-dating-coach`, the spend will not join to the traffic and the test reads as zero.
4. **Naming carries no network token.** `rules/naming.md`'s campaign and ad-set shapes have
   no network field, so this campaign name is identical to what a Snap push would produce.
   Harmless for the id-based joins, confusing for humans, and untested against
   `ad-analytics.ts`'s ad-set rollup with two networks in play.

## Note — creative (2026-08-27)

COMPLIANCE ESCALATION, unresolved — app owner's decision before enabling. The §8 independent pass in creatives/moveon-properly-w2530/qa.md returned escalate on rules/compliance.md §6.2 ('Label AI imagery'). The asset is a fully AI-generated portrait carrying a first-person breakup line, which reads as testimony from a real customer, and nothing in frame labels it as generated. Covering the Gemini watermark satisfied the 'no visible AI-tool watermark' half of §6.2 and moved away from the 'label it' half. Three options are written out in qa.md (label it / change the framing / narrow §6.2's scope in the rules file). Important: the push gate will NOT stop this — it greps qa.md for the string 'pass' and the finished-asset header still reads pass, so a document containing both 'pass' and 'escalate' passes the gate.

## Note — incident (2026-08-27)

TRACKING IS UNPROVEN ON THIS NETWORK. Per lrn-2026-08-27-meta-ads-carry-no-utms, every live Meta ad in account 1561367575690055 carries no UTM parameters at all (read directly from Ads Manager 2026-08-27: bare https://www.riteangle.dating/get, empty URL parameters field, Website events unchecked). So this will be the first Meta ad here ever to carry UTMs, which means utm_source=meta is a convention this record SETS rather than matches, and q-2026-08-27-meta-utm-source-spelling is still open. If that spelling disagrees with pocket-dating-coach's normalisation, the spend will not join to the traffic and this test will read as having produced nothing — the same failure as snap/snapchat, which left only 7 of 151 signups joinable. Settle the spelling before enabling.

## Note — observation (2026-08-27)

No comment-moderation policy exists for the hostility a public breakup hook attracts. Carried from the original brief on 2026-08-27 and still unaddressed. Meta comments are more exposed than Snap's, since a Meta ad IS a Page post and accumulates public replies under the Riteangle Page.

## Note — incident (2026-08-28)

Pushed to Meta PAUSED on 2026-08-28 and read back clean, 13/13 fields matching. Real ids: campaign 6984035763681, ad set 6984035818681, ad 6984036525881, tracked creative 3381749368661464. url_tags on the creative carry literal values with no macro: utm_source=fb, utm_term=6984035818681 (ad set id), utm_content=6984036525881 (ad id, which is what traffic-quality.ts joins on for Meta). Advantage Audience read back 0, so the 25-30 band held and was not silently broadened. All 83 creative enhancement features report OPT_OUT, so the QA-passed asset is intact. HOUSEKEEPING: the push took four attempts and left orphaned untracked creatives behind (1812181563532325, 3546135838888885, 982834978110685) plus duplicate uploaded images. All unused and costing nothing; meta.py cannot delete them by design, so remove them by hand in Ads Manager if the clutter matters.
