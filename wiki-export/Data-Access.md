# Data Access

## The principle

This agent should never re-derive `pocket-dating-coach`'s ad-analytics aggregation itself. That
aggregation — the sample-size gating, the bot-traffic exclusion, the ad-set-keyed leaderboard — is
several hundred carefully-tuned lines with exactly one correct owner. Anything this repo needs should
come from calling that logic, never reimplementing a piece of it.

## Channel 1 — the authenticated analytics endpoint (primary)

A route on `pocket-dating-coach`, `/api/internal/ad-analytics`, authenticated by a bearer token
(`ADS_AGENT_API_KEY`) instead of the admin session cookie, calling the exact same `buildAdAnalytics()`
function the admin dashboard itself uses and returning the identical JSON shape. This is the answer for
any rate, tap rate, cost-per-signup, or verdict. `ad-agent fetch-analytics` calls this.

**Status: not built yet.** This is one of two pieces of outstanding work on the `pocket-dating-coach`
side — see [Open Work](Open-Work).

## Channel 2 — a least-privilege read-only database role (secondary)

A Postgres role, `ads_agent_ro`, granted `SELECT` only, only on `ad_spend_daily`,
`ad_demographics_daily`, `marketing_page_views`, `marketing_store_clicks`, `user_acquisition`, and
`ad_fx_rates`. For raw, exploratory lookups the analytics endpoint doesn't answer — never for
recomputing a number channel 1 already owns. Two independently-computed answers to the same question
is a worse failure mode than not having the number at all.

**Status: not built yet.** The other piece of outstanding work — see [Open Work](Open-Work).

## The boundary that doesn't move

This agent never gets read access to `verified_vibe_users` or any other table carrying member data —
names, emails, chat transcripts, trust scores. The read-only role above is scoped to marketing/ad
tables by construction; there is no path from this agent to member data, by design, not by convention.

## Where secrets live

`ADS_AGENT_API_KEY` and the `ads_agent_ro` connection string are never committed to either repository.
They live only in this repo's own `config.local.yaml`, which is gitignored — see `config.example.yaml`
for the shape. A fresh clone of this repo (on a laptop or in a sandbox) has neither value until someone
puts them there deliberately.
