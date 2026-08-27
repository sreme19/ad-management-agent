---
id: q-2026-08-27-meta-utm-campaign-name-or-id
kind: tracking
status: open
asked: '2026-08-27'
raised_by: null
answered: null
learning: null
---

## Question

Should utm_campaign on Meta carry the campaign NAME or the campaign ID?

## Why it matters

networks.utm_params writes the campaign NAME into utm_campaign for both networks. traffic-quality.ts's adSetKeyOf docstring, verified against the Marketing API on 2026-08-10, says the two networks differ: on Snap 'utm_campaign holds the ad set NAME rather than the campaign name', and on Meta 'utm_campaign and utm_id both hold the campaign id'. lead-source.test.ts:43 backs the Meta half with a real row: utm_campaign: '6978749199681', a numeric id. Meanwhile ad-health.ts:198 warns when 'its utm_campaign does not match anything arriving on the landing pages', which reads as comparing utm_campaign against a campaign NAME from spend. So the consumer's own files are not obviously consistent, and our value matches neither documented convention exactly. Not urgent: adSetName is only a FALLBACK used when adSetId is absent, and both pushes write utm_term with a real ad set id, so the join does not depend on it today. It matters for ad-health's mismatch warning and for any rollup that reads the denormalised campaign column. Settle it by reading a live row after the first Meta push lands, rather than by guessing now.
