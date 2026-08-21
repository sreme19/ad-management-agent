# ad-management-agent

A loop-engineered, harness-driven ad-operations agent for Riteangle (the product; the consumer-facing
codebase is `pocket-dating-coach`). It runs entirely inside Claude Code sessions — **no Anthropic API
key exists anywhere in this repo.** The actual reasoning (targeting, creative, research) happens live
in whichever Claude Code session is running one of the four modes below; this repo's own code only
persists results deterministically, through a small zero-API command-line tool.

Built in the same spirit as this account's other agent, [job-hunt-agent](https://github.com/sreme19/job-hunt-agent) — same philosophy (do the
thinking live, in a paid-for chat session; only give a CLI to the parts that are pure, deterministic
file reads and writes), applied to running paid social campaigns instead of a job search.

## Start here

- **[Architecture and Decisions](Architecture-and-Decisions)** — why this repo is shaped the way it
  is, and every locked design decision behind it.
- **[The Four Modes](The-Four-Modes)** — what each skill does and when to invoke it.
- **[Rules Overview](Rules-Overview)** — where the targeting, creative, compliance, naming, and budget
  rules actually live, and how they're meant to be used.
- **[Ledger and CLI](Ledger-and-CLI)** — the `ad-agent` command reference and the campaign-record
  lifecycle.
- **[Data Access](Data-Access)** — how this agent reads `pocket-dating-coach`'s analytics, and what's
  not wired up yet.
- **[Working Across Laptop, Sandbox, and GitHub](Working-Across-Laptop-Sandbox-and-GitHub)** — how
  this repo stays in sync across the three places it lives.
- **[Open Work](Open-Work)** — what's still outstanding, and where.

## The one sentence version

You ask a Claude Code session rooted in this repo to set up an ad, audit how the live ads are doing,
find new ideas, or learn from an ad you found somewhere else; the session does the actual thinking and
writes the result to a plain-text ledger that never touches a live Ads Manager account.

## The one rule that never changes

This agent never calls a Meta or Snap Ads Manager API to create, publish, enable, or change budget on
anything live. Every recommendation it produces is instructions a human executes by hand. That stays
true even if a future Claude plugin exists to "steer" the setup process — steering means telling the
human what to click, never clicking it.
