---
id: q-2026-08-26-utm-content-on-meta
kind: tracking
status: answered
asked: '2026-08-26'
raised_by: null
answered: '2026-08-27'
learning: null
---

## Question

Does utm_content carry the ad name or the ad id on Meta? tracking.md's URL template and its own prose disagree.

## Why it matters

The template shows utm_content={{ad.name}} for both networks, while the prose says utm_content is Meta's ad-level id and is what traffic-quality.ts joins on for the meta network. Both cannot hold on Meta: writing the name there breaks the join, writing the id there loses the human-readable label the template promises. networks.yaml follows the prose, since that is the half naming the code that reads it, and _utm_url now writes the id into whichever parameter the registry marks as the ad join. But the rule file still contradicts itself and should be corrected once someone confirms against a real Meta URL.

**Escalated 2026-08-27: the trap is now armed.** This question closed with "no Meta ad is created by this repo, so nothing is broken today - this is a trap set for the first person who builds one." `meta-push` was built that day, and it writes the ad id into `utm_content` following the registry. So the guess this question flagged is now the shipped behaviour on a live-account write path, and it is still unverified against a real Meta URL or against traffic-quality.ts. If the prose is wrong, the first Meta push loses the human-readable ad label AND breaks the ad-level join - the same class of failure as the snap/snapchat utm_source mismatch that left only 7 of 151 signups joinable to a costed ad set. **Resolve this before the first real meta-push, not after.**

## Answer (2026-08-27)

utm_content carries the AD ID on Meta. Confirmed by reading pocket-dating-coach/src/lib/server/traffic-quality.ts on 2026-08-27: adSetKeyOf computes 'adId = network === "snap" ? uuidOrNull(raw.utm_id) : network === "meta" ? clean(raw.utm_content) : null'. So the prose half of rules/tracking.md was right and its single URL template was wrong, and networks.utm_params already implemented the correct behaviour by writing the ad id into whichever parameter the registry marks as ad_join_param. Snap has both parameters available (utm_id for the id, utm_content for the readable ad name) so it keeps both; Meta must spend utm_content on the id and therefore has no human-readable ad label in its URLs. rules/tracking.md's template and a new per-network table now say this explicitly. The trap this question warned about — 'set for the first person who builds one' — did not fire: meta-push shipped the correct behaviour.
