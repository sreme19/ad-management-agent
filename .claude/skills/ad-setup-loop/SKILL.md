---
name: ad-setup-loop
description: Recommend a new ad — campaign/ad-set/ad names, targeting, and creative — for Riteangle's Snap or Meta campaigns, write the recommendation to the ledger, and later log the real IDs once it's set up by hand. Use whenever the user asks to set up an ad, launch a campaign, try a new audience/creative, or asks what to build next after an ad-ideation or ad-intake idea was approved.
---

# Setting up an ad (mode 5)

## What this skill never does

This skill produces instructions a human executes by hand in Ads Manager. It never calls a Meta or
Snap Ads Manager API to create, publish, enable, or change budget on anything live — that boundary is
locked in `SPEC.md` and does not get relaxed later, even once a Claude plugin exists to "steer"
implementation. The plugin's job, if it ever exists, is telling the human what to click — never
clicking it.

## The standards to follow — read the source, don't improvise from memory

These are the actual product rules, and they may have been refined since you last read them:

- `rules/compliance.md` — hard, App-Store-enforced constraints. Read this first. Every recommendation
  gets checked against it before it's considered ready (see "Quality check" below).
- `rules/targeting.md` — audience personas, age/gender bands, geography, the provider-energy
  backend-vs-copy distinction.
- `rules/creative-style.md` — tone of voice, taglines, quotable first-party stats, visual identity,
  competitive landscape.
- `rules/naming.md` — the exact campaign/ad-set/ad naming convention. A name that doesn't match this
  breaks the spend/traffic join in `pocket-dating-coach`'s own analytics later — this is not cosmetic.
- `rules/budget.md` — the operating envelope, minimum viable daily spend, and the kill/double rule.

If the user refines any rule mid-conversation, **edit the rule file itself in the same turn** — don't
just apply the change once and let it evaporate. The next `ad-audit` run, and the next session, both
depend on that file being current.

## Procedure

1. **Establish the brief.** What triggered this recommendation — an approved `ad-ideation` idea, an
   `ad-intake` finding, or a direct ask? Name the persona (`rules/targeting.md`), the network, and the
   one success metric this ad set is being tested against (landing-page views, taps, Bestie-conversation
   starts, signups — match it to the funnel stage in the campaign name).
2. **Decide names, following `rules/naming.md` exactly.** Campaign, ad set, ad — all three, plus the
   UTM parameters that go on the landing URL.
3. **Decide targeting** — persona, age band, gender, geography, interest categories, device targeting —
   per `rules/targeting.md`. State it as a short paragraph, not just a list of fields, since that's what
   goes into the brief.
4. **Decide the creative** — which existing asset under `creatives/` to use, or a brief for a new one to
   commission, following `rules/creative-style.md`'s tone, taglines, and visual identity. If it's a new
   asset, note that mode 8 (`ad-intake`) or a fresh export is how it eventually lands in `creatives/`.
5. **State a budget cap and duration**, per `rules/budget.md` — never omit this. Default to the
   ₹800–1,200/day minimum viable range unless there's a specific reason to go higher or lower; say the
   reason if you deviate.
6. **Quality check before handing anything off.** Run the finished ad-set name, targeting summary, and
   creative brief/copy back against `rules/compliance.md` explicitly — show a short table: each
   compliance rule against how this recommendation satisfies it, or note plainly why a rule doesn't
   apply. This mirrors job-hunt-agent's own observability-trace requirement; don't skip it because the
   copy "feels obviously fine." Per Sree's own note, prefer a second, independent pass (a fresh
   session/model) over trusting the same reasoning pass that wrote it.
7. **Write the brief to a file**, then log the proposal — this is a pure file write, no API call:
   ```
   ad-agent propose <slug> \
     --network snap|meta \
     --campaign-name "..." --ad-set-name "..." --ad-name "..." \
     --targeting-summary "..." --creative-ref "creatives/<path-or-id>" \
     --budget-cap <INR/day> --duration-days <n> \
     --brief /tmp/brief.md
   ```
   This prints the generated `rec_id` and the record's path. Show the user the full brief and the
   `rec_id` plainly — that id is what they'll need for the next step.
8. **Hand it back.** The user sets this up by hand in Ads Manager. Tell them exactly what to name each
   level and what to paste into targeting/budget fields — this should read like a checklist they can
   follow without re-deriving anything.

## Closing the loop — do this every time, don't let it go unresolved

Once the user says the ad is live (or comes back later with the real IDs), log it — this is what lets
`ad-audit` later join a real outcome back to this exact recommendation:

```
ad-agent log-setup <rec_id> --network snap|meta \
  --campaign-id <real> --ad-set-id <real> --ad-id <real> \
  [--deviated "what changed from the brief, and why"]
```

If the user decides not to execute a proposal at all, close it out explicitly rather than leaving it to
rot as `proposed` forever:

```
ad-agent abandon <rec_id> --reason "..."
```

## The one rule that never changes

Regardless of how good the recommendation is, **you never touch Ads Manager yourself**. Every campaign,
ad set, and ad gets created by the user's own hand, from the instructions you hand them.
