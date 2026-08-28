---
id: note-2026-08-28-internal-ai-creative-prior-art
title: 'Internal prior art on AI-generated ad creative: LexHive ads team, Riteangle
  photo engine, tool spend'
source: own-research
captured: '2026-08-28'
learnings:
- lrn-2026-08-28-edit-framing-beats-recreate
- lrn-2026-08-28-ai-tests-humans-ship
- lrn-2026-08-28-product-rejects-what-ads-are-made-of
---

# Internal prior art on AI-generated ad creative (LexHive/DemandLane ads team + Riteangle photo engine)

Retrieved 2026-08-28 from the local `job-hunt-corpus` retrieval index over the user's own
meeting-notes corpus, and from `RAD - Documents/` and `pocket-dating-coach/docs/photo-engine/`.
Verbatim extracts, with source document and date.

## 1. The ads team already runs AI video in production (a different business, US legal lead-gen)

**"Briefing Session - Ads & Marketing Team <> Deep", 2025-11-28.** Avinash MB, Krishna Soni,
Sagar Basagouda Gudodagi, Rup Sarmah, Sree Dayanidhi, Deep Kakkad.

> "Most of the creatives that we use in our funnel are videos. So we use extensively we use uh AI
> videos and stuff."  — Avinash MB

> "Videos are performing better than images for them, and they use different AI tools to create
> videos that look more or less like real ads, incorporating different visualizations and hooks."

> "Avinash MB listed multiple tools they are constantly evaluating, including B3 and ARADS
> (00:13:04). Krishna Soni added 'Heny' and 'Ltx' and stated they try market tools to see which
> provides a more realistic output."

Tool names are Gemini's transcription of speech and are garbled. Best reading, flagged as
inference not fact: **ARADS = Arcads** (arcads.ai, AI-actor UGC ads), **Heny = HeyGen**,
**Ltx = LTX Studio**, **B3 = possibly Veo 3**. Not verified with the speakers.

The most important line in the whole set, because it states the limit of the medium:

> "Avinash MB explained that sometimes AI-generated content is not perfect and people can identify
> it as AI. They primarily use AI to test concepts and, once tested, they engage with actual
> creators from marketplaces to produce the final videos (00:14:10)."

So the working pattern in the one place inside this org with real spend behind it is
**AI for concept discovery, humans for the winning asset** — not AI end-to-end.

## 2. Seedance was evaluated three weeks ago, with numbers

**"SSD Scale Up Meeting", 2026-08-06.** Aditi Shinde presenting.

> "Aditi Shinde shared that the team experimented with Seedance, a ByteDance model, to create AI
> videos, resulting in high-quality output that resembles real actors. Aditi Shinde noted that the
> current third-party tool limits prompts to under 2,000 characters, which restricts the level of
> detail compared to Xfield. Regarding efficiency, this tool generates videos in 5 to 6 minutes,
> whereas Xfield takes about 10 minutes and Supercomputer takes up to 45 minutes, with the latter
> often producing poor-quality results. Xfield is expected to launch the Seedance 2.0 model on
> August 8th. Aditi Shinde will investigate if the team can license the Seedance 2.5 model directly
> from ByteDance to avoid tool-based limitations."

Summary line from the same doc:

> "Testing shows Seedance models outperform existing tools in both speed and quality. Direct
> licensing is prioritized to bypass current character limitations."

"Xfield" is almost certainly **Higgsfield** (inference). "Supercomputer" is unidentified.

Open action item, owner Aditi Shinde, dated 2026-08-06, status unknown as of 2026-08-28:
> "[Aditi Shinde] Investigate Seedance Availability: Research if Seedance 2.5 is available for
> direct purchase as a model from ByteDance."

## 3. They tag creative "real" vs "AI" and have looked at the split — but the data is unusable

**"Weekly Marketing Review", 2026-03-09.** Aditi Shinde and Avinash MB.

> "Aditi Shinde and Avinash MB discussed the data sources, specifically whether content is
> designated as 'real' versus 'AI' and whether this designation is derived from the name."

> "Avinash MB referenced a dashboard analysis they had previously requested, which suggested
> focusing on 'real' creators and doubling down on a 'real story angle'. They noted that the meaning
> of 'real' in this context likely means the word is present in the ad's name, but they are not
> entirely sure and need to verify it."

And why the read cannot be trusted:

> "Aditi Shinde estimated that the naming is about 80% accurate but the margin of error makes the
> data unusable for analysis."

So: there is an in-house signal pointing at *real* beating *AI*, and it is explicitly not
trustworthy, for the same reason `ad-management-agent` built `naming.md` —
cf. `lrn-2026-08-26-naming-conformance-breaks-audience-cut`, which is the identical failure in
this repo.

## 4. Riteangle already ran a rigorous generation-vendor bake-off — for stills

**`riteangle-photo-engine-eval.pdf`, 2026-06-29.** Six approaches, four vendors, cohort of five
real men. Decision:

