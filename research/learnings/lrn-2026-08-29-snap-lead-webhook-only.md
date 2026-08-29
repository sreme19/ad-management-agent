---
id: lrn-2026-08-29-snap-lead-webhook-only
subject: tracking
claim: Snap delivers lead-form submissions only by webhook, signed HMAC-SHA256 over
  {timestamp}.{body} with the timestamp from a 't' header and the signature in a header
  named 'signature'. There is no endpoint that lists or downloads leads, and registration
  does not backfill.
source: platform-doc
confidence: high
sample_n: null
status: open
created: '2026-08-29'
last_confirmed: '2026-08-29'
review_after: '2027-02-25'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Snap delivers lead-form submissions only by webhook, signed HMAC-SHA256 over {timestamp}.{body} with the timestamp from a 't' header and the signature in a header named 'signature'. There is no endpoint that lists or downloads leads, and registration does not backfill.

## Evidence

- (2026-08-29) Verified end-to-end 2026-08-29 against the live Riteangle Snap account. GET /adaccounts/{id}/lead_generation_forms returns form metadata only; no leads endpoint exists. Registration is POST /v1/lead_gen/integrations/public_webhook with the body wrapped in a 'webhook_integrations' list -- unwrapped it answers 500 INTERNAL_FAILURE. Three response shapes for one object: create returns snake_case webhook_integrations/webhook_integration/integration_id, the docs example shows camelCase, and the list endpoint returns partner_integrations with the url nested under generic_webhook_handler_info. Reading the wrong key returns an empty list with no error, which made 'snap-leads forms' report all seven forms as unregistered. Signing the raw body alone yields 401; the first live test delivery is what revealed the {timestamp}.{body} scheme and the header name. Test delivery then returned 200 and correctly rejected Snap's dummy phone as no_usable_contact.
