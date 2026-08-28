---
id: lrn-2026-08-28-gemini-watermark-is-tier-gated
subject: creative
claim: Gemini's visible sparkle watermark persists on the Free and AI Pro tiers, so
  only AI Ultra or AI Studio output can satisfy the no-AI-label rule
source: platform-doc
confidence: high
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2027-02-24'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Gemini's visible sparkle watermark persists on the Free and AI Pro tiers, so only AI Ultra or AI Studio output can satisfy the no-AI-label rule

## Evidence

- (2026-08-28) Google's Nano Banana Pro announcement (blog.google, 20 Nov 2025) and the Gemini API image docs (ai.google.dev/gemini-api/docs/image-generation), read 28 Aug 2026: Google applies a visible Gemini 'sparkle' watermark to generated images on the Free and Google AI Pro tiers, and removes it for Google AI Ultra subscribers and in Google AI Studio, the developer surface. Invisible SynthID is applied to all Google-generated media regardless of tier, and DeepMind states it is designed to survive cropping, filtering, frame-rate changes, lossy compression, noise and speed changes - though it publishes no failure thresholds. This matters because rules/creative-generation.md section 4 forbids 'AI-tool watermarks or labels of any kind' and the app owner restated it on 2026-08-17 as 'No grok label', while the Gemini image path is otherwise the best-evidenced option and is what the product's own photo engine already ships. India INR tiers reported as AI Plus Rs 399, AI Pro Rs 1,950, AI Ultra Rs 24,500 per month (secondary sources, unverified) - so the clean-output consumer tier is roughly 2.6x the entire current Rs 9,400/month tool budget, and the API or AI Studio route is the affordable way to a watermark-free asset. Also verified: Google's API pricing page lists gemini-3.1-flash-image at $0.067 per 1K image and $0.034 batch, against the $0.04 the photo-engine eval budgeted on gemini-2.5-flash-image.
