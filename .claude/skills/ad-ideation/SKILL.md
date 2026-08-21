---
name: ad-ideation
description: Deep research into what new campaigns, audiences, or creative angles could be worth deploying next for Riteangle — competitor creative, unused product stories, untested personas — ending every idea in a recommend/hold verdict with an estimated spend. On approval, hands off to ad-setup-loop. Use whenever the user asks for new ad ideas, wants a research pass on what to try next, or asks what's not being tested yet.
---

# Researching what to deploy next (mode 7)

## What this skill produces

A short list of ideas, each ending in a plain verdict — **`recommend`** or **`hold`** — with a stated
estimated spend to test it. This mirrors job-hunt-agent's `fit`/`risk` gate: an idea without a stated
cost is missing the thing the user would actually decide on. `hold` is not a dead end — say what would
need to be true (more research, a resolved compliance question, a cheaper way to test it) for it to
become `recommend`able.

## Where to look

- **`rules/creative-style.md`'s "Competitive landscape"** section, plus the Meta Ads Library, Snap's
  public ads library, and Google's Ads Transparency Center — see what Tinder, Bumble, Hinge, Shaadi.com,
  Aisle, TrulyMadly/QuackQuack are actually running right now, not just their stated positioning.
- **`ad-audit`'s findings** — a persona or creative angle that's already outperforming is a strong
  candidate for a deliberate scale-up idea, not just a wait-and-see.
- **Product stories not yet in creative** — `rules/creative-style.md` lists several (the honest-Tip
  feedback loop, the "clock stops while he answers" mechanic, the invite-loop-through-DMs channel) that
  are built and live but have never been turned into an ad. These are often stronger ideas than a new
  audience segment, because they're first-party and differentiated rather than a guess at what
  competitors are doing.
- **Open hypotheses already logged** in `rules/targeting.md` and the source marketing docs (e.g.
  whether a Tier-2 city like Indore outperforms further concentration in Bangalore/Delhi/Hyderabad) —
  these are explicitly flagged as untested, which makes them good research targets rather than
  assumptions to just adopt.

## Confidence — looser than ad-audit's, but not absent

Unlike `ad-audit` (which is bound to `pocket-dating-coach`'s `MIN_SAMPLE = 30` for verdicts on live
data), this skill is proposing hypotheses to test, not reporting on data that already exists — it's
allowed to reason from competitor observation, product knowledge, and qualitative signal. But every
idea still needs: which persona/audience it targets (`rules/targeting.md`), why now, an estimated
test spend (`rules/budget.md`'s minimum viable range as the floor), and a plain check against
`rules/compliance.md` before it's called `recommend`.

## Procedure

1. Research broadly — competitor creative, product stories, open hypotheses, ad-audit findings — before
   narrowing.
2. For each idea worth writing up: name the persona/audience, the emotional hook or product story it's
   built on, why this and why now, an estimated daily spend to test it, and a compliance check against
   `rules/compliance.md`.
3. Give each a verdict: `recommend` or `hold`. For a `hold`, say what would change the verdict.
4. Present the list to the user plainly, ranked by conviction, not just chronologically.

## On approval

An approved idea feeds straight into `ad-setup-loop` (mode 5) — hand off the persona, hook, and
estimated spend as the seed of that skill's brief rather than making the user re-explain it.
