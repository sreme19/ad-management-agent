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

## Start from the queue, not from a blank page

**Run `ad-agent open` first.** Research that starts from "go find some ideas" wanders; research that
starts from an open question converges. The queue is filled by every other mode — an `inconclusive`
audit verdict, an intake raising a why-does-this-work, a previous idea held pending research — and
`open` lists what is unanswered, alongside learnings past their review date and notes nobody has
derived anything from.

If the pass answers one of those questions, close it: `ad-agent answer <q-id> --text "..."`, or pass
`--answers <q-id>` to the `learn` that resolves it.

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

1. **`ad-agent open`** — see what is already outstanding before adding to it.
2. Research broadly — competitor creative, product stories, open hypotheses, ad-audit findings — before
   narrowing.
3. **Record what you learned, separately from what you propose.** A durable claim about the world is a
   learning; a thing to try is an idea. They have different lifetimes and the distinction is what makes
   the library usable later:
   ```
   ad-agent learn --claim "..." --subject audience|creative|channel|tracking|competitor|product|budget \
     --source live-data|platform-doc|source-code|own-research|competitor-observation|intuition \
     --confidence high|medium|low [--sample-n <n>] --evidence "..." [--answers <q-id>] [--slug ...]
   ```
   **The confidence gate will refuse you, and it is right to.** Only `live-data`, `platform-doc` and
   `source-code` may be `high`; a competitor observation or an informed hunch caps at `medium`, however
   plausible it feels. A `live-data` claim needs `--sample-n` and can only be `low` below
   `MIN_SAMPLE = 30`. Don't reach for a source kind that fits the confidence you want.
4. For each idea worth writing up: name the persona/audience, the emotional hook or product story it's
   built on, why this and why now, an estimated daily spend to test it, and a compliance check against
   `rules/compliance.md`.
5. Give each a verdict: `recommend` or `hold`, and **write it down**:
   ```
   ad-agent idea --title "..." --verdict recommend|hold --network <key from rules/networks.yaml> \
     --persona <from rules/targeting.md> --est-daily <INR> --est-days <n> --rationale "..." \
     [--learning <lrn-id>]... [--blocked-on "..."] [--slug ...]
   ```
   A `hold` **must** state `--blocked-on`: what would have to be true for it to become recommendable.
   The command refuses without it, because a hold with no unblock condition is indistinguishable from a
   no and will sit in the queue forever.
6. **Cite only the learnings the test actually bears on.** `--learning` is not a bibliography. When the
   campaign returns a verdict, `log-review` applies it to every learning the idea lists — so naming a
   claim this test will not vary marks it on evidence it did not produce.
7. Present the list to the user plainly, ranked by conviction, not just chronologically.

## What is not an idea

If the thing to do is a landing-page change, a tracking fix, or anything else that is not a campaign,
**do not force it into an `idea`** — it has no daily spend and no persona, and dressing it as one makes
the ideas queue lie about what is actionable here. Record it as a learning plus a question, and say
plainly whose repo the fix belongs in.

## On approval

An approved idea feeds straight into `ad-setup-loop` (mode 5). Hand off the persona, hook and estimated
spend rather than making the user re-explain it — and tell that skill the idea id, so it can pass
`ad-agent propose --from-idea <idea-id>` and close the idea out. An approved idea that became a real
record should stop showing up in `open` as one nobody acted on.
