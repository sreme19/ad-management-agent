---
id: q-2026-08-29-pocket-dating-coach-s-scripts-check-banned-strings-sh
kind: tracking
status: open
asked: '2026-08-29'
raised_by: null
answered: null
learning: null
---

## Question

pocket-dating-coach's scripts/check-banned-strings.sh — the Guideline 1.1.4 regression gate that exists because the iOS build was rejected for compensated-dating framing — is entirely English. Its patterns are phrases like 'picks up the bill' and 'wined and dined'. Nothing in it can match kharcha, paisa, ameer, bill uthane wala or kharche uthata hai. Should the wordlist carry Hindi and romanised-Hindi equivalents?

## Why it matters

Riteangle is about to write Hindi copy on /get/w-apply and in Meta ad creative, which is exactly the surface the gate was built to guard, and the app owner's own first framing of the women's positioning included 'dating a rich guy, cruises, trips'. The gate scans src/routes/get, so the new page IS in scope — but it is blind to the language the new copy is written in. A gate that cannot see the copy it guards is worse than a known gap, because it reports clean.
