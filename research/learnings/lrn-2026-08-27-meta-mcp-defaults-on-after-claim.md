---
id: lrn-2026-08-27-meta-mcp-defaults-on-after-claim
subject: tracking
claim: Claiming an ad account into a Meta business portfolio enables the ads MCP server
  channel for it at full permission by default (7 of 7, including create campaigns/ads
  and edit budget).
source: live-data
confidence: low
sample_n: 1
status: open
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-12-25'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Claiming an ad account into a Meta business portfolio enables the ads MCP server channel for it at full permission by default (7 of 7, including create campaigns/ads and edit budget).

## Evidence

- (2026-08-27) CONFIDENCE LABEL IS A GATE ARTIFACT — see q-2026-08-27-min-sample-and-config-facts; n=1 because there is one ad account. Observed 2026-08-27 immediately after ad account 1561367575690055 was claimed into portfolio 1587705756249660: Business settings > ads MCP server listed the account at 'Actions allowed: 7 of 7' with take actions, edit/set budget, create campaigns, create ad sets and create ads all Allowed. Nobody enabled it; it was on from the moment the claim completed. This directly contradicts the instruction given earlier the same day, which said to 'leave it off' and so would have caused nobody to look. Set to 0 of 7 / View only, Meta confirmed 'Changes saved', read access intact. Why it matters: SPEC.md's non-negotiable forbids a second unguarded write path into an account this repo drives, because MetaClient._call's refusals are worthless if a parallel channel can enable and re-budget the same objects. The check therefore has to be an ACTIVE verification after every claim, not a passive assumption about defaults.
