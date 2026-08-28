---
id: lrn-2026-08-28-edit-framing-beats-recreate
subject: creative
claim: Framing an image prompt as an edit of a real photo preserves identity, where
  asking the same model to recreate the person makes it idealise and drift
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

Framing an image prompt as an edit of a real photo preserves identity, where asking the same model to recreate the person makes it idealise and drift

## Evidence

- (2026-08-28) riteangle-photo-engine-eval.pdf (29 Jun 2026) tested six approaches across four vendors on five real men for the product's own photo engine. Two rows differ only in the framing verb, on the same model at the same ~$0.04/image: 'Gemini 2.5 - edit-framing + flattering' scored Identity=Strong, Realism=High, SELECTED, described as 'Framing it as an edit of one real man (keep him identical, change only the scene) preserved identity + hair while keeping realism'. 'Gemini 2.5 - recreate framing' scored Identity=Poor and was Rejected: 'prompting it to recreate him made it idealize - drifting to an older, balder, or different face.' The recipe held on 4 of 5 men across age, hair type and source-photo quality, with one fixable edge case (older grey-haired men de-age unless explicitly guarded). Caveat: n=5, judged by humans on identity, and the finding is about portraits of a known real person - it is not established that the same framing advantage applies to inventing a model who does not exist, which is what ad creative does.
