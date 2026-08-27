---
id: lrn-2026-08-27-matrix-options-are-code-changes
subject: channel
claim: Every capture-point and format option in the funnel matrix is a code change
  rather than a configuration change, because snap-push hardcodes a static-image,
  web-view, traffic-objective funnel end to end
source: source-code
confidence: high
sample_n: null
status: promoted
created: '2026-08-27'
last_confirmed: '2026-08-27'
review_after: '2026-10-26'
derived_from: note-2026-08-27-womens-funnel-matrix
questions: []
recs: []
promoted_to: rules/funnel.md
---

## Claim

Every capture-point and format option in the funnel matrix is a code change rather than a configuration change, because snap-push hardcodes a static-image, web-view, traffic-objective funnel end to end

## Evidence

- (2026-08-27) Read out of src/ad_agent/snap.py on 2026-08-27. Four values are literals with no parameter reaching them: upload_media posts type 'IMAGE' (line 321), create_creative posts type 'WEB_VIEW' with a single top_snap_media_id (lines 348-351), create_ad posts type 'REMOTE_WEBPAGE' (line 377), and the campaign is created with objective_v2_type 'TRAFFIC' (line 230). So a video ad is not a different asset through the same pipe — it needs the media type and the creative wiring changed. A carousel or collection needs a different creative type again. An on-platform lead form needs a different objective, a different ad type and a lead-form resource that snap.py has no call for at all. Only a second static image against the existing objective can be pushed today without touching this repo's code. Filed high on source-code's 60-day clock: one commit to snap.py invalidates it.
## Promoted (2026-08-27)

This claim is now normative, in `rules/funnel.md`. That file is what skills obey; this atom is only its origin.
