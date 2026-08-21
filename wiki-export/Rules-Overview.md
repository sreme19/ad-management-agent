# Rules Overview

Every skill reads these files live, rather than having the rules restated in the skill's own
instructions — the same pattern `job-hunt-agent` uses for its fit filter and style rules. If a rule
gets refined mid-conversation, the correct move is to edit the file in place, not just apply the change
once. The canonical text lives in the repo under `rules/`; this page is a map of what's there, not a
copy of it.

## rules/compliance.md — read this one first

Hard, App-Store-enforced constraints, not style preferences. The iOS build was actually rejected under
App Store Guideline 1.1.4 ("compensated dating") on 2026-08-03. Money, wealth, generosity, and
provider-framing are never an attraction signal in ad copy — even though the matching backend is
allowed to model "provider energy" as a real preference some users have. That distinction (model it in
the algorithm, never say it in the creative) is the single most important thing to get right, and the
one most likely to be gotten wrong by pattern-matching on the underlying preference data. Also covers:
no purchase language, no rupee amounts for referral cash in-app, never call the membership
"high-earning," never show a man's real unenhanced photo, label AI imagery, 18+ without exception, and
running finished ad copy through the same banned-vocabulary gate the main product's build already
enforces.

## rules/targeting.md

The audience personas (Invisible Man, Flooded Woman, Second-Chapter Person, Casual but Selective
Woman), the core age/gender bands, city priority (Bangalore first, then Delhi/Hyderabad), and the open
hypotheses the source marketing research explicitly left untested (e.g. whether a Tier-2 city would
outperform further concentration in existing metros).

## rules/creative-style.md

Tone of voice, the taglines and ad-ready emotional hooks already identified, the first-party product
statistics that are safe and strong to quote (median time-to-match, median suitor count, share of
messages sent by an AI on someone's behalf, the platform's own gender ratio versus the market's),
objection-handling copy, the visual identity (palette, typeface, the deliberate light/cream look versus
competitors' dark UIs), and a production note on why six-second Snap creative needs purpose-built
scripted assets rather than generic stock footage.

## rules/naming.md

The campaign / ad-set / ad naming convention already live in production
(`RA_TRAFFIC_GET_IN_[GEO]_[FUNNEL]_[YYYYMM]` and so on) and the UTM scheme that has to go on every
landing URL for `pocket-dating-coach`'s own analytics to be able to join spend back to traffic. A
recommendation that doesn't follow this convention isn't just untidy — it breaks that join.

## rules/budget.md

The ~₹50,000/month operating envelope, the 40–50% test / 40–50% exploit / 10% retarget split, the
₹800–1,200/day minimum viable spend per ad set, and the rule for killing a losing ad set after 3–5 days
or 50–100 events. Also notes the roughly 8x cost-per-signup asymmetry between men and women that
reflects the platform's own gender-balance goal, not a targeting mistake.
