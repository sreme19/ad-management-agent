# ad-management-agent — Spec

**Status: v1 scaffold.** Ledger CLI (`propose` / `amend` / `note` / `log-setup` / `log-review` /
`abandon` / `stats` / `dump-ledger` / `open` / `commands` / `fetch-analytics` / `snap-push`) and four
skills are built. `fetch-analytics` cannot do anything
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
2. **Five skills, manual-trigger-only.** `ad-research` (mode 9) was added 2026-08-26 alongside the
   research store — modes 7 and 8 had no write path at all until then, which is the hole it closes:
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
   - `ad-research` — mode 9: work an open question from the queue, ingest notes brought in by hand, and
     derive durable learnings into `research/`. The mode that fills the library the other four read
     from. See "Research" below for the precedence rule against `rules/`.
3. **The boundary, as amended 2026-08-26 (Snap) and 2026-08-27 (Meta).** Originally: this agent never
   calls a Meta or Snap Ads Manager API at all, and every `ad-setup-loop` output is instructions a
   human executes by hand. **The app owner lifted that for Snap on 2026-08-26**, explicitly and after
   the trade-off was put to them, so that setup could be automated. **On 2026-08-27 the app owner
   extended the same permission to Meta**, in as many words, after a readiness probe of the live Meta
   account. The rules below are written per-network only where the networks actually differ; the
   paused-only discipline is identical on both. What stands now:

   - The agent **may create** campaigns, ad squads, creatives and ads on Snap, through
     `ad-agent snap-push`, and **only ever with status `PAUSED`**.
   - The agent **never enables anything, and never changes the budget of anything live.** There is no
     enable, resume or activate call anywhere in `snap.py`, and none is to be added without the app
     owner saying so in as many words. Starting spend stays a human action in Ads Manager.
   - Every created object is **read back from the API and diffed** against the plan before the command
     exits. A 200 from a POST is not evidence that an ad squad targets who you think it targets.
   - The agent **reads the parent campaign's own spend caps before creating an ad squad under it**, and
     refuses when a cap would bind. A campaign-level daily or lifetime cap silently overrides a larger
     ad-squad budget — the lower figure wins. `WOMEN_18-22_CASUAL_LPV` was pushed on 2026-08-26 with an
     ad squad at ₹1,000/day under a campaign capped at ₹300/day, putting the live test below
     `rules/budget.md`'s floor and making its read inconclusive before a rupee was spent; nothing in the
     push looked at the parent, so nothing caught it. Unlike the destination gate this one has an
     escape hatch (`--accept-campaign-cap`), because a low cap is sometimes deliberate — but it names
     the deviation and prints the `note` command to record it, and never proceeds quietly. The observed
     caps are written onto the record, so `open` can tell a funded ad set from a starved one.

   - The paused-only rule is **enforced at the transport layer, not asserted in a comment.**
     `SnapClient._call` inspects every outbound payload — at every nesting depth, because Snap wraps
     each object in a list under a plural key — and raises `SnapSafetyError` on any enabling status
     value, or on any budget field in a `PUT`. Creation carrying a budget stays allowed; changing one
     on an object that already exists does not. There is no override flag.

   **Be clear about what was lost.** The old rule was enforced by decision #10 — the agent held no
   credential that could reach a live account, so "never touches a live account" was true by
   construction. That is now true only because this code is careful. It is a weaker kind of guarantee,
   and the paused-only rule above is what carries the weight instead. Putting the check at the single
   choke point every request passes through is what "careful" has to mean to be worth anything: a
   method added later cannot skip a check it never knew about, and `tests/test_snap_safety.py` asserts
   a refused request never reaches the network.

   **The Meta extension (2026-08-27) inherits that reasoning rather than restating it.** A Meta client
   is only permitted on the same terms: creation `PAUSED` only, no enable/resume/activate call in the
   module at all, no budget change to anything that already exists, read-back-and-diff after every
   create, and the refusal enforced at the single transport choke point rather than asserted per
   method. A Meta client that does not carry its own equivalent of `SnapClient._call`'s check is not
   permitted by this decision — the permission is to build that shape, not to reach the API by any
   means. What is written above about the guarantee being weaker now applies twice over, because
   there will be two live accounts reachable from this repo instead of one.
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
10. **Credentials, as amended 2026-08-26 (Snap) and 2026-08-27 (Meta).** Originally: no Meta or Snap Marketing API credentials in
    this repo at all, which is what made #3 structurally true rather than merely a policy. **Amended
    for Snap only, by the app owner, on the same call as #3.** `config.local.yaml` (gitignored) now
    holds a Snap OAuth client id, client secret and refresh token for the `riteangle-marketing-api`
    app, scoped `snapchat-marketing-api`.

    **Amended for Meta too, by the app owner, on 2026-08-27.** `config.local.yaml` may now also hold
    Meta Marketing API credentials for the `riteangle` app (App ID `1020330197292995`, owned by the
    `Equal Dating App` business portfolio, ID `1587705756249660`). The agreed shape is a **system-user
    token**, not a user token: the system user `riteangle-api` (ID `61593371450505`) is portfolio-owned
    and its token does not expire, where a long-lived user token lasts ~60 days and Meta offers no
    refresh-token equivalent — it would expire mid-campaign, silently.

    That route requires claiming the previously personal ad account `1561367575690055` into the
    portfolio, because a system user can only ever be assigned portfolio-owned assets — which is why
    `riteangle-api` currently sits with zero assets. Meta treats the claim as effectively one-way, and
    the portfolio's ad-account creation limit is 1. That cost was put to the app owner and the route was
    chosen on 2026-08-27. **The claim itself, the asset assignment, and the token generation are manual
    steps and were not complete when this was written** — so the credential block does not exist yet.
    Anything reading this decision should verify `config.local.yaml` rather than assume.

    Snap's access tokens are minted per run from the refresh token and never written to disk. Meta's
    system-user token has no refresh step, so it is read from `config.local.yaml` per run and likewise
    never copied elsewhere. As with the Snap client secret, Meta shows a generated system-user token
    **once** — there is no regenerate.

    Research for modes 7/8 continues to work from `pocket-dating-coach`'s exports plus the public Meta
    Ads Library and Snap ad search; nothing about this amendment requires research to authenticate.
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

