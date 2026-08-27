---
id: lrn-2026-08-27-audienceof-call-site-not-classifier
subject: tracking
claim: 'audienceOf() is not the broken part: the traffic call sites pass a row carrying
  only ids, while the spend call site already passes an ad-set name and classifies
  correctly'
source: source-code
confidence: high
sample_n: null
status: open
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-10-26'
derived_from: null
questions:
- q-2026-08-26-audienceof-fix-choice
recs: []
promoted_to: null
---

## Claim

audienceOf() is not the broken part: the traffic call sites pass a row carrying only ids, while the spend call site already passes an ad-set name and classifies correctly

## Evidence

- (2026-08-27) In pocket-dating-coach/src/lib/server/ad-analytics.ts, spendMatches calls audienceOf({campaign: s.ad_set_name ?? s.campaign_name}) and classifies WOMEN_18-22_CASUAL_LPV correctly. matchesFilters (views and taps) and the three facets splits call audienceOf(row) on a marketing_page_views / marketing_store_clicks row, whose haystack in ad-audience.ts is [campaign, utm_campaign, utm_content, utm_term] - all UUIDs and a gender-free campaign name under the naming rules. So spend classifies and traffic does not, in the same request. The name is already recoverable for those rows: the same file joins traffic to spend via adSetKeyOf(utm) and reads s.ad_set_name from the matched spend row, which is how the leaderboard displays WOMEN_18-22_CASUAL_LPV for the very rows the filter reads as unknown.
