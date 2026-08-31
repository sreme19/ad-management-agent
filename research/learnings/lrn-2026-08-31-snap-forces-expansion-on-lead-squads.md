---
id: lrn-2026-08-31-snap-forces-expansion-on-lead-squads
subject: audience
claim: 'Snap re-enables targeting expansion on LEAD_FORM_SUBMISSIONS ad squads after
  creation, even when the create call sends enable_targeting_expansion=false. It appears
  specific to the lead objective: non-lead squads hold the flag off.'
source: live-data
confidence: low
sample_n: 17
status: open
created: '2026-08-31'
last_confirmed: '2026-08-31'
review_after: '2026-12-29'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Snap re-enables targeting expansion on LEAD_FORM_SUBMISSIONS ad squads after creation, even when the create call sends enable_targeting_expansion=false. It appears specific to the lead objective: non-lead squads hold the flag off.

## Evidence

- (2026-08-31) Read live off the Snap Marketing API 2026-08-31, all 17 ad squads on ad account 5c43c7ee (Riteangle - Primary). WOMEN_18-30_CASUAL_MOVEON-LEAD (85c2e782, ACTIVE, LEAD_FORM_SUBMISSIONS) reads enable_targeting_expansion=true with auto_expansion_options.auto_expansion_type=SMART_TARGETING, although its record rec-2026-08-29-moveon-lead-w1830-snap specifies expansion:false and targeting.to_snap sends the flag explicitly either way since commit a29fe59. auto_expansion_type is a key this repo NEVER sends, so Snap wrote it. Five squads carry SMART_TARGETING and all five are lead squads: WOMEN_18-30_CASUAL_MOVEON-LEAD, WOMEN_18-35_CASUAL_STORY_IND_LEADS, SC_F_19-30_India, RA_LEADS_WOMEN_18-34_IN_20260818, MEN_28-40_CASUAL_STORY_IND_LEADS. The one squad on the account reading enable_targeting_expansion=false is WOMEN_18-30_CASUAL_MOVEON-STORY (ACTIVE, created 2026-08-30 by snap-push-story, non-lead) - same code path for the flag, same account, same week, and it held. MECHANISM LINK: the three women-targeted lead sets that lrn-2026-08-31-snap-women-targeted-leads-deliver-male found delivered ~90 percent male in W3 are exactly three of the five SMART_TARGETING squads, which supplies that learning with the mechanism it lacked. LOW CONFIDENCE IS DELIBERATE: 17 squads is a census of one account rather than an experiment, the flip itself was never observed (only its end state), and no Snap doc has been read that says the lead objective forces expansion - that is the obvious next check. CONSEQUENCE MEANWHILE: expansion:false in a record is an INTENT on a Snap lead squad, not a fact. Read the squad back before crediting any women-targeted lead result to a narrow audience, and treat snap-push-lead's expansion DIFF line as expected rather than anomalous.
