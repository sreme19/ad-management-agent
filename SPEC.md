# ad-management-agent — Spec

**Status: v1 scaffold.** Ledger CLI (`propose` / `amend` / `log-setup` / `log-review` / `abandon` /
`stats` / `dump-ledger` / `fetch-analytics`) and four skills are built. `fetch-analytics` cannot do anything
real yet — it depends on a small `pocket-dating-coach` PR (see "Data access") that has not landed.

## Problem framing

Riteangle (product name; the codebase and internal identifiers say `verified_vibe_*` and the
consumer-facing site is `pocket-dating-coach`) runs paid social campaigns on Snap and Meta to drive
signups. Campaign setup, performance research, and creative ideation were happening ad hoc, with no
memory of what was recommended vs. what was actually run, and no single place encoding the targeting/
creative/compliance rules that should govern every campaign. This repo is a loop-engineered,
harness-driven agent — in the same spirit as the user's `job-hunt-agent` — that runs those modes as
skills inside a Claude Code session, with no metered Anthropic API key anywhere in it.

## Locked decisions

1. **No Anthropic API key, anywhere, ever, in this repo.** Unlike `job-hunt-agent`, there is no
   API-calling reference implementation to build later — every mode here is a skill that does its
   reasoning live in whatever Claude Code session is running it, and persists results through this
   repo's zero-API CLI (`ad-agent ...`). The CLI never imports or calls an Anthropic client.
2. **Four skills, manual-trigger-only for v1:**
   - `ad-setup-loop` — mode 5: recommend campaign/ad-set/ad names, targeting, and creative; write the
     recommendation back to the ledger; later, once you've set it up by hand, log the real IDs.
   - `ad-audit` — mode 6: research what's live and deployed, infer what's working, write findings back
     to the ledger against the recommendations that produced them. Candidate for a scheduled task later,
     the same way `job-hunt-agent`'s `incubator-sweep` moved from on-demand to a Claude Code scheduled
     task once it was trusted — not attempted until `ad-setup-loop` and `ad-audit` have been run by hand
     enough times to trust unattended.
   - `ad-ideation` — mode 7: deep research into what could be deployed next; every idea ends in a
     `recommend` or `hold` verdict with a stated estimated spend, mirroring job-hunt's `fit`/`risk`
     verdict gate. An approved idea feeds into `ad-setup-loop`.
   - `ad-intake` — mode 8: you paste or describe an ad you found elsewhere; the skill learns from it and
     can feed a resulting idea into `ad-setup-loop`. Direct analog of job-hunt's `linkedin-opportunity`.
3. **The non-negotiable boundary (locked, survives any future plugin):** this agent never calls a Meta
   or Snap Ads Manager API to create, publish, enable, or change budget on anything live. Every
   `ad-setup-loop` output is instructions a human executes by hand in Ads Manager. "Steers
   implementation" (the eventual Claude plugin the user described) means telling the human what to
   click, field by field — never clicking it. Money and audience reach are on the line, not just an
   account ban (the reasoning job-hunt used for its own "never automate a send" rule) — this rule is
   stricter, not looser.
4. **The close-the-loop step is mandatory, not optional.** A `propose`d recommendation with no
   `log-setup` sits as an open loose end forever; `ad-audit` cannot join a recommendation to a real
   outcome without the real `ad_set_id` on record. See "Ledger" below for the exact lifecycle.
5. **Every recommendation states a budget/duration cap.** `ad-agent propose` requires `--budget-cap`
   (INR/day) and `--duration-days`. A recommendation with no stated cost is missing the thing the human
   would actually decide on.
6. **Confidence gating inherited from `pocket-dating-coach`.** Any claim in `ad-audit` that a live ad set
   "is/isn't working" must respect the same `MIN_SAMPLE = 30` floor `ad-analytics.ts` uses — below that,
   the verdict is `inconclusive`, not a guess dressed as a finding. `ad-ideation` (mode 7) is allowed to
   reason more loosely, since it is proposing hypotheses to test, not reporting on live data.
