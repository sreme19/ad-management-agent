---
id: note-2026-08-26-lpv-count-discrepancy
title: Snap vs first-party landing-page-view counts (commit b470386)
source: own-research
captured: '2026-08-26'
learnings:
- lrn-2026-08-26-snap-and-beacon-disagree-on-lpv
- lrn-2026-08-26-conversion-page-views-is-the-wrong-field
---

# Landing-page-view count discrepancy — from commit b470386, 2026-08-26

Snapshotted verbatim from the commit message of b470386 ("Attach the account's Snap
pixel when creating an ad squad"), which is where this was first written down.
Recorded by a parallel session, not by this one.

---

Attach the account's Snap pixel when creating an ad squad

Every LANDING_PAGE_VIEW ad squad in this account carries pixel
0657d30b-4d65-414b-b9a9-65edb4aa1e07 — including Female 18-22-LPV, the 20.9%
tap-rate squad this recommendation is modelled on. The first squad snap-push
created carried none, because create_adsquad never passed one. It is now a
required argument, and the plan printed before anything is created shows it,
so a missing pixel is visible rather than silent.

Correcting the record on why. I first read `conversion_page_views: 0` off the
ad squad stats and concluded Snap could not see landing-page views at all,
and that this explained the stuck learning phase, the 8.1x frequency and the
whole day's budget going in ninety minutes. That was wrong, and Ads Manager
says so plainly: 59 landing page views at Rs 5.91 each. `conversion_page_views`
was simply the wrong field. For a WEB_VIEW ad Snap renders the page in its own
in-app browser and counts the load natively, with no pixel involved.

So the missing pixel is a real inconsistency with the account's own
convention and worth fixing, but it is not the cause of anything observed
today. The docstring says so, so the next reader does not inherit the wrong
story.

Still unexplained, and left open rather than guessed at: Snap counts 59
landing page views where our own site counts 96 for the same ad squad.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
