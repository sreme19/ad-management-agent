# The Four Modes

Each mode is a Claude Code skill under `.claude/skills/`. You don't invoke them by name — you just ask
for what you want in a session rooted in this repo, and the matching skill picks it up.

## ad-setup-loop — "set up an ad"

Recommends campaign, ad-set, and ad names, targeting, and creative for a new ad, following
[Rules Overview](Rules-Overview) exactly. Writes the recommendation to the ledger with
`ad-agent propose` before anything gets built in Ads Manager, then, once the ad is live, logs the real
IDs with `ad-agent log-setup` so the audit mode can find it later. Every output is a checklist a human
follows by hand — this skill never touches an Ads Manager account itself.

## ad-audit — "how are the ads doing"

Pulls live performance data via `ad-agent fetch-analytics`, joins it back to the ledger by ad-set ID,
and writes a `working` / `not-working` / `inconclusive` verdict against each live recommendation with
`ad-agent log-review`. Bound to the same minimum-sample floor `pocket-dating-coach`'s own dashboard
uses — a verdict on too little data is `inconclusive`, never a guess.

## ad-ideation — "find me some new ideas"

Deep research into what to try next — competitor creative, unused product stories, untested personas.
Every idea ends in a `recommend` or `hold` verdict with an estimated spend, the same way `job-hunt-agent`
gates every researched company on a `fit`/`risk` verdict. An approved idea hands off straight to
ad-setup-loop.

## ad-intake — "I found this ad, what do you think"

You paste or describe an ad you found elsewhere — a screenshot, a competitor's Meta or Snap ad, a link.
The skill reads it directly (vision, no OCR step needed), says specifically what it's doing well or
poorly, checks it against the compliance rules before drawing any lesson from it, and can turn it into
an idea for ad-setup-loop if it's worth pursuing. Direct analog of `job-hunt-agent`'s
`linkedin-opportunity` skill.

## How they connect

```
ad-ideation  ──┐
               ├──► (approved idea) ──► ad-setup-loop ──► (live ad, real IDs logged)
ad-intake    ──┘                                               │
                                                                ▼
                                                            ad-audit
                                                     (verdict written back to
                                                      the same ledger record)
```
