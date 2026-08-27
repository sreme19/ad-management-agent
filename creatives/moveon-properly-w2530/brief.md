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
