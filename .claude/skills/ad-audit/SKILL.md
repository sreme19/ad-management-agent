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

**Known blind spot, until it is fixed:** the `--audience` filter cannot see ad sets whose names follow
`rules/naming.md`. `pocket-dating-coach`'s `audienceOf()` infers audience from gender words in the
campaign name and `utm_*` values, and a conforming ad set carries UUIDs and a gender-free campaign
name — so `WOMEN_18-22_CASUAL_LPV` classifies as `unknown`. Read that ad set by ad-set id, never by
audience filter, and treat any men-vs-women split as blind to it. See
`lrn-2026-08-26-naming-conformance-breaks-audience-cut`.

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

0. **`ad-agent open` first.** It lists every live record with its review date, which ones are past
   their kill/double window, and — the one that changes how you read a number — which are funded below
   `rules/budget.md`'s floor. An ad set running under the floor produces an `inconclusive`, not a weak
   result, and knowing that before you look at its tap rate stops you writing the wrong verdict.
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
     --summary "..." [--review-log /tmp/review.md] [--learning <lrn-id>]...
   ```
   **This writes to three places, not one**, and you should read what it prints. Besides the record: it
   appends the outcome to the creative's `prompts.md` with the audience and the effective daily spend
   (`rules/creative-generation.md` §9 — a ranked prompt library is the reason the exact prompt text is
   kept, and a prompt with no outcome attached taught nothing); and it walks `record → idea →
   learnings` and marks every claim the recommendation rested on.

   `working` supports those claims, `not-working` contradicts them, and **`inconclusive` records the
   evidence without moving the belief** — which is the correct outcome when a campaign was unreadable
   for reasons that say nothing about the claim, a spend cap below the floor being the obvious one.

   If it prints `learnings: none`, the record is not linked to any belief and this verdict corrects
   nothing in the library. That is worth a beat: either attach one with `--learning`, or notice that
   the recommendation was never grounded in a recorded claim in the first place.

   Only a record that actually ran can be reviewed, and only once. A later finding on a reviewed record
   is `ad-agent note`, or `log-evidence` on the learning it bears on — not a second verdict.
6. **Check `stats` for the bigger picture** once individual records are reviewed:
   ```
   ad-agent stats
   ad-agent dump-ledger [--status live|reviewed|proposed|abandoned]
   ```
   Look for patterns worth escalating to `ad-ideation` — a persona that consistently underperforms, a
   creative angle that consistently wins, a network where nothing has cleared `MIN_SAMPLE` yet.

7. **File what you could not explain.** An `inconclusive` verdict, an anomaly with no cause, a number
   that disagrees with another number — these are the raw material of the next research pass, and they
   evaporate if they only appear in this session's output:
   ```
   ad-agent question --text "..." --kind tracking|audience|creative|channel|... \
     --why "what decision it unblocks" --raised-by <rec_id>
   ```
   An unexplained result does not stay unexplained. It gets attached to whatever hypothesis is nearest
   when the next weak read arrives — which has already happened here once, when a `conversion_page_views:
   0` reading was confidently blamed for a stuck learning phase it had nothing to do with.

8. **Record a durable finding as a learning, not just a verdict.** A verdict is about one ad set; a
   learning is about the world and outlives the campaign that produced it:
   ```
   ad-agent learn --claim "..." --subject ... --source live-data --confidence high|medium|low \
     --sample-n <n> --evidence "..."
   ```
   `--sample-n` is required for `live-data` and the claim can only be `low` below `MIN_SAMPLE = 30` —
   the same floor this skill already applies to verdicts, enforced by the command rather than by you
   remembering.

## Status checks ("how are the ads doing")

Don't just read the leaderboard — read it against the ledger. "Ad set X is at 4.2% tap rate" is a
number; "Ad set X (from `rec-2026-08-15-casual-selective`, recommended because [reason]) is
outperforming its stated hypothesis at 4.2% tap rate on n=140" is a finding someone can act on.

## Later: this can become a scheduled task, not yet

Per `SPEC.md` decision #2, this skill is manual-trigger-only until it's been run by hand enough times
to trust unattended — same order `job-hunt-agent`'s `incubator-sweep` moved from on-demand to a Claude
Code scheduled task. Don't set one up unprompted.
