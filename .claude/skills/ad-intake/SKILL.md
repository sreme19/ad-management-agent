---
name: ad-intake
description: Process an ad the user found elsewhere (a screenshot, a description, a link to a competitor's Meta/Snap ad) — learn what it's doing and why, and optionally turn it into an idea for ad-setup-loop. Use whenever the user pastes or describes an ad they discovered outside this workflow, especially a competitor's.
---

# Learning from a discovered ad (mode 8)

The user's habit: they see an ad somewhere (Meta Ads Library, Snap, a screenshot from their own feed)
and brings it here to learn from. This is the direct analog of job-hunt-agent's
`linkedin-opportunity` skill — read what's in front of you directly, don't guess at what a screenshot
shows.

## Procedure

1. **Read what's actually there.** If it's an image, it's already in your context — extract the hook,
   the visual style, the claim being made, the call to action, and (if visible) which network and
   roughly which audience it's aimed at. If it's a link or description, work from that.
2. **Identify who's running it**, if known, and check it against `rules/creative-style.md`'s
   "Competitive landscape" — is this a known player doing something consistent with their positioning,
   or something new from them?
3. **Say what it's doing well or poorly, specifically** — not "this is a good ad" but "this leads with
   [specific hook] in the first two seconds, which works because [reason]" or "this makes a claim
   Riteangle couldn't make honestly because [compliance reason]." Ground it in the actual creative, not
   generic ad-copy commentary.
4. **Check it against `rules/compliance.md` before drawing any lesson from it.** A competitor doing
   something Riteangle's product rules forbid (implying money/provider energy, an unverified claim, a
   real male photo) is a lesson in what *not* to copy, not a template.
5. **Store what you were given, verbatim.** Before deriving anything, snapshot the raw material —
   the description, the pasted copy, the notes the user brought:
   ```
   ad-agent ingest --title "..." --source competitor-observation|own-research|platform-doc \
     (--text "..." | --file /path) [--slug short-id]
   ```
   Notes are immutable: the content *is* the provenance a claim points back at, so a second ingest
   under the same id is refused rather than merged. If the source is an image already in your context,
   write down what you actually see in it — the note is what someone reads in three months, and the
   screenshot will not be there.

6. **Derive the lesson as a learning**, linked to that note:
   ```
   ad-agent learn --claim "..." --subject creative|competitor|channel|audience|product \
     --source competitor-observation --confidence medium --evidence "..." \
     --derived-from <note-id> [--slug ...]
   ```
   A competitor observation **cannot be `high` confidence** — the gate refuses it. That is deliberate:
   what a rival is visibly doing is a hypothesis about what works, not a measurement of it.

   This is the step that used to be "just log the observation plainly," with nowhere to log it. An
   observation that stays in the session teaches nothing, which is precisely how
   `rules/targeting.md` ended up carrying dated notes with no source attached.

7. **Raise a question if the ad prompts one you cannot answer** — why a format works, what it costs,
   whether a claim is substantiated:
   ```
   ad-agent question --text "..." --kind creative|competitor|channel|... --why "what it unblocks"
   ```

8. **Decide whether this is worth turning into an idea.** If yes, write it up the way `ad-ideation`
   does — `ad-agent idea` with persona, spend, `recommend`/`hold`, and `--learning` pointing at what
   you just derived — and offer to hand it to `ad-setup-loop` if the user approves. If the lesson is
   more general, the learning above is already the right home for it; don't inflate it into an idea to
   feel finished.

## Check for it first

Run `ad-agent open` or look through `research/learnings/` before writing a new atom. If this ad
restates something already recorded, that is `ad-agent log-evidence <lrn-id> --outcome supported
--text "..."` on the existing claim, not a second file making the same point. `learn` prints existing
learnings on the same subject for exactly this reason — read them before accepting the new one.

## What this skill never does

Never suggest replicating a competitor's copy or imagery directly — Riteangle's own compliance rules
(`rules/compliance.md`) and visual identity (`rules/creative-style.md`) are stricter than most
competitors', and the point of this skill is extracting the *why it works*, not the *what to paste*.
