---
id: q-2026-08-26-why-the-lpv-counts-disagree
kind: tracking
status: open
asked: '2026-08-26'
raised_by: lrn-2026-08-26-snap-and-beacon-disagree-on-lpv
answered: null
learning: null
---

## Question

Why do Snap and pocket-dating-coach's own beacon disagree by roughly 39% on landing-page views for the same ad squad, and which of the two should the kill/double gate be read against?

## Why it matters

budget.md's gate fires at 50-100 landing-page views and this record declares landing-page views as its success metric, so the two systems cross the threshold at different times and could support different verdicts on the same run. Candidates worth separating before guessing: reporting lag and differing day boundaries; Snap counting an in-app-browser page load where our beacon needs JS to execute and survive an early bounce; different bot filtering; the beacon counting reloads. The direction matters too - Snap reading LOWER than first party is the opposite of the usual pixel-loss story, which is what makes this worth actually investigating rather than assuming.
