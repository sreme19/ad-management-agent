---
name: ad-audit
description: Research what's actually live and deployed on Riteangle's Snap/Meta campaigns, infer what's working and what isn't from real performance data, and write findings back to the ledger against the recommendations that produced them. Use whenever the user asks how the ads are doing, wants a performance review, asks what to pause/scale, or wants a status check across live campaigns.
---

# Auditing deployed ads (mode 6)

## Where the data comes from — and where it never comes from

Pull performance data via:

```
ad-agent fetch-analytics --start <YYYY-MM-DD> --end <YYYY-MM-DD> [--network snap|meta|all] [--audience ...]
```

This calls `pocket-dating-coach`'s authenticated internal endpoint, which runs the exact same
`buildAdAnalytics()` aggregation the admin dashboard itself uses — the same `MIN_SAMPLE = 30` gating,
the same bot-traffic exclusion, the same ad-set-keyed leaderboard. **Never recompute a rate, tap rate,
cost-per-signup, or verdict from raw Supabase rows even if you have read access to them** — that access
(if configured — see `config.example.yaml`'s `pdc.readonly_db_url`) exists only for raw, exploratory
lookups the analytics endpoint doesn't answer (a freshness check, a one-off row inspection), never for
recomputing something the endpoint already owns. Two independently-computed answers to "what's the tap
rate on this ad set" is a worse failure mode than not having the number at all.

If `fetch-analytics` errors because `pdc.analytics_url`/`pdc.api_key` aren't configured yet, say so
plainly — that means the `pocket-dating-coach` PR this depends on hasn't shipped (see `SPEC.md`, "Open /
deferred"). Don't fall back to guessing at numbers.

## Confidence gating — inherited, not optional

Any claim that a specific ad set "is working" or "isn't working" must respect the same
`MIN_SAMPLE = 30` floor the dashboard itself enforces (`rules/budget.md`). Below that sample, the
correct verdict is `inconclusive` — "not enough data yet" is a real finding, not a non-answer, and
reporting a guess as a verdict is the one mistake worth avoiding here above all others.

## Procedure

1. **Pull the leaderboard** for the range in question. Note `paidButNoTraffic` flags, anomalies, and
   any campaign the endpoint already flags as a spend leak — these are instrumentation findings, not
   performance opinions, and should be surfaced regardless of what else you find.
2. **Join to the ledger.** For every `live` record in `campaigns/`, look up its `ad_set_id` in the
   leaderboard (same `${network}:${ad_set_id}` key `pocket-dating-coach` uses internally — that's why
   `log-setup` records it that way). This is how a real outcome gets attributed back to the
   recommendation that produced it.
3. **Check what was actually executed vs. what was recommended.** Read the record's `--deviated` note
   (if any) before judging performance — a budget or creative change made at setup time changes what
   you're actually evaluating.
4. **Form a verdict per live record**: `working`, `not-working`, or `inconclusive` (sample too small).
   State the evidence plainly — the number, the sample size, and whether it cleared `MIN_SAMPLE`.
5. **Write the verdict back**:
   ```
   ad-agent log-review <rec_id> --verdict working|not-working|inconclusive \
     --summary "..." --review-log /tmp/review.md
   ```
6. **Check `stats` for the bigger picture** once individual records are reviewed:
   ```
   ad-agent stats
   ad-agent dump-ledger [--status live|reviewed|proposed|abandoned]
   ```
   Look for patterns worth escalating to `ad-ideation` — a persona that consistently underperforms, a
   creative angle that consistently wins, a network where nothing has cleared `MIN_SAMPLE` yet.

## Status checks ("how are the ads doing")

Don't just read the leaderboard — read it against the ledger. "Ad set X is at 4.2% tap rate" is a
number; "Ad set X (from `rec-2026-08-15-casual-selective`, recommended because [reason]) is
outperforming its stated hypothesis at 4.2% tap rate on n=140" is a finding someone can act on.

## Later: this can become a scheduled task, not yet

Per `SPEC.md` decision #2, this skill is manual-trigger-only until it's been run by hand enough times
to trust unattended — same order `job-hunt-agent`'s `incubator-sweep` moved from on-demand to a Claude
Code scheduled task. Don't set one up unprompted.
