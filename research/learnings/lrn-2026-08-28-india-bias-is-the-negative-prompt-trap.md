---
id: lrn-2026-08-28-india-bias-is-the-negative-prompt-trap
subject: creative
claim: Steering an image model away from luxury does not land on ordinary middle-class
  India; peer-reviewed work shows these models substitute poverty and caste-coded
  imagery
source: own-research
confidence: medium
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2026-12-26'
derived_from: null
questions: []
recs: []
promoted_to: null
---

## Claim

Steering an image model away from luxury does not land on ordinary middle-class India; peer-reviewed work shows these models substitute poverty and caste-coded imagery

## Evidence

- (2026-08-28) Two peer-reviewed 2026 papers, surfaced 28 Aug 2026. 'Beyond Categories of Caste' (Singh, Das, Rama Subramanian, Saha, Voida, Semaan), FAccT '26, 28 Apr 2026, Montreal (https://arxiv.org/html/2606.00039v1, https://dl.acm.org/doi/10.1145/3805689.3806720): 1,536 images generated from gemini-flash-2.5-image across food, education, neighbourhood, migration, worship and profession. Upper-caste-coded names produced clean outfits, smiling subjects and clean streets; lower-caste-coded names produced a cleaner on a dirty street holding a broom in worn-out clothes; names with no surname defaulted to pottery work in a village setting with a makeshift house. The model assigned caste-coded occupations without any explicit caste marker in the prompt. 'Colorism in Multimodal AI' (Maurya, Shukla, Panat), EACL 2026 Student Research Workshop, Mar 2026 (https://aclanthology.org/2026.eacl-srw.69/): 210 occupations, 2,500+ portraits, three models; high-income prompts consistently produced lighter-skinned faces and prompt constraints only modestly reduced the effect, with GPT-4 Image-mini and Gemini-2.5 Flash-Image shifting more than Grok-2 Image. Direct bearing on rules/creative-generation.md section 4, which is written almost entirely as a negative list ('never generate gowns, ballrooms, marble lobbies, luxury cars') plus a one-line positive instruction to specify 'contemporary and ordinary rather than aspirational-luxury'. The evidence says the space the model falls into when pushed off luxury is not neutral. Caveat: neither paper tested advertising creative, neither tested the exact model or prompt skeleton in use here, and the failure has not been observed in any Riteangle asset - this is a predicted failure mode, not a diagnosed one.
