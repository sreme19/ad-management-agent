---
id: lrn-2026-08-31-meta-w3-lead-spend-not-captured
subject: tracking
claim: Meta spend for the mid-August lead surge is not captured — fetch-analytics shows
  ₹0 Meta spend for Aug 15–21 despite 119 Meta leads arriving that week; Meta spend only
  appears from Aug 22 onward, so Meta cost-per-lead for the biggest Meta batch is unknown
source: own-research
confidence: high
sample_n: 119
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

`ad-agent fetch-analytics` reports **₹0 Meta spend for W3 (Aug 15–21)**, yet **119 Meta
leads** were stored in `marketing_leads` that week. Meta spend first appears in the
leaderboard in **W4 (Aug 22–28)** and continues in W5. So the platform delivered and
billed for Meta lead volume in mid-August that our analytics has no spend row for, and
**Meta cost-per-lead for the largest Meta batch of the month cannot be computed.**

This is a cost-side blind spot distinct from — but of a piece with — the known Meta
ingestion/attribution breakage. Snap spend for the same W3 window is present and complete;
only Meta's is missing.

## Evidence

- (Aug 2026, per-week `fetch-analytics` leaderboard, spend in INR):
  - W2 (Aug 8–14): Meta **₹0**, Snap ₹1,584
  - W3 (Aug 15–21): Meta **₹0** — but **119 Meta leads** stored — Snap ₹1,984
  - W4 (Aug 22–28): Meta ₹296 (traffic/LPV), Snap ₹360
  - W5 (Aug 29–31): Meta ₹699 (₹628 lead + ₹71 traffic), Snap ₹1,167
- Every non-W3 Meta week reconciles (spend present alongside or ahead of leads). W3 is the
  hole: real Meta lead delivery, zero recorded Meta spend.
- Month total captured spend was ₹6,090 (Snap ₹5,095 / Meta ₹995). If W3 Meta spend is
  genuinely missing rather than genuinely zero, the true Meta spend — and the month total —
  is understated, and the "Meta ₹22/lead" figure (W5 only) is the *only* trustworthy Meta
  CPL we have.

## Consequence for planning

- **Never present a month-level Meta cost-per-lead as if it covers W3.** Meta CPL is known
  only for W5 (~₹22). The 119 W3 Meta leads have no cost attached — say so rather than
  dividing by a partial spend figure.
- Treat the captured **₹6,090 August total as a floor**, not a settled number, until the
  W3 Meta gap is explained (spend API not connected in mid-August vs. a genuine zero-spend
  organic/backfilled batch).
- Reconciliation for spend needs the same discipline the lead count already has: pull the
  **Meta Ads Manager** spend for Aug 15–21 and compare to our ₹0 before trusting either.
- Open question this raises: were those 119 W3 Meta leads even paid delivery, or were they
  backfilled from an earlier period? That bears on `project_meta_lead_ingestion_broken`.

## Related

- `lrn-2026-08-31-meta-lead-ingestion-both-paths-broken.md` — the ingestion side of Meta's
  recurring gaps; this atom is the spend/cost side.
- `lrn-2026-08-31-snap-women-targeted-leads-deliver-male.md` — same W3 window, audience
  side; also the reason Snap's W3 CPL is known while Meta's is not.
- `lrn-2026-08-30-marketing-leads-undercounts-leads-by-design.md` — the standing rule that
  a channel returning a clean zero is not proof of zero.
