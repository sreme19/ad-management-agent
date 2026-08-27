---
id: q-2026-08-27-meta-utm-source-spelling
kind: tracking
status: open
asked: '2026-08-27'
raised_by: null
answered: null
learning: null
---

## Question

Is Meta's utm_source 'meta', or 'facebook'/'fb'?

## Why it matters

rules/networks.yaml declares utm_source: meta, and as of 2026-08-27 meta-push writes that literal onto every ad URL it creates. The spelling has never been checked against what pocket-dating-coach's normalisation actually accepts. This is the exact shape of the snap/snapchat mismatch — the registry's own header comment records that Snap's key is 'snap' while its utm_source is 'snapchat', and that discrepancy is why only 7 of 151 signups could be joined to a costed ad set. Two things make 'meta' suspect: the live campaigns in the account are named FB_TRAFFIC_* / FB_F_LEADS_*, and 'facebook' is the more common convention in the wild. If it is wrong, Meta spend cannot be joined to Meta traffic at all, and the ad set will look like it produced nothing. Cheap to settle before the first push by reading one existing live Meta URL.
