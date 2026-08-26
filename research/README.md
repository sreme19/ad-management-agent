# research/ — evidence and hypotheses, never constraints

This directory is **not** `rules/`, and the difference is the whole point.

`rules/` is **normative**. A skill reads it and obeys it. `rules/compliance.md` is not a
well-supported opinion about App Store guidelines; it is the thing that stops an ad shipping.

What lives here is **evidence**: dated, sourced, revisable, and sometimes contradicted by the next
thing that arrives. A learning is a claim about the world with a confidence attached. A question is
something nobody knows yet. An idea is a hypothesis with a price on it.

**Precedence is one-directional and absolute: `rules/` wins.** Nothing in this directory constrains
anything. A skill that finds a learning disagreeing with a rule follows the rule and raises a
question. The only way a claim here becomes binding is a human promoting it into a rules file — an
edit and a decision, recorded afterwards with `ad-agent promote`, never a status change on its own.

## Why it exists as its own store

`rules/targeting.md` already carries inline parentheticals like *"the Aug 9 note records that
hard-hitting, feminist-coded copy tests well in this band."* The live women's record cites that note
as part of the justification for a ₹5,000 spend. There is no way to find out whether it came from a
measured result, a competitor screenshot, or a hunch — because a normative file had an observation
dropped into it with no source and no date.

Every atom here carries where it came from, so that can't happen again.

## The four stores

| | what it holds |
|---|---|
| `research/notes/` | what someone actually brought in, **verbatim and immutable** |
| `research/learnings/` | one claim per file, with its source kind and confidence |
| `research/questions/` | the open-question queue |
| `../ideas/` | proposal-shaped hypotheses, each with a verdict and a stated spend |

Notes are immutable on purpose. The content *is* the provenance — if it could be rewritten, a claim
pointing back at it would prove nothing.

## Confidence is gated, not self-declared

`--confidence high` is refused unless the source is `live-data`, `platform-doc`, or `source-code`.
Everything else — your own reading, a competitor observation, an informed hunch — caps at `medium`,
however plausible. A test earns the upgrade.

`source-code` is for a fact read directly out of a codebase, ours or `pocket-dating-coach`'s. It was
added the day the audience-classification break forced a statement about what `audienceOf()` *does* —
verifiable by reading the function — to be filed alongside hunches as `own-research`/`medium`. Reading
code is as certain as reading a doc. What it is **not** is durable: it describes something someone is
actively changing, and one commit can invalidate it, so it carries high confidence on a 60-day clock.
That pairing is deliberate, not a contradiction.

A `live-data` claim must state `--sample-n`, and below `MIN_SAMPLE = 30` it can only be `low`. That
is SPEC.md decision #6, inherited from `pocket-dating-coach`'s own `ad-analytics.ts`, applied here so
a brief cannot lean on a number the dashboard itself would call inconclusive.

## The loop closes, or it isn't a loop

```
question ──→ research ──→ note ──→ learning ──→ idea ──→ propose ──→ live ──→ verdict
    ↑                                  ↑                                          │
    └───── raised by any stage ────────┴───────── log-evidence ───────────────────┘
```

`log-evidence` is the back-edge, and it is the part that matters most. Without it the library only
ever grows and never corrects itself — and a store that confidently records wrong things is worse
than no store at all.

**You rarely run it by hand.** `ad-agent log-review` walks `record → idea → learnings` and applies the
verdict to every claim the recommendation rested on: `working` supports, `not-working` contradicts,
and `inconclusive` records the evidence without moving the belief. Run `log-evidence` yourself for a
record with no idea behind it, or when a result bears on a claim the chain doesn't know about —
`log-review --learning <id>` does the same thing inline.

One caution, since the propagation is automatic: **an idea should cite only the learnings its test
actually bears on.** Every one it lists receives the verdict, so a claim the campaign never varied
will be marked on evidence it did not produce. Nothing is lost when that happens — evidence is
append-only and names the record — but the fix is a narrower `--learning` list when the idea is
written, not a correction afterwards.

## Staleness

Claims rot at different speeds, so each carries a `review_after` date set from its source: source-code
and competitor observations 60 days, hunches 90, own research and live data 120, platform docs 180.
`ad-agent open` lists what is past due. A claim nobody has reconfirmed is not automatically wrong —
it is unverified, which is a different thing, and the report says so.

## Fixing a mis-filed claim

`ad-agent reclassify <id> --reason "..."` corrects a learning's `subject`, `source`, `confidence` or
`sample_n`. It runs the same confidence gate `learn` does — so it cannot be used to get around the
ceiling — appends a dated `## Reclassified` section recording what moved, and recomputes the review
clock from `last_confirmed` rather than today, because re-filing something is not reconfirming it.

**The claim text itself is deliberately not changeable.** Evidence already attached was gathered
against the claim as written, and letting the wording move underneath it would make the whole trail
lie. A claim that turned out to be the wrong claim is `retire` plus a new atom, not an edit.

## Reading it

`ad-agent open` surfaces everything outstanding: unanswered questions, notes nobody derived anything
from, learnings past review, learnings never tested, recommended ideas nobody proposed, and the worst
state in the system — a claim that was promoted into `rules/` and has since been contradicted.
