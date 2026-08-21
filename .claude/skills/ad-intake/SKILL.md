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
5. **Decide whether this is worth turning into an idea.** If yes, write it up the same way
   `ad-ideation` would — persona, hook, why now, estimated spend, compliance check, `recommend`/`hold`
   verdict — and offer to hand it to `ad-setup-loop` if the user approves it. If the lesson is more
   general (a tone shift, a stat worth stealing the *idea* of quoting, not the number itself), just log
   the observation plainly rather than forcing it into a formal idea.

## What this skill never does

Never suggest replicating a competitor's copy or imagery directly — Riteangle's own compliance rules
(`rules/compliance.md`) and visual identity (`rules/creative-style.md`) are stricter than most
competitors', and the point of this skill is extracting the *why it works*, not the *what to paste*.
