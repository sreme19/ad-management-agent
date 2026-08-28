---
id: lrn-2026-08-28-video-cost-has-collapsed
subject: creative
claim: A vertical AI video clip now costs well under a dollar, so cost is no longer
  the reason Riteangle has not tested video
source: platform-doc
confidence: high
sample_n: null
status: supported
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2027-02-24'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

A vertical AI video clip now costs well under a dollar, so cost is no longer the reason Riteangle has not tested video

## Evidence

- (2026-08-28) Verified vendor pricing read 28 Aug 2026. Google (https://ai.google.dev/gemini-api/docs/pricing): Veo 3.1 Fast $0.10/s at 720p, $0.12/s at 1080p; Veo 3.1 Lite $0.05/s at 720p; Veo 3.1 supports 9:16 and includes native audio at no surcharge, in 4, 6 or 8 second durations. An 8-second vertical Veo 3.1 Fast spot is therefore ~$0.80, about Rs 70. Kling official API (https://kling.ai/dev/pricing): Kling 3.0 at $0.084/s 720p silent and $0.112/s 1080p silent, native 9:16 in text-to-video, up to 15s - a 5s 1080p silent clip is $0.56 - though the prepaid minimum is $700, so the aggregator route (fal.ai, matching kling.ai to the cent) is the accessible one. Alibaba Wan 3.0 on fal is $0.10/s at 720p and ranks first on the Artificial Analysis text-to-video arena (Elo 1,241, read 28 Aug 2026). ByteDance Seedance 2.5 (OpenRouter, read 28 Aug 2026) runs $0.1028/s at 480p, supports 4-30s, 9:16, and up to 50 reference assets. For comparison the whole Riteangle generation stack costs Rs 9,400/month (RAD Tool Expenses, 6 Aug 2026) against a ~Rs 50,000/month ad budget and a Rs 300/day ad-set default. What this does NOT establish: that video is worth running - q-2026-08-27-is-video-worth-it-for-women turns on whether the strongest women's threads survive motion, and lrn-2026-08-27-matrix-options-are-code-changes still applies because snap.py hardcodes IMAGE media. Also unverified: whether any of these vendors accept Indian cards or UPI, which was the one thing the research could not settle for any tool.
- (2026-08-28) **supported**: (2026-08-28) Follow-up verification on the Seedance route specifically. Seedance 1.5 Pro on fal.ai is ~$0.58 for a 5s 1080x1920 vertical clip with audio (~$0.29 with audio off, since fal halves the 1.5 Pro token rate when audio is disabled), and is the only verified-native path to true 1080x1920 - fal's own page states 1080p max with an explicit 9:16 enum. Two caveats to settle BEFORE spending, neither of which changes the cost conclusion. First, resolution honesty: the Seedance 2.0 paper states native resolution is 480p and 720p only, and fal's published pixel grid for 2.5 tops out at 720x1280 for 9:16, so the 1080p and 4K tiers sold on 2.x by fal, PiAPI and Wavespeed are very likely provider-side upscales rather than native renders. No platform publishes a 1080p dimension grid, so one test render is the only way to learn the actual output dimensions. Second, Seedance i2v on 2.5 exposes no aspect-ratio parameter at all - it inherits the ratio from the input image, so vertical output requires feeding a 1080x1920 still, which is consistent with lrn-2026-08-28-constrain-what-the-model-invents anyway. Payment rails partially closed against q-2026-08-28-which-ai-generation-vendors-can: fal.ai and Replicate are both verified India-eligible (embargo-only country restrictions, prepaid USD by card or ACH, so no RBI recurring-mandate exposure); Volcengine and BytePlus remain unverified because their docs are client-rendered and defeated every fetch.