7. **Data access — two channels, not one, with a rule for which does what.**
   - **Channel 1 (primary, for anything already a computed metric):** an authenticated internal
     endpoint on `pocket-dating-coach`, `/api/internal/ad-analytics`, checked against a bearer token
     (`ADS_AGENT_API_KEY`) instead of the admin session cookie, calling the exact same
     `buildAdAnalytics()` function the dashboard itself calls. Zero duplicated aggregation logic —
     `pocket-dating-coach` stays the single owner of every rate, every `MIN_SAMPLE` gate, every
     bot-traffic exclusion. This PR has **not shipped yet** — `fetch-analytics` in this repo is wired
     up and waiting for it.
   - **Channel 2 (secondary, raw/exploratory only):** a least-privilege, read-only Postgres role
     (`ads_agent_ro`) granted `SELECT` on `ad_spend_daily`, `ad_demographics_daily`,
     `marketing_page_views`, `marketing_store_clicks`, `user_acquisition`, `ad_fx_rates` — nothing
     else. **Never used to recompute a rate, verdict, or total that channel 1 already owns** — only for
     one-off raw lookups the analytics endpoint doesn't answer. Also not built yet.
   - **PII boundary (non-negotiable alongside #3):** this agent never gets read access to
     `verified_vibe_users` or any other table carrying member data — names, emails, chat transcripts,
     trust scores. Scoped to marketing/ad tables only, by construction of the granted role.
8. **Tech stack: Python (`uv`/`hatchling`), matching `job-hunt-agent`'s toolchain** — same conventions,
   one less thing to context-switch on. The CLI has no dependency on `pocket-dating-coach`'s TypeScript
   beyond calling its JSON endpoint over HTTP.
9. **Repo is private.** Targeting, budget figures, and creative strategy are business-sensitive.
10. **No Meta/Snap Marketing API credentials held by this agent, at all.** Research (modes 7/8) works
    from `pocket-dating-coach`'s exports plus the public Meta Ads Library / Snap ad search — never a
    direct, credentialed connection to either ad platform. This is what makes #3 structurally true
    rather than merely a policy: the agent has no credential that *could* touch a live account.
11. **The destination has an audience, and the gate that enforces it is hard.** `propose` refuses to
    write a record whose ad-set audience doesn't match the framing of its landing page, per
    `rules/destinations.yaml`. There is no override flag and `amend` cannot launder one — a blocked
    proposal is unblocked by building the page and registering it, never by a command-line escape
    hatch. Origin: the first live lead campaigns produced 98% male lead-form submissions and 100% male
    `/get` store taps, and `/get` is written in the second person to a man throughout.
12. **Creative asset library builds incrementally**, via `ad-intake`'s discoveries plus a one-time
    manual export of whatever's already running when this repo is stood up — no attempt to backfill
    everything from Ads Manager on day one.
13. **Ledger format: markdown + YAML front matter, one file per campaign, plus a generated index** — not
    a spreadsheet, not plain JSON. See "Ledger" below for the reasoning (the ledger has two readers,
    human and agent, and needs to serve both without a second source of truth to keep in sync).

## Non-negotiables (compliance — see `rules/compliance.md` for the full detail)

These come from the product's own marketing knowledge base, not from this repo's design process, and
they are load-bearing: the iOS build was actually rejected under App Store Guideline 1.1.4 for
"compensated dating" on 2026-08-03.

- Money, wealth, generosity, or provider-framing is never an attraction signal in ad copy. No lane may
  imply money, luxury, being kept, or a giver/receiver pair — even though "provider energy" is a real
  preference some women in the casual segment have, and the matching backend is allowed to weigh it as
  a real signal. **The backend may model it; the ad copy may never say it.** This is a distinction to
  preserve exactly, not a contradiction to paper over.
- No purchase language (no in-app purchases exist). No rupee amount for referral cash in-app. Never
  call the membership "high-earning" — "identity-verified and established professionals" is the
  approved phrasing.
- `pocket-dating-coach` has an automated banned-vocabulary gate that fails its build if this vocabulary
  reappears anywhere. `ad-setup-loop` must run finished ad copy through the same check (or the same
  wordlist, manually, until this repo has a way to call that gate directly) before a recommendation is
  considered ready — treat a hit as a decision for the app owner, never a copy edit to just make and
  move on.
- Never show a man's real, unenhanced photo in an ad. Label AI imagery. 18+ without exception.

## Non-negotiables (never automate a live account — see decision #3)

- Never call a Meta or Snap Ads Manager API to create, publish, enable, or change budget on anything
  live.
- Never hold Meta/Snap Marketing API credentials (decision #10) — there is no credential in this repo
  that could touch a live account even by accident.
- Never give this agent read access to member-data tables (decision #7's PII boundary).

## Architecture

```
Skill (live reasoning, in a Claude Code session)
  → does the actual research / targeting / creative work
  → persists through ad-agent's zero-API CLI (this repo)
       propose / amend / log-setup / log-review / abandon / stats / dump-ledger
  → pulls read-only data through ad-agent's zero-API CLI
       fetch-analytics  (channel 1: pocket-dating-coach's authenticated endpoint)
```

No server, no daemon, no cron in this repo for v1. Every mode is triggered by asking for it in a
Claude Code session rooted here (or in a session with this repo attached alongside
`pocket-dating-coach`). `ad-audit` is the only candidate for a future Claude Code scheduled task (see
decision #2), and only once trusted from repeated manual runs — same order job-hunt-agent proved out
with its `incubator-sweep`.

## Ledger

**Source of truth: `campaigns/<slug>/record.md`, one file per campaign recommendation.** Markdown with
a YAML front-matter block, updated in place as the record moves through its lifecycle, with a new
section appended to the body at each step. Chosen over plain JSON (fails "I have to read this too")
and over a spreadsheet (nothing to build around — no pre-existing habit like job-hunt's Career Hacking
Tracker, and `pocket-dating-coach` already owns the numeric ledger; this repo's ledger is decisions and
creative briefs, not metrics).

**`INDEX.md` at the repo root is generated, never hand-edited** — regenerated by every mutating CLI
command. It is the human's at-a-glance rollup (rec_id · network · status · campaign · ad set id ·
verdict · created); a spreadsheet export can be layered on top later (`ad-agent dump-ledger` prints the
same table to stdout for an ad hoc copy-paste) but the markdown files stay canonical.

Lifecycle:

```
proposed → executing → live → reviewed
    ↑ ↓           ↓
  amend       abandoned
```

- `ad-agent propose <slug> ...` — mode 5's output. Requires network, campaign/ad-set/ad names,
  targeting summary, a creative reference, a budget cap, a duration, and a brief file (the free-form
  reasoning). Generates a `rec_id`, writes `campaigns/<slug>/record.md`, status `proposed`.
- `ad-agent amend <rec_id> --reason ... [--ad-name ...] [...]` — revise a still-`proposed`
  recommendation before it is executed, appending an `## Amendment` section recording every
  field that moved. **Only `proposed` records may be amended**: once a record is `live` its fields
  describe what was actually built, and rewriting them would falsify the thing `ad-audit` joins a real
  outcome back to — a post-launch change is a `log-setup --deviated` note instead. Amending
  `ad_set_name` or `destination_url` re-runs the destination gate against the resulting pair, so
  `amend` cannot be used as the override flag the gate deliberately doesn't have.
- `ad-agent log-setup <rec_id> ...` — after you set the ad up by hand. Real campaign/ad-set/ad IDs,
  optional `--deviated` note for anything that changed from the brief. Status → `live`. The `ad_set_id`
  recorded here is deliberately the same join key `ad-analytics.ts` uses internally
  (`${network}:${adSetId}`), so `ad-audit` can look up real performance without you ever hand-attaching
  metrics.
- `ad-agent log-review <rec_id> --verdict working|not-working|inconclusive ...` — mode 6's write-back.
  Status → `reviewed`.
- `ad-agent abandon <rec_id> --reason ...` — for a proposal you decided not to execute. Without this,
  unexecuted proposals sit as `proposed` forever and pollute `stats`.

## Rules (single source of truth — read live, edited in place when refined)

Living under `rules/`, read by every skill rather than restated in the skill files — the same pattern
job-hunt-agent uses for `research.py`'s fit filter and `draft.py`'s `STYLE_RULES`: read the source, don't
improvise from memory, and if the user refines a rule mid-conversation, edit the rule file in the same
turn rather than applying the change once and letting it evaporate.

- `rules/compliance.md` — the hard, App-Store-enforced constraints. Never negotiable.
- `rules/targeting.md` — audience personas, age/gender bands, city priority, the provider-energy
  backend-vs-copy distinction.
- `rules/creative-style.md` — tone of voice, taglines, quotable first-party product stats, visual
  identity, objection handling.
- `rules/naming.md` — the campaign/ad-set/ad naming convention already in production use.
- `rules/budget.md` — the ₹50k/month operating budget, the test/exploit/retarget split, minimum viable
  daily spend, and the kill/double rule.

## Creatives

`creatives/` builds incrementally (decision #12) — see `creatives/README.md` for the naming convention
tying an asset to the `rec_id`/`ad_id` that used it.

## Open / deferred

- `fetch-analytics` is wired up but non-functional until the `pocket-dating-coach` PR adding
  `/api/internal/ad-analytics` + `ADS_AGENT_API_KEY` ships (decision #7, channel 1).
- The `ads_agent_ro` read-only Postgres role (decision #7, channel 2) — not created yet.
- A CSV/xlsx export of the ledger for ad hoc spreadsheet use — deferred until `dump-ledger`'s plain-text
  table proves insufficient.
- A Claude Code scheduled task for `ad-audit` — deferred until it's been run by hand enough times to
  trust unattended (decision #2).
- The eventual Claude Code plugin that "steers implementation" of `ad-setup-loop`'s output directly in
  Ads Manager — explicitly still bound by decision #3: it may tell the human what to click, never click
  it itself.
