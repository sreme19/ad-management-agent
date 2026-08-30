---
id: q-2026-08-30-why-has-no-snap-lead
kind: tracking
status: open
asked: '2026-08-30'
raised_by: lrn-2026-08-30-marketing-leads-undercounts-leads-by-design
answered: null
learning: null
---

## Question

Why has no Snap lead ever been stored via the live webhook, when the integration is registered, the receiver validates signatures, and Snap's test delivery returns 200?

## Why it matters

Leads are being lost right now. The integration was created 2026-08-29T15:09:53Z; every lead submitted after that (HashLy Mk 01:38Z and Suraj Hyalij 02:31Z on 08-30) is absent from marketing_leads, and the 7 that are present were bulk-imported hours after submission. Snap's test payload is discarded by isSnapTestPayload before it reaches recordAdLead, so the one green check we have never exercised the storage path. Until this is answered every lead costs Rs 47 and lands nowhere.
