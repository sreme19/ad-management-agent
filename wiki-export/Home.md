# ad-management-agent

**A private system that runs ad operations for Riteangle** (the product; the codebase and internal
identifiers say `verified_vibe_*`, and the consumer-facing site is `pocket-dating-coach`). It is not a
bot that touches Ads Manager — it recommends what to set up, researches what's actually working, digs
up what to try next, and learns from ads found elsewhere, so every campaign traces back to a reasoned
decision instead of ad hoc guesswork.

Everything here is written for someone who does **not** need to read code to understand it. If you're
picturing a small in-house ad-ops team (a planner, an auditor, a researcher, and a scout) working off
one shared filing cabinet, you already understand the shape of it.

## The big picture

```mermaid
flowchart LR
    subgraph Ideate["Finding what to try next"]
        I1["Competitor + product-story research\n(ad-ideation)"]
        I2["Learn from an ad found elsewhere\n(ad-intake)"]
    end

    subgraph Setup["Recommending a new ad"]
        S1["Names, targeting, creative, budget\n(ad-setup-loop)"]
        S2(["Created on Snap, PAUSED\n(snap-push) — or by hand on Meta"])
        S3(["You enable it in Ads Manager"])
    end

    subgraph Track["The filing cabinet"]
        L1["One record per recommendation,\nproposed through reviewed"]
    end

    subgraph Audit["Checking what's real"]
        A1["Pull real performance data,\njoin it back to the record\n(ad-audit)"]
        A2{"working / not-working /\ninconclusive?"}
    end

    I1 -->|"recommend"| S1
    I2 -->|"recommend"| S1
    S1 --> L1
    L1 --> S2
    S2 -->|"log the real IDs"| L1
    L1 --> A1 --> A2
    A2 -.->|"feeds the next round"| I1
```

Nothing in this loop ever touches a live Meta or Snap account. The only step that reaches the outside
world &mdash; creating or changing anything in Ads Manager &mdash; is done by a person, every single
time.

## Read next

- **[How the four modes work](How-the-four-modes-work)** &mdash; the loop, step by step, in plain
  language
- **[The ledger](The-ledger)** &mdash; what "the ledger" actually is, and the lifecycle every
  recommendation moves through
- **[The rules](The-rules)** &mdash; the compliance, targeting, creative, naming, budget, and tracking
  files every mode reads live before it does anything
- **[Data access](Data-access)** &mdash; the two channels into Riteangle's real performance numbers, and
  the one boundary that never gets crossed
- **[Why it's built this way](Safety-and-guardrails)** &mdash; the safety reasoning behind the design
- **[Working across machines](Working-across-machines)** &mdash; how a laptop and cloud sandbox sessions
  stay in sync through GitHub alone
- **[Command cheatsheet](Command-Cheatsheet)** &mdash; every `ad-agent` command, grouped by what you're
  trying to do
- **[Technical architecture](Technical-Architecture)** &mdash; the actual stack and module map, for a
  technical reader
- **[Agent registry](Agent-Registry)** &mdash; every skill by name, its procedure, and exactly where it
  hands off to a human
- **[Glossary](Glossary)** &mdash; plain-language definitions of the terms used across these pages
