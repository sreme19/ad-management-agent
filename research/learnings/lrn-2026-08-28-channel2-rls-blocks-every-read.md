---
id: lrn-2026-08-28-channel2-rls-blocks-every-read
subject: tracking
claim: 'Channel 2 (ads_agent_ro read-only DB) has never worked: all six granted tables
  have RLS enabled with zero policies, so the role reads 0 rows from everything, silently.'
source: live-data
confidence: low
sample_n: 6
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2026-12-26'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Channel 2 (ads_agent_ro read-only DB) has never worked: all six granted tables have RLS enabled with zero policies, so the role reads 0 rows from everything, silently.

## Evidence

- (2026-08-28) CONFIDENCE LABEL IS A GATE ARTIFACT — see q-2026-08-27-min-sample-and-config-facts; n=6 is a census of all six granted tables. Verified 2026-08-28 over the corrected pooler connection: pg_class shows relrowsecurity=true on marketing_page_views, ad_spend_daily, marketing_store_clicks, user_acquisition, ad_demographics_daily and ad_fx_rates, and pg_policies contains zero policies for any of them. Postgres semantics: RLS on + no policy = zero rows for any role without BYPASSRLS, with no error raised. So 'select count(*) from marketing_page_views' returns 0 against a table the destination-gate verification of 2026-08-27 proves has real rows (the app reads via the Supabase service role, which bypasses RLS). TWO separate faults had to be fixed to even see this one: the configured direct host db.<project>.supabase.co is IPv6-only (no A record) and unreachable from an IPv4-only machine — the working route is aws-1-ap-southeast-1.pooler.supabase.com:6543 with the project-suffixed username, and the project is in Singapore, not India. FIX (belongs in pocket-dating-coach, needs owner privileges): one SELECT policy per table for ads_agent_ro, e.g. create policy ads_agent_ro_read on public.marketing_page_views for select to ads_agent_ro using (true). Until then the beacon side of every Meta/Snap traffic question is unanswerable from this repo.
