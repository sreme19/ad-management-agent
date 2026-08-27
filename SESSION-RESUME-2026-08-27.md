# Session resume — 2026-08-27 (creative bake-off + competitor scan)

Pick-up point for a new session (account switch). Everything below is on disk in
this repo. Read this first, then `uv run ad-agent open`.

---

## 1. The headline state — where to resume

**A finished, QA-passed ad creative exists and is one banned-vocab check away from
being proposable.**

- Finished asset: `creatives/moveon-properly-w2530/asset-c5-a.jpg` (1080×1920, Snap Story)
- It is the MOVE-ON-PROPER breakup re-entry hook, women 25–30, Snap, `/get/w`.
- Idea it came from: `ideas/idea-2026-08-27-breakup-reentry-second-chapter.md` (verdict `recommend`).
- Brief for propose: `/tmp/brief-moveon.md` was written in-session and is EPHEMERAL —
  regenerate it from the "Deployment brief" section below; do not rely on /tmp.

### The exact next 3 steps to ship (all still to do)
1. **Banned-vocabulary check** on the copy — run `pocket-dating-coach`'s
   `check-banned-strings.sh` (or its wordlist manually) against:
   - "Move on toh karna hai — par dhang se."
   - "He's vetted before he ever reaches you." (beat 2, if used in video later)
   - "Verified, not vibes."
   This is the one open item on `creatives/moveon-properly-w2530/qa.md`.
2. **`ad-agent propose`** (see brief below), with `--creative-ref creatives/moveon-properly-w2530`
   and `--from-idea idea-2026-08-27-breakup-reentry-second-chapter`.
3. **`ad-agent snap-push <rec_id> --dry-run`** then real (creates PAUSED). Then the
   pre-launch tracking check (`rules/tracking.md`). NEVER enable — that's the user's action.

### Deployment brief (reconstruct /tmp/brief-moveon.md from this)
- Campaign: `RA_TRAFFIC_GETW_IN_BLR_TOF_202608`
- Ad set: `WOMEN_25-30_CASUAL_MOVEON-LPV`
- Ad: `STORY_MOVE-ON-PROPER_A_20260827`
- Targeting: women, 25–30, Bangalore, expansion off. Persona CASUAL-SELECTIVE
  (security-register end of the 18–28 band, per the Aug-5 age split).
- Destination: `https://www.riteangle.dating/get/w` (audience: women — gate passes)
- UTM (on the AD's own URL): `?utm_source=snapchat&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adSet.id}}&utm_id={{ad.id}}&utm_content={{ad.name}}`
- Budget: ₹1,000/day × 5 days. **Parent campaign cap must be ≥ ₹1,000/day** or snap-push refuses (the ₹300 incident).
- Carried risk: no comment-moderation policy exists for the hostility a breakup hook attracts. Surface again at propose.

### TWO naming-file gaps to fix before names are final (flagged, not yet edited)
- `rules/naming.md` has no token for `/get/w` — I used `GETW`. Add the row.
- `MOVE-ON-PROPER` is not in `rules/creative-style.md`'s ad-ready-threads vocabulary
  (which `naming.md` requires `[HOOK]` to come from). Add it, or map to an existing thread.

---

## 2. The creative bake-off — the harness, proven this session

`creatives/_bakeoff/` is the command center: one brief → many tools → scored on a
fixed rubric → winner advances. Driven through the user's logged-in Chrome (this
repo holds no API keys by design).

- `_bakeoff/README.md` — how a round works + the loop-engineering endgame
- `_bakeoff/rubric.md` — scoreable gates + 5 weighted dims (/37.5)
- `_bakeoff/tools.md` — tool registry + which tool wins which lane
- `_bakeoff/round-01-moveon/` — brief, candidate ledger, and 5 candidate images

### Round-1 result (candidates.md has the full scores)
| id | tool | score | note |
|----|------|-------|------|
| **c5** | Gemini (fresh chat) | **36.5** | **WINNER, Sree-approved.** Beautiful, chic boy cut, dusty-rose tee, cream Indian home, POV-speaker. `gemini-3-beautiful.png` |
| c3 | Gemini | 36.5 | plainer subject; superseded by c5 |
| c1 | ChatGPT | 34.0 | strong alt, cleanest empty wall for type |
| c4 | Gemini (edit) | 33.5 | polished but anchored to plain subject |
| c2 | Grok | 20.0 | out — defaults dark/cinematic |

### Durable learnings from the bake-off (also in tools.md / candidates.md)
- **Cream-UGC reproduces on ChatGPT AND Gemini**; Grok defaults dark/cinematic even when told cream. Route cream lane to Gemini/ChatGPT.
- **Gemini edits anchor hard to the established subject** — for a distinctly different face, start a FRESH chat, don't edit.
- **Attractiveness ≠ object-of-desire.** The guardrail (agreed with Sree): "hot and confident, addressing you" = fine; "posed for the viewer's desire" = the documented 98/2 male-recruitment trap. The rubric under-weights casting appeal (only shows in stop-scroll) — add an explicit "casting appeal" dim next round.
- **The dishevelled first result was a prompt fault** ("not glossy / slightly imperfect / muted"). For attractive-but-POV-correct: "beautiful, radiant, put-together, confident, talking to camera" + rely on the negative list.

### Type pass — programmatic, no Figma/Canva needed
`creatives/moveon-properly-w2530/typeset.py` (Pillow + real Gabarito) sets all type,
crops the Gemini ✦ watermark under a cream footer, exports 1080×1920. Re-cut any
variant with: `uv run python creatives/moveon-properly-w2530/typeset.py`
(Pillow is installed in `.venv`; Gabarito is read from the pocket-dating-coach repo.)
Decision recorded: buy neither Figma nor Canva — the programmatic route is free AND
is the loop-engineerable path. Grok text overlay is fine for throwaway comps only
(§2: samplers garble the lowercase `riteangle` wordmark).

---

## 3. Competitor scan (earlier in the session) — already committed as 084762c

16 accounts, 9 transcribed reels, 30+ posts. 9 notes / 13 learnings / 3 questions
in `research/`, 56 reference images in `creatives/_competitor-reference/` (gitignored
media, tracked prose). The big finding: the FLOODED-WOMAN persona is probably
inverted — every creator observed complains about QUALITY of what reaches her, not
volume. See `research/questions/q-2026-08-27-is-the-riteangle-woman-flooded.md` —
worth resolving before the 31-Aug `women-1822-casual-lpv` review.

Recovery know-how (in `creatives/_competitor-reference/sources-2026-08-27.md`):
`facebookexternalhit/1.1` UA unlocks any public IG post's og:image (640px);
full-res needs a logged-in `/api/v1/feed/user/<id>/` call. The old sweep's claim
that competitor CDN assets can't be saved was wrong.

---

## 4. The loop-engineering endgame (not started — the next big task)

Once deployment is done once by hand, automate: dispatch → score (fan candidates to
cheap subagents so the command center never ingests pixels — this is the token fix)
→ typeset → QA. The rubric and candidate ledger are already structured for it.
Generation stays browser/human until a sanctioned API path exists.

---

## 5. Housekeeping notes for the next session
- `uv run ad-agent open` shows 3 recommended-but-unproposed ideas (moveon, UGC-women, hinglish-headline) and 9 open questions.
- The moveon idea and the standing `ugc-format-womens-creative` idea should be FOLDED — same testimonial bet. Don't run duplicates.
- `git push origin main` was blocked by the auto-mode classifier in-session; push may need to be done manually.
- Model economy: image ingestion costs the same on any model; run the capture/score grind on Sonnet, keep Opus for strategy, and fan scoring to subagents when automated.
