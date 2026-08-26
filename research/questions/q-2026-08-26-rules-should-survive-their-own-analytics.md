---
id: q-2026-08-26-rules-should-survive-their-own-analytics
kind: tracking
status: open
asked: '2026-08-26'
raised_by: lrn-2026-08-26-naming-conformance-breaks-audience-cut
answered: null
learning: null
---

## Question

Should tracking.md require that a conforming URL still carries whatever the downstream analytics classify on, so following the rules cannot silently break the numbers that judge the rules?

## Why it matters

This failure was invisible for a full day of spend and was caught by someone looking, not by a check. tracking.md already has pre-launch and post-launch checklists; neither asks whether the resulting traffic classifies correctly. A rule set that can break its own measurement without anyone noticing is the same shape as the 2026-08-21 macro incident, and the answer probably belongs in that post-launch checklist rather than in a code change here.
