---
id: lrn-2026-08-28-product-rejects-what-ads-are-made-of
subject: product
claim: The product rejects AI-generated photos as untrustworthy while all of its paid
  creative is AI-generated, and no rules file reconciles the two
source: own-research
confidence: medium
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2026-12-26'
derived_from: note-2026-08-28-internal-ai-creative-prior-art
questions: []
recs: []
promoted_to: null
---

## Claim

The product rejects AI-generated photos as untrustworthy while all of its paid creative is AI-generated, and no rules file reconciles the two

## Evidence

- (2026-08-28) [master] Riteangle - product requirement.docx states the anti-AI-forgery rule in three separate proof categories. Lifestyle Photos: 'Uploaded photos must pass an anti-AI-forgery check. AI-generated, synthetic, or manipulated photos are rejected and don't count. Only genuine, real-world photos earn the signal.' Discipline: 'uploads must pass the check. AI-generated, synthetic, or manipulated images (including faked app screenshots) are rejected and earn no trust.' The product's trust proposition is therefore that it can distinguish real from synthetic and refuses synthetic. Every Riteangle paid asset to date is Grok-generated, and rules/creative-generation.md is written entirely around generated imagery. The marketing side is aware of the seam - [master] Riteangle - marketing requirement.docx line 270 says 'Label AI imagery. All AI imagery is labelled in-product as generated from verified photos. Creative that shows a portrait should not imply it is an untouched snapshot' - but that clause governs in-product imagery, not ads, and no rules/ file carries it. Note also that rules/creative-generation.md section 4 forbids 'AI-tool watermarks or labels of any kind' in generated output, which is about not letting the sampler stamp its own mark and is reconcilable with deliberate disclosure, but nothing states the distinction. Caveat: this is a brand-coherence and disclosure risk that has not been tested against any actual user reaction or platform enforcement.
