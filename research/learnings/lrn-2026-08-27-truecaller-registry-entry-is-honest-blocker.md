---
id: lrn-2026-08-27-truecaller-registry-entry-is-honest-blocker
subject: tracking
claim: "Adding Truecaller to rules/networks.yaml needs no client module \u2014 creation:none\
  \ with no credentials is already a valid, Meta-proven shape \u2014 but it cannot\
  \ be written honestly today, because networks.py rejects an entry with an empty\
  \ ad_join_param or ad_set_join_param and Truecaller's own click-URL macro convention\
  \ is undocumented outside the login."
source: source-code
confidence: high
sample_n: null
status: open
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-10-26'
derived_from: note-2026-08-27-truecaller-channel-recon
questions: []
recs: []
promoted_to: null
---

## Claim

Adding Truecaller to rules/networks.yaml needs no client module — creation:none with no credentials is already a valid, Meta-proven shape — but it cannot be written honestly today, because networks.py rejects an entry with an empty ad_join_param or ad_set_join_param and Truecaller's own click-URL macro convention is undocumented outside the login.

## Evidence

- (2026-08-27) networks.py _load() raises NetworkError on any entry missing utm_source, ad_join_param or ad_set_join_param, and require_creation is additive-only so creation:none needs no code. Truecaller publishes no tracking documentation publicly (see the same note's Support finding). Guessing Snap's utm_id here would repeat the 2026-08-21 incident in rules/tracking.md, where an assumed auto-appended parameter cost a week of unattributable spend.
