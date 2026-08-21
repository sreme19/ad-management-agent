# Budget guardrails

Source: Sree's Aug 7 log. Every `ad-setup-loop` recommendation must state a budget cap and duration
(SPEC.md decision #5) and should default to these figures unless there's a specific reason to deviate
— state the reason plainly if it does.

## Operating envelope

- **Total operating budget: ~₹50,000/month.** Concentrate on learning speed, not scale, until unit
  economics are cracked (cost to acquire one active woman, one active man).
- **Split:** 40–50% testing (new creative + audience variants) · 40–50% exploitation of proven winners
  · 10% retargeting/engagement once there's signal to retarget against.
- **Minimum viable daily spend: ₹800–1,200 per active ad set.** Below this, the platform's delivery
  algorithm rarely exits its learning phase — concentrate spend rather than spreading it thin across
  many ad sets at once. (An earlier note mentions ₹100/day tests; that volume only tells you whether an
  ad *can* deliver, not whether the offer or creative is any good — treat anything below the floor as a
  system check, not a real experiment.)

## Test → measure → kill/double → exploit loop

1. **Hypothesis → test.** ~70% of budget in early weeks goes to testing new creative/audience
   combinations.
2. **Measure.** Installs, landing-page views, Bestie-conversation-starts, or whatever the campaign's
   stated success metric is (see `ad-setup-loop`'s brief template — every proposal names one).
3. **Kill or double.** Pause a losing ad set after **3–5 days or 50–100 events**, whichever comes
   first. Move its budget to whatever's winning.
4. **Exploit.** Scale the proven creative × audience × bid combination.

## Signup targets (context, not a hard budget rule)

Most recent figures (Aug 17 log): **1,000 men signups at ~₹25/signup**, **100 women signups at
~₹200/signup** — the ~8x cost asymmetry reflects the platform's own gender-balance goal (women are the
scarcer, more valuable acquisition on a dating product skewed male across the market). A recommendation
targeting women should tolerate a materially higher cost-per-signup than one targeting men; treating
them as the same target is a modeling error, not a budget win.

## Confidence gating (SPEC.md decision #6)

`ad-audit` inherits `pocket-dating-coach`'s `MIN_SAMPLE = 30` floor for any claim that a specific ad set
is or isn't working. Below that sample, the correct answer is "not enough data yet" (`inconclusive`),
never a guess dressed as a finding.
