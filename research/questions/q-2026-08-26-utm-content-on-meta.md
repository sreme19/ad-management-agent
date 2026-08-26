---
id: q-2026-08-26-utm-content-on-meta
kind: tracking
status: open
asked: '2026-08-26'
raised_by: null
answered: null
learning: null
---

## Question

Does utm_content carry the ad name or the ad id on Meta? tracking.md's URL template and its own prose disagree.

## Why it matters

The template shows utm_content={{ad.name}} for both networks, while the prose says utm_content is Meta's ad-level id and is what traffic-quality.ts joins on for the meta network. Both cannot hold on Meta: writing the name there breaks the join, writing the id there loses the human-readable label the template promises. networks.yaml follows the prose, since that is the half naming the code that reads it, and _utm_url now writes the id into whichever parameter the registry marks as the ad join. But the rule file still contradicts itself and should be corrected once someone confirms against a real Meta URL. No Meta ad is created by this repo, so nothing is broken today - this is a trap set for the first person who builds one.
