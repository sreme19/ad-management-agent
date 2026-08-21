# Architecture and Decisions

The full canonical version of this page is `SPEC.md` in the repo root — this page is a navigable
summary of it. If the two ever disagree, `SPEC.md` is right.

## Problem this repo solves

Riteangle runs paid social campaigns on Snap and Meta to drive signups. Campaign setup, performance
research, and creative ideation were happening ad hoc, with no memory of what was recommended versus
what was actually run, and no single place encoding the targeting, creative, and compliance rules that
should govern every campaign. This repo is that place, run as a set of skills inside Claude Code
sessions rather than as a hosted service.

## The decisions that shape everything else

**No Anthropic API key, anywhere, ever.** Unlike `job-hunt-agent`, there is no API-calling reference
implementation planned for later — every mode here is a skill that reasons live in whatever session is
running it, and persists through this repo's CLI. The CLI never imports or calls an Anthropic client.

**Four skills, manual-trigger-only.** See [The Four Modes](The-Four-Modes). The audit mode is the one
candidate for an eventual Claude Code scheduled task, and only once it's been run by hand enough times
to trust unattended — the same order `job-hunt-agent`'s own incubator sweep moved from on-demand to
scheduled.

**The non-negotiable boundary.** This agent never calls a Meta or Snap Ads Manager API to create,
publish, enable, or change budget on anything live. This is stricter than `job-hunt-agent`'s "never
automate a send" rule, and for a sharper reason: money and audience reach are on the line here, not
just an account ban.

**Closing the loop is mandatory.** A recommendation with no record of what was actually set up is a
loose end forever — the audit mode cannot join a live outcome back to the reasoning that produced it
without the real ad-set ID on file. See [Ledger and CLI](Ledger-and-CLI).

**Every recommendation states a budget and duration cap.** A recommendation with no stated cost is
missing the thing a human would actually decide on.

**Confidence gating is inherited from `pocket-dating-coach`.** Any claim that a live ad set is or isn't
working respects the same minimum-sample floor (30 observations) the admin dashboard itself enforces.
Below that, the honest answer is "not enough data yet," not a guess dressed as a finding. The ideation
mode is allowed to reason more loosely, since it's proposing hypotheses to test, not reporting on data
that already exists.

**Data access is two channels, not one.** See [Data Access](Data-Access) for the full reasoning — the
short version is that this agent never re-derives `pocket-dating-coach`'s aggregation logic itself, and
never gets read access to member data.

**Tech stack: Python**, matching `job-hunt-agent`'s own toolchain, for one less thing to context-switch
on.

**The repo is private**, and no Meta/Snap Marketing API credentials are ever held by this agent — there
is no credential in this repo that could touch a live ad account even by accident.

**The creative library builds incrementally.** No attempt to backfill everything from Ads Manager on
day one.

**The ledger is markdown plus YAML front matter, one file per campaign, with a generated index.** Not a
spreadsheet, not plain JSON — see [Ledger and CLI](Ledger-and-CLI) for why.

## No server, no daemon

Every mode is triggered by asking for it in a Claude Code session. There is nothing running in the
background for v1.
