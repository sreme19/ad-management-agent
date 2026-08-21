# Command cheatsheet

Every `ad-agent` command reads and writes the real ledger, or makes one plain HTTP call to
`pocket-dating-coach`. Nothing below ever touches Meta or Snap's Ads Manager &mdash; that always happens
by hand, in the actual Ads Manager UI, following what a skill hands you.

## "Recommend a new ad" (mode 5's write-back, run inside the skill)

```
ad-agent propose <slug> \
  --network snap|meta \
  --campaign-name "..." --ad-set-name "..." --ad-name "..." \
  --targeting-summary "..." --creative-ref "creatives/<path-or-id>" \
  --budget-cap <INR/day> --duration-days <n> \
  --brief /tmp/brief.md
```
Generates a `rec_id`, writes `campaigns/<slug>/record.md` with status `proposed`, regenerates
`INDEX.md`. You generally won't type this by hand &mdash; `ad-setup-loop` runs it once the
recommendation is ready and hands you the `rec_id` plainly.

## "I set the ad up by hand — log the real IDs"

```
ad-agent log-setup <rec_id> --network snap|meta \
  --campaign-id <real> --ad-set-id <real> --ad-id <real> \
  [--deviated "what changed from the brief, and why"]
```
Status → `live`. This is what lets `ad-audit` later join a real outcome back to this exact
recommendation, so this step is mandatory the moment an ad actually goes live &mdash; don't let it sit.

## "I decided not to run this one"

```
ad-agent abandon <rec_id> --reason "..."
```
Closes out a proposal that was never executed. Without this, it sits as `proposed` forever and pollutes
`stats`.

## "Write mode 6's verdict back to a live recommendation"

```
ad-agent log-review <rec_id> --verdict working|not-working|inconclusive \
  --summary "..." [--review-log /tmp/review.md]
```
Status → `reviewed`. `--review-log` is optional and holds the longer written detail behind the verdict.

## "How's the ledger looking overall?"

```
ad-agent stats
```
Deterministic counts, no network call: total records, a breakdown by status, and a breakdown by
verdict among reviewed ones.

```
ad-agent dump-ledger [--status proposed|executing|live|reviewed|abandoned]
```
Prints the same table `INDEX.md` holds, optionally filtered to one status, for an ad hoc copy-paste.

## "Pull real performance data" (mode 6, needs `config.local.yaml`)

```
ad-agent fetch-analytics --start <YYYY-MM-DD> --end <YYYY-MM-DD> \
  [--network all|snap|meta|other] [--audience all|men|women|unknown] \
  [--currency INR|USD] [--out /tmp/analytics.json]
```
Calls `pocket-dating-coach`'s authenticated `/api/internal/ad-analytics` endpoint. Fails with a clear
message, not a stack trace, if `pdc.analytics_url` / `pdc.api_key` aren't set yet in
`config.local.yaml` &mdash; see [Data access](Data-access) for why that's currently expected.

## First-time setup

```
cp config.example.yaml config.local.yaml   # then fill in pdc.api_key once it exists
pip install -e .
```
Everything except `fetch-analytics` works with zero setup &mdash; `config.local.yaml` only needs to
exist once `pocket-dating-coach`'s analytics endpoint has actually shipped.

## Keeping a laptop in sync with GitHub

```
scripts/sync.sh
```
Commits any dirty state with a timestamped message, pulls with rebase, then pushes &mdash; see
[Working across machines](Working-across-machines) for the full reasoning and the cron line that runs
this every 30 minutes as a backstop.

---

More commands get added here as new needs come up &mdash; this page is meant to grow with the tool.