> "Ship Google Gemini 2.5 Flash Image with multi-reference + edit-framing + a flattering dial as
> the MVP photo engine. No per-person training. ~$0.04/image → ~$120 per 1,000 men (3 photos each).
> Per-person fine-tuning (Astria) is reserved as an optional paid 'Pro photos' tier."

| Approach | Identity | Realism | Cost/image | Verdict |
|---|---|---|---|---|
| Gemini 2.5 — edit-framing + flattering | Strong | High | ~$0.04 | SELECTED |
| Gemini 2.5 — "recreate" framing | Poor — drifts/ages/baldens | High | ~$0.04 | Rejected |
| Astria — per-person fine-tune (FLUX LoRA) | Best | High | $1.50 train + $0.10 | Premium tier only |
| flux-pulid (FLUX, Replicate) | Medium | Medium — glossy | ~$0.04 | Rejected — baldens, glossy |
| InstantID (SDXL, Replicate) | Medium | Poor — cartoon, bad hands | ~$0.08 | Rejected |
| fal.ai flux-pulid (previous prod engine) | — | — | ~$0.05 | Account out of balance |
| Grok / xAI | — | — | — | **Not tested (unfunded)** |

The transferable finding, and the reason this document matters today:

> "Gemini 2.5 — edit-framing + flattering. Framing it as an edit of one real man ('keep him
> identical, change only the scene') preserved identity + hair while keeping realism; a flattering
> clause makes it his most attractive self."

versus the rejected sibling:

> "Gemini 2.5 — 'recreate' framing. Most realistic of the field, but prompting it to 'recreate him'
> made it idealize — drifting to an older, balder, or different face."

Same model, same cost, opposite result, on the framing verb alone. Also recorded:

> "Identity scoring is human-judged (the subject's own face is the ground truth); automated vision
> scores under-rate correct-but-different-angle shots."

> "Result: strong on 4 of 5; one fixable edge case (older grey-haired men de-age unless explicitly
> guarded). The recipe generalizes across age, hair type, and source-photo quality."

## 5. The product itself rejects AI photos — a brand tension the ad medium has to respect

**`[master] Riteangle - product requirement.docx`.** Repeated across Lifestyle Photos, Discipline
and Social Proof sections:

> "Uploaded photos must pass an anti-AI-forgery check. AI-generated, synthetic, or manipulated
> photos are rejected and don't count. Only genuine, real-world photos earn the signal."

> "Anti-AI-forgery: uploads must pass the check. AI-generated, synthetic, or manipulated images
> (including faked app screenshots) are rejected and earn no trust."

The product's trust proposition is that it can tell real from synthetic and refuses synthetic.
Riteangle's own paid creative is, today, entirely synthetic.

## 6. The marketing requirement already carries an AI-labelling clause

**`[master] Riteangle - marketing requirement.docx`, line 270:**

> "Label AI imagery. All AI imagery is labelled in-product as generated from verified photos.
> Creative that shows a portrait should not imply it is an untouched snapshot."

And in **"Riteangle - marketing meeting notes", 2026-08-07**, among the hard constraints:

> "Creative must still obey every hard constraint from the marketing knowledge base (no
> money/provider language, no real male photos, 18+, label AI imagery, etc.)."

Note this does not obviously agree with `rules/creative-generation.md` §4, which says never
generate "AI-tool watermarks or labels of any kind." The two are reconcilable — don't let the
*sampler* stamp its own mark; do disclose deliberately in a layer you control — but no rules file
currently says so.

## 7. Latest creative direction, and the unit economics that bound tool spend

**"Riteangle - marketing meeting notes", 2026-08-17:**

> "Setting up the ad by using claude / Use sonnet → medium/low / Quality check step before posting
> the ad → use another AI to check the work / No grok label / Image the itself should not have AI
> glitches / Indian models / Research a bit on what can get women"

Targets from the same entry:

> "Bonus - signed up / 1000 men - Rs. 25 per men sign up / 100 women - Rs. 200 per women signup"

**`RAD Tool Expenses .xlsx`, last modified 2026-08-06** — total ₹9,400/month:

| Tool | ₹/month | Status |
|---|---|---|
| Claude | 2,400 | Active |
| Vercel | 2,000 | Active |
| Anthropic API | 2,000 (on-demand) | Active |
| Fal.ai | 2,000 | (blank) |
| Grok | 1,000 | Active |
| Gemini | — (on-demand) | Active |
| AWS, Kiro, Windsurf | 0 | Suspended |

So the whole generation stack runs on ₹9,400/month against a ~₹50,000/month ad budget, and a
₹25/male-signup, ₹200/female-signup target. Any new generation tool has to be priced against that,
not against a US agency's budget.

## 8. A video asset already exists and has never been discussed in this repo

`RAD - Documents/Snap Ad Copies/` holds two files dated 2026-08-07:
- `Flooded Women image` — JPEG, 720×1280
- `Flooded women video ` — MP4 (ISO Media), 1.19 MB

Both are named for the FOURTEEN-SUITORS / flooded-woman hook. Nothing in `creatives/`,
`research/` or the ledger mentions a video asset. Provenance, tool, and whether it ever ran
are all unknown.
