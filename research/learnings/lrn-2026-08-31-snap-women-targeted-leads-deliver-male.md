---
id: lrn-2026-08-31-snap-women-targeted-leads-deliver-male
subject: audience
claim: Snap's mid-August women-targeted lead campaigns delivered overwhelmingly male
  leads — women-targeted ad sets (WOMEN_18-35, SC_F_19-30, WOMEN_18-34) produced ~90%
  male leads, i.e. Snap ignored the gender constraint and served men at scale
source: own-research
confidence: medium
sample_n: 250
status: open
created: '2026-08-31'
last_confirmed: '2026-08-31'
review_after: '2026-11-30'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

When Snap lead campaigns were pointed at **women** in mid-August (W3, Aug 15–21), the
leads that came back were **overwhelmingly male**. The ad-set names encode the intended
audience — `WOMEN_18-35_CASUAL_STORY_IND_LEADS`, `SC_F_19-30_India`,
`RA_LEADS_WOMEN_18-34_IN_20260818` — yet the delivered leads read ~90% male. Snap did not
hold the gender constraint; it served men at volume and cheaply.

This is the inverse of the late-August pattern, where women-targeted spend actually
delivered women — so the failure is specific to the W3 Snap run, not a permanent property
of the account.

## Evidence

- (Aug 15–21, W3) Snap delivered **250 leads** across the lead campaigns above. Inferred
  gender from first names: **~224 male / 8 female / ~18 unclear** — roughly 90% male out
  of a set explicitly targeting women. Snap lead-campaign spend that week was **₹1,433**,
  i.e. **~₹5.7/lead** — very cheap, but almost entirely the wrong gender.
- Lead quality compounded it: **207 of 273** Snap leads in the window had **no email at
  all** (name only). So the cheap male leads were also largely uncontactable.
- Contrast W5 (Aug 29–31): the women-targeted `WOMEN_18-30_MOVEON-LEAD` Snap campaign
  (₹760) delivered **11 female / 7 male / 3 unclear** out of 21 — majority female. Same
  account, same platform, women-targeting *worked* here. So W3 was a delivery/targeting
  failure, not a structural impossibility.
- Gender is inferred from first names (real error rate on ambiguous Indian names) and
  ~15% of handles were unclassifiable, so treat the split as directional, not measured.

## Consequence for planning

- **Do not trust a Snap lead campaign's gender label from its name.** Before scaling a
  gender-targeted Snap lead campaign, check the *delivered* gender mix against the intended
  one; Snap has demonstrably served the opposite gender at volume while reporting cheap CPL.
- A low cost-per-lead on Snap is not by itself a success signal — W3's ₹5.7/lead was the
  cheapest of the month and the least useful (wrong gender + no email).
- When the goal is women specifically, weight toward the creative/campaign shape that
  worked in W5 (the "MOVE-ON" women-targeted lead set) rather than the W3 story-lead sets.

## Related

- `lrn-2026-08-29-roman-script-is-an-audience-signal.md` — another case of the delivered
  audience differing from the nominal target.
- `lrn-2026-08-31-meta-w3-lead-spend-not-captured.md` — the same W3 window, cost side:
  Meta's spend for its 119 W3 leads is missing, so W3 cost-per-lead is only known for Snap.
