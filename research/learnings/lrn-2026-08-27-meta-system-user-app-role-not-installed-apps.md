---
id: lrn-2026-08-27-meta-system-user-app-role-not-installed-apps
subject: channel
claim: A Meta system user cannot be given an app role from the Installed apps tab;
  the role comes from Assign assets > Apps, and the app is installed by the act of
  generating a token.
source: live-data
confidence: low
sample_n: 1
status: open
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-12-25'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

A Meta system user cannot be given an app role from the Installed apps tab; the role comes from Assign assets > Apps, and the app is installed by the act of generating a token.

## Evidence

- (2026-08-27) CONFIDENCE LABEL IS A GATE ARTIFACT — see q-2026-08-27-min-sample-and-config-facts. Observed 2026-08-27 while setting up riteangle-api (61593371450505). The Installed apps tab has no Add button and reads 'No apps installed yet - Generate a token to manage your business assets'; its '...' menu offers only Edit info and Assign assets. With no app role assigned, the Generate-token wizard shows 'No permissions available - assign an app role to the system user' and Generate is disabled. The role is granted via Assign assets > Apps > riteangle > Develop app (View insights and Test app bundle in; Manage app can stay off), after which the scope list appears. The wizard footer states: 'By clicking Generate Token, you agree to install the selected app for system user riteangle-api.' So installation is a CONSEQUENCE of generating, and the sequencing advice given earlier that day - install the app first or the token dialog will not offer it - had the dependency backwards and describes a step that cannot precede token generation in this UI version.
