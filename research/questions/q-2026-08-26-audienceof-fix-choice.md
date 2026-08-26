---
id: q-2026-08-26-audienceof-fix-choice
kind: tracking
status: open
asked: '2026-08-26'
raised_by: lrn-2026-08-26-naming-conformance-breaks-audience-cut
answered: null
learning: null
---

## Question

Should audienceOf() classify on the resolved ad-set name, or should the ad-set name be carried in utm_content alongside the ad name?

## Why it matters

Both fix the blind audience cut and they are not equivalent. Classifying on the resolved name needs no URL change and the information is already present - the leaderboard displays WOMEN_18-22_CASUAL_LPV correctly for the very rows the classifier reads as unknown. Carrying the name in utm_content is quicker and costs nothing on Snap, where utm_id is the join, but on Meta utm_content IS the ad-level join key per tracking.md, so it would change what that parameter means on one network and not the other - exactly the cross-network confusion tracking.md warns against. The fix lands in pocket-dating-coach either way; this repo can only recommend.
