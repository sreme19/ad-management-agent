---
id: note-2026-08-26-audience-classification-break
title: Audience classification break on WOMEN_18-22_CASUAL_LPV
source: own-research
captured: '2026-08-26'
learnings:
- lrn-2026-08-26-womens-traffic-classifies-unknown
- lrn-2026-08-26-naming-conformance-breaks-audience-cut
- lrn-2026-08-26-audience-splits-rest-on-ad-hoc-names
---

# Incident note — audience classification, 2026-08-26

Recorded by a parallel session as `## Note — incident` on
campaigns/women-1822-casual-lpv/record.md (committed as 6ba0bc8). Snapshotted here
verbatim so the claims derived from it point at fixed text.

This ad set's traffic classifies as audience=unknown, not women. 103 views today, none of which fetch-analytics --audience women can see.

Cause: pocket-dating-coach's audienceOf() infers audience by finding gender words in the campaign name and utm_* values, because the landing page itself has no identity signal and deliberately never will. Older ad sets carried readable names in utm_campaign (sc_men_28_38_blr_casual) and classified cleanly. This ad set follows naming.md and tracking.md, so utm_term carries the ad squad UUID and utm_campaign is RA_TRAFFIC_GET_IN_PAN_TOF_202608 — no gender word appears anywhere in the URL.

So conforming to the naming and tracking rules broke the audience cut, and every ad set created through snap-push will inherit it. The ID-based scheme is what made ad-level attribution work this afternoon, so the scheme is not the thing to change.

Right fix: audienceOf() should classify on the resolved ad-set name rather than the raw row. The analytics already recovers that name — the leaderboard displays WOMEN_18-22_CASUAL_LPV correctly for these very rows — so the information is present, just not where the classifier looks. Quick alternative: carry the ad-set name in utm_content alongside the ad name, which costs nothing on Snap where utm_id is the join, but changes what utm_content means on Meta.

Practical effect meanwhile: any men-vs-women split in ad-audit is blind to this ad set. Read it by ad-set id, not by audience filter.