- **Never enable anything, and never change the budget of anything already live**, on either network.
  Creation is permitted on Snap (amended 2026-08-26) and on Meta (amended 2026-08-27), and only ever
  `PAUSED`; starting spend is a human action, every time. This is now the whole of the boundary — there
  is no longer a network this agent is barred from touching, so it is the only line left.
- **Never add an enable, resume or activate call to a network client**, on either network, without the
  app owner saying so in as many words. Pausing is permitted (it can only stop spend); the asymmetry is
  deliberate — see `snap.py.pause_campaign`.
- Never leave Meta's **ads MCP server** channel enabled for an ad account this repo drives directly
  (Business settings → ads MCP server → "Actions allowed"). Two independent write paths into one live
  ad account, one of them outside this repo's guards, is the failure decision #3 exists to prevent.
- Never give this agent read access to member-data tables (decision #7's PII boundary).

## Architecture

```
Skill (live reasoning, in a Claude Code session)
  → does the actual research / targeting / creative work
  → persists through ad-agent's zero-API CLI (this repo)
       propose / amend / note / log-setup / log-review / abandon / stats / dump-ledger
  → optionally creates the ad set on Snap, PAUSED, and diffs it back
       snap-push   (decision #3 as amended — creates, never enables)
  → pulls read-only data through ad-agent's zero-API CLI
       fetch-analytics  (channel 1: pocket-dating-coach's authenticated endpoint)

The research loop persists the same way, through its own stores:
       ingest / learn / log-evidence / promote / retire   research/notes, research/learnings
       question / answer                                  research/questions
       idea  (+ propose --from-idea)                      ideas/

Two commands serve the human rather than a skill:
       open       every loose end the ledger can see — the "where was I" entry point
       commands   regenerates the command list in README.md and the wiki cheatsheet
```

**`open` is the entry point, and it is deliberately derived.** It holds no state: proposals never
executed, live ad sets past their kill/double window, creative that cleared QA and was never used,
funding below `rules/budget.md`'s floor — all computed from the records on every run, so it cannot go
stale the way a hand-kept TODO would. It also names the loops it *cannot* see yet, so an empty report
is never mistaken for a finished loop.

**`commands` exists because the documentation failed.** On 2026-08-26 both `README.md` and the wiki
cheatsheet still asserted that this agent never calls a Snap API, hours after `snap-push` had created a
live ad set through one, and neither listed `snap-push` at all — three hand-maintained copies of one
list, none of them right. The list is now generated from the argparse parser; the prose around each
command stays hand-written, and `commands --check` fails if a command has no prose section.

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

  note — appended at any status, never rewrites
```

- `ad-agent propose <slug> ...` — mode 5's output. Requires network, campaign/ad-set/ad names,
  targeting summary, a creative reference, a budget cap, a duration, and a brief file (the free-form
  reasoning). Generates a `rec_id`, writes `campaigns/<slug>/record.md`, status `proposed`.

  **A record carries its audience twice, and both are required.** `targeting_summary` is prose — the
  reasoning, which is what a human reads and what `ad-audit` quotes back. `targeting` is a normalized
  block (`gender`, `min_age`, `max_age`, `countries`, `os`, `expansion`, `regulated_content`) and it is
  what `snap-push` actually pushes. Prose cannot be pushed; a machine-readable block cannot explain
  itself. Before this existed, `snap-push` compensated with a hardcoded audience, which meant the
  second record ever pushed would have been created carrying the *first* one's targeting — and would
  have diffed clean, because the read-back was compared against the same hardcoded dict rather than
  against the brief. The diff is now derived from the record's own spec (`targeting.py`), which is the
  whole point: a read-back checked against a literal only validates the code against itself.

  Two validations refuse a proposal outright: `min_age` below 18 (`rules/compliance.md` is 18+ without
  exception, and Snap's dating category enforces the same floor independently), and a targeting block
  that disagrees with the gender token in its own ad-set name — one of the two is wrong and which one
  cannot be guessed.
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
- `ad-agent note <rec_id> --kind budget|targeting|creative|incident|observation --text ...` — an
  append-only, dated note, allowed at any status. The lifecycle otherwise has no home for something
  that happens *during* a run: `amend` refuses a live record on purpose, `log-setup` fires once, and
  `log-review` is the end. Without this, a budget raised on day three leaves no trace and the verdict
  gets judged against conditions that quietly moved. Notes never rewrite anything.
- `ad-agent log-review <rec_id> --verdict working|not-working|inconclusive ...` — mode 6's write-back.
  Status → `reviewed`. **Only a `live` (or `executing`) record may be reviewed**; a proposal has no
  outcome to judge and a reviewed record already has its verdict.

  **This is the loop's closing edge, and it writes to three places.** Besides the record: the
  creative's `prompts.md` gets an `## Outcome` section with the audience and the *effective* daily
  spend (`rules/creative-generation.md` §9 — a prompt with no outcome attached taught nothing, and a
  ranked prompt library is the point of keeping the exact text); and every learning the
  recommendation rested on, reached along `record → idea → learnings`, gets dated evidence via
  `log_evidence`. `inconclusive` records the evidence without moving the belief, because a campaign
  can be unreadable for reasons that say nothing about the claim.

  Both were previously mandated in prose and enforced nowhere. A mandated manual step with no
  enforcement is a step that stops happening around run four, which is why this is a code path rather
  than a line in a skill file. There is no flag to turn it off; `--learning` only adds.
- `ad-agent abandon <rec_id> --reason ...` — for a proposal you decided not to execute. Without this,
  unexecuted proposals sit as `proposed` forever and pollute `stats`.

## Research (evidence and hypotheses — never constraints)

**Added 2026-08-26, closing the hole that modes 7 and 8 had no write path at all.** `ad-ideation` and
`ad-intake` did their reasoning in a session and produced prose that died with it — the only two modes
in the repo with no persistence, which is why `rules/targeting.md` ended up carrying inline dated
observations with no source, and why the live women's record cites "the Aug 9 note" to justify ₹5,000
of spend with no way to check whether it came from a test, a screenshot, or a hunch.

`research/` (notes, learnings, questions) and `ideas/` are that write path. **Precedence over `rules/`
is one-directional and absolute: rules win.** Nothing under `research/` constrains anything; a skill
finding a learning that disagrees with a rule follows the rule and raises a question. Promotion into a
rules file is a human decision, recorded afterwards with `ad-agent promote`, never a status change on
its own. See `research/README.md`.

Four properties are load-bearing:

- **Notes are immutable.** The content *is* the provenance; a claim pointing back at a note that could
  have been rewritten proves nothing.
- **Confidence is gated, not self-declared.** Only `live-data`, `platform-doc` and `source-code` may
  be `high`; everything else caps at `medium`. A `live-data` claim must state its sample size and can
  only be `low` below `MIN_SAMPLE = 30` — decision #6, applied so a brief cannot lean on a number the
  dashboard itself would call inconclusive. `ad-agent reclassify` corrects a mis-filing and runs the
  same gate, so it is not a way around the ceiling; it cannot change the claim text, because evidence
  already attached was gathered against the claim as written.
- **The back-edge is a command, not a habit.** `log-evidence` puts a campaign's verdict onto the
  learning that spawned the recommendation. Disagreeing outcomes produce `mixed`, not whichever
  arrived last.
- **Claims go stale on a clock set by their source** — competitor observations 60 days, hunches 90,
  own research and live data 120, platform docs 180. `open` reports what is past due, and reports a
  stale claim as unverified rather than as wrong.

## Networks (registry — the second rule file the CLI reads directly)

**Added 2026-08-26, before any new platform rather than after one.** `snap` and `meta` were a
two-value enum hardcoded in four argparse calls, plus a `utm_source: "snapchat"` string literal inside
a Snap-only function. A network is not a string: it is a UTM convention, a join key, an analytics
label, and a statement about whether this agent may create anything on it — and two of those already
differ between the two networks in ways that have caused real bugs. Snap's analytics key is `snap`
while its `utm_source` is `snapchat`, which is why only 7 of 151 signups could be joined to a costed
ad set; and `traffic-quality.ts` reads `utm_id` as the ad id on Snap but `utm_content` on Meta.

Adding a network is now an entry in `rules/networks.yaml` plus a client module, not a scatter of new
string literals. The file leads with the reason not to add one: `rules/budget.md`'s ₹800–1,200/day
floor against a ₹50,000/month envelope funds one or two properly funded ad sets at a time, so a new
network splits the same money below the floor rather than adding reach — and it has to be taught to
`pocket-dating-coach` too, or its spend cannot join to its traffic.

**The `creation` field can only ever refuse.** `networks.require_creation` is called *in addition to*
a command's own hardcoded network check, never instead of it. Flipping `meta` to `paused-only` in the
yaml grants nothing on its own: `snap-push` still refuses a non-`snap` record before it consults the
registry. The registry declares intent and can tighten; the client modules' transport-layer refusals
are what hold. `tests/test_networks.py` asserts both directions.

**`meta.creation` stays `none` until a Meta client actually exists.** Decision #3 was extended to Meta
on 2026-08-27, so the *permission* is granted — but permission is not capability, and the registry
describes what the code can do, not what the app owner has agreed to. Flipping the field the moment
the decision changed would delete a live refusal and put nothing behind it, and would leave a future
session reading `paused-only` and reasonably concluding a push path exists.

The flip belongs with the **push path**, meaning the client *and* a CLI command that calls it — not
with the client alone. `meta.py` and its safety tests landed on 2026-08-27 and the registry
deliberately did not move, because a client no command invokes is not yet a way to create anything,
and `paused-only` would have been describing a capability that still had no entry point.
`test_require_creation_refuses_meta` is what holds that ordering in place — when it is changed, it
should be changed to assert the new direction, never simply deleted.

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
- `rules/funnel.md` — the funnel as a three-axis matrix (format x capture point x follow-up channel)
  rather than the one path currently running, plus the friction ladder that orders the untried cells by
  what each actually costs to build. Added 2026-08-27 from a standing operator instruction; it widens
  what `ad-ideation` may propose without widening what may ship.

## Creatives

`creatives/` builds incrementally (decision #12) — see `creatives/README.md` for the naming convention
tying an asset to the `rec_id`/`ad_id` that used it.

## Open / deferred

- `fetch-analytics` is wired up but non-functional until the `pocket-dating-coach` PR adding
  `/api/internal/ad-analytics` + `ADS_AGENT_API_KEY` ships (decision #7, channel 1).
- The `ads_agent_ro` read-only Postgres role (decision #7, channel 2) — not created yet.
- A CSV/xlsx export of the ledger for ad hoc spreadsheet use — deferred until `dump-ledger`'s plain-text
  table proves insufficient.
- ~~CI~~ — **done 2026-08-26**, `.github/workflows/checks.yml`. Runs `commands --check`, a staleness
  check on the generated command list, `pytest`, and `ruff` on push and PR. Ordered by what has
  actually gone wrong here rather than by convention: documentation drift is the failure with a real
  incident behind it, so it runs first. `src/` and `tests/` are now lint-clean, with one documented
  `noqa` — `date.today()` is deliberate, because every date this repo writes is an IST business date
  read alongside analytics that bucket by IST day.
- A Claude Code scheduled task for `ad-audit` — deferred until it's been run by hand enough times to
  trust unattended (decision #2).
- The eventual Claude Code plugin that "steers implementation" of `ad-setup-loop`'s output directly in
  Ads Manager — explicitly still bound by decision #3: it may tell the human what to click, never click
  it itself.
