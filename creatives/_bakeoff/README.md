# Creative bake-off harness — the command center

One brief, dispatched to many generation tools (and if useful, many LLMs for the
prompt), outputs collected here, scored on a fixed rubric, ranked, winner advanced
to the type pass and finished-asset QA, then to `propose`/`snap-push`.

**This Claude session is the command center.** Every directive, prompt, score, and
the deploy call is decided and logged here in the repo. Pixels are made elsewhere
(driven through the user's logged-in Chrome, per the 2026-08-27 decision) and
return to `round-*/candidates/` for judging. Nothing is judged by the pass that
wrote its prompt — QA is a second pass (`creative-generation.md` §10).

## Two layers
- **Command center (in-repo, invariant):** `rubric.md` (how candidates score),
  `tools.md` (the generation surface registry), and each `round-*/` (brief +
  candidate ledger + the pixels).
- **Generation surface (external):** the tools in `tools.md`, driven via Chrome.

## A round, start to finish
1. Write `round-N/brief.md` — the creative goal + a tool-agnostic prompt + per-tool tweaks.
2. Dispatch the same brief to each tool in the round's lineup (drive Chrome).
3. Save every output to `round-N/candidates/<tool>-<n>.<ext>`; log a row in `round-N/candidates.md`.
4. Score each against `rubric.md`. Hard-gate failures are eliminated regardless of craft.
5. Rank. Advance the winner (or best 2) to the type pass; re-cut losers only if a prompt clause explains the miss.
6. Write learnings back — which tool/prompt pattern won, per medium and persona. A candidate with no verdict taught nothing.

## Loop-engineering (the endgame, not yet)
Once a round runs clean by hand, the automatable spine is: dispatch → collect →
score against `rubric.md` → rank → advance. The rubric and the candidate ledger
are kept structured for exactly that. Generation stays human/browser until a
sanctioned API path exists — the repo holds no keys by design.
