---
id: q-2026-08-26-audienceof-fix-choice
kind: tracking
status: answered
asked: '2026-08-26'
raised_by: lrn-2026-08-26-naming-conformance-breaks-audience-cut
answered: '2026-08-27'
learning: lrn-2026-08-27-audienceof-call-site-not-classifier
---

## Question

Should audienceOf() classify on the resolved ad-set name, or should the ad-set name be carried in utm_content alongside the ad name?

## Why it matters

Both fix the blind audience cut and they are not equivalent. Classifying on the resolved name needs no URL change and the information is already present - the leaderboard displays WOMEN_18-22_CASUAL_LPV correctly for the very rows the classifier reads as unknown. Carrying the name in utm_content is quicker and costs nothing on Snap, where utm_id is the join, but on Meta utm_content IS the ad-level join key per tracking.md, so it would change what that parameter means on one network and not the other - exactly the cross-network confusion tracking.md warns against. The fix lands in pocket-dating-coach either way; this repo can only recommend.

## Answer (2026-08-27)

Neither of the two options in the original note. Classify traffic rows on their RESOLVED ad-set name, using the join ad-analytics.ts already performs.

Reading the source changed the diagnosis. audienceOf() works, and one of its call sites (spendMatches) already feeds it an ad-set name and gets the right answer. The rows that fail are the traffic rows, which carry only ids - and the join that recovers their ad-set name already exists further down the same file, because it is what makes the leaderboard display WOMEN_18-22_CASUAL_LPV for exactly the rows the filter reads as unknown.

So the fix is a call-site change in ad-analytics.ts: pass the resolved name to audienceOf for matchesFilters and the three facets splits, the way spendMatches already does. No URL change, no change to naming.md or tracking.md, nothing new for snap-push to emit, and no new failure mode for a future network.

That also settles the utm_content option as strictly worse rather than merely quicker: it would permanently overload the parameter that IS the ad-level join key on Meta, to carry information already recoverable on Snap today.

Caveat: acqMatches classifies on a.campaign from user_acquisition, a separate row set with its own naming, and this answer does not cover it. The change belongs to pocket-dating-coach; this repo can only recommend.
