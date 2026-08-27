---
id: q-2026-08-27-meta-placement-granularity
kind: tracking
status: open
asked: '2026-08-27'
raised_by: null
answered: null
learning: null
---

## Question

Is losing the fb-vs-ig placement split worth avoiding a Meta macro in utm_source?

## Why it matters

utm_source is chosen as the literal 'fb' (q-2026-08-27-meta-utm-source-spelling). Meta's own {{site_source_name}} macro would resolve per impression to fb / ig / an / msg, giving real placement granularity — Instagram versus Facebook feed is a genuine performance question for a women's creative, and Reels versus Feed is where the cream-UGC bet either works or does not. The literal collapses that: networkOf treats fb and ig identically so the network join is unaffected, but the split is simply not recorded. Against the macro: an unresolved {{ad.id}} macro cost a week of unattributable spend on 2026-08-21, and adSetKeyOf rejects any value containing '{{' as absent, so a macro that fails resolves to no attribution at all rather than to something wrong. A middle option exists — keep the literal in utm_source and add {{site_source_name}} in a separate non-load-bearing parameter, so a failure loses granularity but never the join.
