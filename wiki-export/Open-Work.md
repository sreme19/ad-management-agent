# Open Work

Two pieces of outstanding work, both on the `pocket-dating-coach` side, not in this repo. Until they
land, `ad-agent fetch-analytics` (and therefore the audit mode) cannot pull real performance data.

## 1. The authenticated internal analytics endpoint

A new route, something like `/api/internal/ad-analytics`, that calls `buildAdAnalytics()` — the exact
same function the admin dashboard already uses — and returns the identical JSON shape, but
authenticated by a bearer token checked against a new environment variable (`ADS_AGENT_API_KEY`)
instead of the admin session cookie. GET only, no mutation capability, no other admin functionality
reachable through it. The token itself is a long random secret generated once and added to the
`pocket-dating-coach` Vercel project's environment variables — never committed to source, never logged.

## 2. The least-privilege read-only database role

A plain SQL migration (checked into `pocket-dating-coach`'s existing migrations folder, not routed
through Supabase's row-level-security/service-role model) creating a role, `ads_agent_ro`, granted
`SELECT` only, only on `ad_spend_daily`, `ad_demographics_daily`, `marketing_page_views`,
`marketing_store_clicks`, `user_acquisition`, and `ad_fx_rates`. Must never be granted access, directly
or through a view, to `verified_vibe_users` or any other table carrying member data — that exclusion is
a hard security boundary, not a convenience choice.

## Why these are tracked here and not as code in this repo

Both changes live in a different codebase (`pocket-dating-coach`) with its own deploy pipeline and its
own production database. This repo's role is to consume what they produce, not to contain their
implementation.
