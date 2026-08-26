---
name: ad-research
description: Run a research pass for Riteangle's ad operations — work an open question, ingest notes the user brings in, and derive durable learnings into research/. Use whenever the user brings research notes to add, asks what's still unanswered, wants an open question worked, or asks what we actually know about an audience, channel, creative format or tracking behaviour.
---

# Running a research pass (mode 9)

This skill fills the library the other four modes read from. It does not propose campaigns
(`ad-ideation`), read one ad (`ad-intake`), or judge live performance (`ad-audit`) — it answers
questions and writes down what is now known.

Everything it writes lands in `research/` or, for a hypothesis with a price on it, `ideas/`.
**Nothing it writes constrains anything.** `rules/` is normative; research is evidence. A claim becomes
binding only when a human promotes it into a rules file. Read `research/README.md` once before working
here.

## Start from the queue

```
ad-agent open
```

A pass that starts from "go research women's ads" wanders. A pass that starts from an open question
converges and terminates. The queue is filled by every other mode — an `inconclusive` audit verdict, an
idea held pending research, an intake raising a why-does-this-work.

`open` also shows what is rotting: learnings past their `review_after` date, learnings never tested
against a real outcome, notes nobody derived anything from. Any of those is a legitimate pass.

## The two ways material arrives

**The user brings notes.** Snapshot them before deriving anything:

```
ad-agent ingest --title "..." --source own-research|competitor-observation|platform-doc|source-code \
  (--file /path/to/notes.md | --text "...") [--slug short-id]
```

Notes are immutable and a repeat ingest is refused — the content *is* the provenance a claim points
back at, and a note that could be rewritten proves nothing about the claim citing it. If the material
is a conversation, a screenshot, or a page you read, write down what was actually there rather than
your summary of it; the note is what someone reads in three months.

**You research it live.** Web search, the Meta Ads Library, Snap's public ad search, Google's Ads
Transparency Center, `pocket-dating-coach`'s own source. Snapshot what you found the same way — a
learning whose evidence is "I looked it up" is not checkable later.

## Deriving a learning

```
ad-agent learn --claim "..." \
  --subject audience|creative|channel|tracking|competitor|product|budget \
  --source live-data|platform-doc|source-code|own-research|competitor-observation|intuition \
  --confidence high|medium|low [--sample-n <n>] --evidence "..." \
  [--derived-from <note-id>] [--answers <q-id>] [--slug short-id]
```

**One claim per atom.** If you find yourself writing "and also" in a claim, that is two learnings.

**The confidence gate will refuse you, and that is the feature.** Only `live-data`, `platform-doc` and
`source-code` may be `high`. Your own reading, a competitor observation and an informed hunch cap at
`medium` however convincing they feel — a test earns the upgrade. A `live-data` claim must state
`--sample-n` and can only be `low` below `MIN_SAMPLE = 30`, the same floor
`pocket-dating-coach`'s dashboard applies to itself.

**Do not pick the source kind that unlocks the confidence you want.** The gate only means anything if
the kind is the truthful one. If a claim is a hunch that feels certain, it is `intuition`/`medium`.

**`learn` prints existing learnings on the same subject. Read them.** If this restates one, that is
`ad-agent log-evidence <lrn-id> --outcome supported --text "..."` on the original — two files making
the same claim is how a library loses the ability to say what it believes.

## Closing questions, and raising new ones

```
ad-agent answer <q-id> --text "..." [--learning <lrn-id>] [--dropped]
ad-agent question --text "..." --kind ... --why "what decision it unblocks" [--raised-by <id>]
```

Answering with `--learning` (or `learn --answers <q-id>`) links the question to what it produced.
`--dropped` closes one that is no longer worth answering — a different and honest outcome.

**A pass that raises more questions than it closes is not a failed pass.** Say so plainly rather than
padding the answer to look conclusive.

## When the answer changes something we already believed

```
ad-agent log-evidence <lrn-id> --outcome supported|contradicted|inconclusive --text "..."
ad-agent reclassify <lrn-id> --reason "..." [--source ...] [--confidence ...]
ad-agent retire <lrn-id> --reason "..."
```

`reclassify` corrects how a claim was *filed* — wrong subject, wrong source kind, wrong confidence. It
cannot change the claim text, because evidence already attached was gathered against the claim as
written. A claim that turned out to be the wrong claim is `retire` plus a new atom.

## Promotion is a human decision

If a learning is reliable enough to become binding, **say so and let the user decide** — don't promote
it yourself. When they agree: edit the relevant `rules/` file to carry the claim, then record it:

```
ad-agent promote <lrn-id> --rule rules/targeting.md
```

The command records the graduation; the rule file is what skills actually obey. A promoted claim later
contradicted is the worst state in the system, and `ad-agent open` reports it first.

## What this skill never does

- **Never writes to `rules/` on its own initiative.** The precedence runs one way.
- **Never records a competitor observation or a hunch as `high` confidence** to make an idea look
  better supported than it is.
- **Never derives a claim from a note that does not exist.** If the material is in the session and not
  in `research/notes/`, ingest it first.
- **Never leaves a pass unwritten.** Reasoning that stays in the session is exactly the hole this whole
  store was built to close — if it was worth working out, it is worth one `learn` or one `question`.
