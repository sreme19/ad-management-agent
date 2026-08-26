---
id: lrn-2026-08-26-conversion-page-views-is-the-wrong-field
subject: tracking
claim: conversion_page_views is the wrong Snap stats field for a WEB_VIEW ad, and
  reading zero from it does not mean Snap is blind to landing-page views
source: own-research
confidence: medium
sample_n: null
status: open
created: '2026-08-26'
last_confirmed: '2026-08-26'
review_after: '2026-12-24'
derived_from: note-2026-08-26-lpv-count-discrepancy
questions: []
recs: []
promoted_to: null
---

## Claim

conversion_page_views is the wrong Snap stats field for a WEB_VIEW ad, and reading zero from it does not mean Snap is blind to landing-page views

## Evidence

- (2026-08-26) Snap renders a WEB_VIEW ad's page in its own in-app browser and counts the load natively, with no pixel involved - it reported 59 views for a squad that carried no pixel at all. A conversion_page_views: 0 reading was briefly diagnosed as Snap being unable to see landing-page views, and as the explanation for the stuck learning phase, the 8.1x frequency and the day's budget going in ninety minutes. Ads Manager contradicted all of it. Recorded because the wrong story is the plausible one and someone reached it already.
