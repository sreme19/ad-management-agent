---
id: q-2026-08-27-min-sample-and-config-facts
kind: tracking
status: open
asked: '2026-08-27'
raised_by: null
answered: null
learning: null
---

## Question

Should MIN_SAMPLE=30 apply to configuration facts, or only to performance rates?

## Why it matters

On 2026-08-27 two first-party observations read directly out of Ads Manager — that the live Meta ads carry no UTM parameters, and that Meta binds the conversion dataset at account level rather than per ad set — were both forced to 'low' confidence by the MIN_SAMPLE=30 gate on n=7 and n=1. Neither is a statistical claim. Reading a configuration field on all 7 ads in the account is a CENSUS: there is no sampling error for n to guard against, and looking at 30 ads would not make the field any more empty. SPEC.md decision #6 imports the gate from ad-analytics.ts, where it correctly protects rates and verdicts computed over user behaviour. Applied to a config fact it inverts the meaning of the label: the strongest evidence available — direct first-party observation — gets filed as the weakest, and a future brief reading 'low' will correctly underweight something that is simply true. Both learnings now carry a 'CONFIDENCE LABEL IS A GATE ARTIFACT' preamble in their evidence, which works but is a workaround living in prose rather than in the model. Options: a separate source kind for observed configuration; exempting a census from the n floor; or accepting the distortion and relying on the preamble. Worth deciding before more config facts get filed as low.
