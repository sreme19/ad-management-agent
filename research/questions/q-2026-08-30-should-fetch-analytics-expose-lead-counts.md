---
id: q-2026-08-30-should-fetch-analytics-expose-lead-counts
kind: tracking
status: open
asked: '2026-08-30'
raised_by: lrn-2026-08-30-marketing-leads-undercounts-leads-by-design
answered: null
learning: null
---

## Question

Should fetch-analytics expose lead counts from marketing_lead_submissions, so ad-audit can see leads at all?

## Why it matters

As of 2026-08-30 the analytics endpoint returns views, taps, spend, leaderboard and LP funnel but no lead metric whatsoever, so mode 6 is structurally blind to the outcome the lead campaigns exist to produce — which is why nobody noticed 9 vs 7. The new submissions table is PII-free and safe to expose.
