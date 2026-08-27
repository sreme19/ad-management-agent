---
id: q-2026-08-27-meta-utm-source-spelling
kind: tracking
status: answered
asked: '2026-08-27'
raised_by: null
answered: '2026-08-27'
learning: null
---

## Question

Is Meta's utm_source 'meta', or 'facebook'/'fb'?

## Why it matters

rules/networks.yaml declares utm_source: meta, and as of 2026-08-27 meta-push writes that literal onto every ad URL it creates. The spelling has never been checked against what pocket-dating-coach's normalisation actually accepts. This is the exact shape of the snap/snapchat mismatch — the registry's own header comment records that Snap's key is 'snap' while its utm_source is 'snapchat', and that discrepancy is why only 7 of 151 signups could be joined to a costed ad set. Two things make 'meta' suspect: the live campaigns in the account are named FB_TRAFFIC_* / FB_F_LEADS_*, and 'facebook' is the more common convention in the wild. If it is wrong, Meta spend cannot be joined to Meta traffic at all, and the ad set will look like it produced nothing. Cheap to settle before the first push by reading one existing live Meta URL.

## Answer (2026-08-27)

Neither 'meta' nor 'facebook' — it is 'fb' (or 'ig'). networkOf() in pocket-dating-coach/src/lib/server/traffic-quality.ts maps only ig/fb/instagram/facebook to 'meta' and falls everything else through to 'other'. Its docstring states the reason: 'utm_source is the PLACEMENT on Meta — real traffic arrives as ig or fb, never as meta — so grouping on the raw value would split one network into two rows that each look half as effective as it is.' lead-source.test.ts:43 carries a real row shaped { utm_source: 'fb', utm_campaign: '6978749199681' }. rules/networks.yaml had declared utm_source: meta since the registry was written; every Meta click would have classified as non-ad 'other' traffic, making the first Meta test read as zero. Fixed to 'fb' before the first push, so unlike the snap/snapchat mismatch (7 of 151 signups joinable) this one cost nothing. A literal was kept rather than Meta's {{site_source_name}} macro because an unresolved macro cost a week of spend on 2026-08-21 and networkOf treats fb and ig identically — only the fb-vs-ig placement split is lost, which is now q-2026-08-27-meta-placement-granularity.
