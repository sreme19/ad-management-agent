# Glossary

Plain-language definitions for terms used across these pages.

**Riteangle**
The product name used in this system's marketing and rules. The codebase and internal identifiers say
`verified_vibe_*`, and the consumer-facing site is `pocket-dating-coach` — all three names refer to the
same product.

**The ledger**
`campaigns/<slug>/record.md` — one markdown file per campaign recommendation, with a YAML front-matter
block plus a body that grows a new section at every lifecycle stage. See [The ledger](The-ledger).

**`rec_id`**
The unique identifier generated for a recommendation the moment `ad-agent propose` runs (e.g.
`rec-2026-08-21-casual-selective`). Every later command — `log-setup`, `log-review`, `abandon` —
targets a record by this id.

**Lifecycle / status**
The stage a ledger record is currently in: `proposed` → `executing` → `live` → `reviewed`, with
`abandoned` as a side-exit from `proposed`. See [The ledger](The-ledger).

**The four modes**
`ad-setup-loop` (mode 5, recommend a new ad), `ad-audit` (mode 6, check real performance),
`ad-ideation` (mode 7, research what to try next), `ad-intake` (mode 8, learn from an ad found
elsewhere). See [How the four modes work](How-the-four-modes-work).

**Persona**
One of four named audience segments in `rules/targeting.md` — The Invisible Man, The Flooded Woman,
The Second-Chapter Person, The Casual but Selective Woman — picked one per ad set, never a generic
"everyone" audience.

**Provider-energy distinction**
The rule that the matching *backend* may model "provider energy" (being well-networked, financially
capable) as a real preference some women in the casual segment have, but the ad *copy* may never say,
imply, or visually signal it. See [The rules](The-rules) and `rules/compliance.md` rule #1.

**`recommend` / `hold`**
The verdict every `ad-ideation` or `ad-intake` idea ends in — `recommend` means it's ready to feed
`ad-setup-loop`; `hold` means not yet, with a stated reason for what would need to be true to change
that. Mirrors `job-hunt-agent`'s `fit`/`risk` gate.

**`working` / `not-working` / `inconclusive`**
The verdict `ad-audit` writes back to a `live` ledger record. `inconclusive` means the sample size
hasn't cleared `MIN_SAMPLE = 30` yet — a real finding, not a non-answer.

**`MIN_SAMPLE = 30`**
The minimum sample size `pocket-dating-coach`'s own admin dashboard requires before treating a rate as
meaningful. `ad-audit` inherits this floor exactly rather than defining its own.

**Kill/double rule**
Pause a losing ad set after 3–5 days or 50–100 events, whichever comes first, and move its budget to
whatever's winning. See `rules/budget.md`.

**Deviated**
The optional note recorded at `log-setup` time describing anything that changed from the original brief
when an ad was actually set up by hand — read by `ad-audit` before judging performance, since a change
at setup time changes what's actually being evaluated.

**Channel 1 / Channel 2**
The two separate paths into `pocket-dating-coach`'s data — an authenticated analytics endpoint
(Channel 1, for anything already a computed metric) and a least-privilege read-only database role
(Channel 2, for raw/exploratory lookups only). See [Data access](Data-access).

**`ads_agent_ro`**
The (not-yet-created) least-privilege Postgres role scoped to six marketing/spend tables only — never
member data. Channel 2 above.

**`ADS_AGENT_API_KEY`**
The bearer token `pocket-dating-coach`'s `/api/internal/ad-analytics` endpoint will check once it
ships, instead of the admin session cookie. Set as a `pdc.api_key` value in this repo's
`config.local.yaml`.

**`config.local.yaml`**
The gitignored file holding real secrets (the analytics API key, the read-only database connection
string) — never committed, never synced to a sandbox through GitHub. See
[Working across machines](Working-across-machines).

**Creative reference (`creative-ref`)**
A path or id under `creatives/` naming which asset a recommendation uses, passed to
`ad-agent propose --creative-ref`.

**`INDEX.md`**
The generated, at-a-glance rollup of every ledger record at the repo root. Never hand-edited — every
mutating `ad-agent` command regenerates it from scratch.

**Learning**
One claim, in one file under `research/learnings/`, carrying where it came from (`source`) and how
sure we are (`confidence`). Evidence and hypotheses only — a learning never constrains anything. See
[The research loop](The-research-loop).

**Note (research)**
Raw material someone brought in, stored **verbatim and never edited**, under `research/notes/`. The
content is the provenance a learning points back at, which is why it cannot be rewritten. Not the same
thing as `ad-agent note`, which appends a dated line to a *ledger record* while a campaign is running.

**Source kind**
Where a claim came from: `live-data`, `platform-doc`, `source-code`, `own-research`,
`competitor-observation`, `intuition`. Only the first three may be marked `high` confidence —
everything else is a hypothesis, however plausible.

**`MIN_SAMPLE`**
The floor of 30, inherited from `pocket-dating-coach`'s own `ad-analytics.ts`. Below it, a claim about
live performance is `inconclusive`, never a finding. Applies to `ad-audit`'s verdicts and to any
`live-data` learning.

**Back-edge**
The step where a campaign's verdict travels back to the belief that produced the recommendation and
marks it supported, contradicted or mixed — and onto the creative's `prompts.md`. Run automatically by
`ad-agent log-review`. Without it the research library only grows and never corrects itself.

**Idea**
A proposal-shaped hypothesis under `ideas/`, carrying a `recommend`/`hold` verdict and the spend it
would take to test. A `hold` must state what would change the verdict, or it is indistinguishable from
a no.

**Promotion**
A human deciding a learning is reliable enough to become a rule, editing the relevant `rules/` file and
recording it with `ad-agent promote`. The only route by which research becomes binding.

**Loose end**
Anything the loop started and did not finish: a proposal never executed, a live ad set past its review
window, a note nobody derived anything from, a recommended idea nobody proposed. `ad-agent open` lists
them all, derived fresh every run.
