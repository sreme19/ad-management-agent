# Compliance rules — hard constraints, not style preferences

Source: `master_Riteangle__marketing_requirement.docx` ("Hard Constraints" and "Creative Compliance
Checklist" sections) and `Sree_only_Riteangle__notes.docx` (Aug 9 log). These are enforced, not
aspirational: the iOS build was rejected by Apple under **App Store Guideline 1.1.4 ("compensated
dating")** on 2026-08-03, and the codebase now has an automated banned-vocabulary gate that fails the
build if the removed wording reappears anywhere.

**Every `ad-setup-loop` output must be checked against this file before it is considered ready.** If a
finished draft trips any rule here, that is a decision for the app owner, never a copy edit to quietly
fix and move on.

## 1. Money is never an attraction signal

Income, net worth, wealth bands, spending, generosity, and provider framing are forbidden as reasons
anyone is desirable, in ad copy or anywhere else user-facing. No lane may imply money, luxury, being
kept, or a giver/receiver pair. Financial verification exists only as an anti-fraud check, never as a
desirability signal.

**The one distinction that must be preserved, not flattened:** the matching *backend* is allowed to
model "provider energy" as a real preference some women in the casual segment genuinely have (see
`targeting.md`) — matching on a real preference is not the same claim as advertising on it. The ad copy
itself may never say it, imply it, or visually signal it (no luxury cars, no cash, no "he'll take care
of you" framing). Model it in the algorithm; never say it in the creative.

## 2. No purchase language

There are no in-app purchases, no subscriptions, no credits. Never write ad copy that implies otherwise.

## 3. Referral cash is never a rupee amount in-app or in ads

Referral cash is web + server-ledger only. The in-app entry point reads "Invite," never a dollar/rupee
figure. Ad copy referencing referrals follows the same rule.

## 4. Never call the membership "high-earning"

Approved phrasing: "identity-verified and established professionals." This is the only way to signal
quality of membership without tripping rule #1.

## 5. Scores are never verdicts on a person's worth

Profile Strength is bands + momentum + next actions, never a raw ranking, in-product. Don't invent ad
copy that implies a hard numeric ranking either ("you're in the top 3%" is off-limits unless it's a
literal, disclosed, first-party stat — see `creative-style.md` for what's actually measured and quotable).

## 6. Creative Compliance Checklist (run against every finished asset)

1. **Never show a man's real, unenhanced photo.** Every man's photo in the product is AI-enhanced; the
   raw photo never appears anywhere, at any stage. It must not appear in an ad either — use the
   AI-enhanced portraits the product itself would show.
2. **Label AI imagery.** All AI imagery is labelled in-product as generated from verified photos.
   Creative showing a portrait must not imply it's an untouched snapshot. (Sree's Aug 21 note: "No grok
   label," "Image itself should not have AI glitches," "Indian models" — the generated creative needs to
   look clean and Indian-context-appropriate, not carry a visible AI-tool watermark.)

   **Scope for paid social, decided by the app owner 2026-08-28.** The two sentences above pull in
   opposite directions on a generated portrait — remove the tool watermark and the image reads *more*
   like an untouched photograph, not less. That ambiguity was scored inconsistently on
   `creatives/moveon-properly-w2530` (the finished-asset gate marked §6.2 `pass` for covering the Gemini
   watermark; the §8 independent pass returned `escalate` for the same asset being unlabelled). It is
   settled here so no future asset re-argues it:

   - **The labelling obligation in sentence one is an in-product obligation.** A paid-social asset does
     not need an on-asset "AI-generated" mark. What it owes is sentence two: no visible AI-tool
     watermark, no AI glitches, and nothing that makes a false claim.
   - **A generated person MAY appear in Riteangle creative.** Photorealistic, unlabelled, addressing
     camera. That is ordinary advertising imagery.
   - **A generated person MAY NOT narrate a first-person experience of using Riteangle.** This is the
     actual line, and it is about the *claim*, not the pixels. "Move on toh karna hai — par dhang se."
     is a general statement and is fine. "Yahan har koi verified hai — main scroll nahi karti" spoken by
     a synthetic woman is a fabricated customer testimonial, and no watermark decision makes that
     acceptable. Copy in her voice about her own results is the trigger; a face is not.
   - **Consequence, recorded so it is not rediscovered:** the MOVE-ON-PROPER *still* is compliant and
     was cleared to enable. The MOVE-ON-PROPER *video* script in that same folder is **blocked** under
     this rule, because its 7-12s line is exactly the prohibited form. Casting a real person, or
     rewriting those lines out of first person, unblocks it.
   - **This scope is about `rules/compliance.md` only.** Meta and Snap each carry their own
     synthetic-media disclosure rules for ads, which bind independently and have not been checked here.
     A platform requirement to disclose AI imagery overrides this scope; it does not conflict with it.
3. **Eighteen and over, without exception.** Confirmed at verification; Snap's dating category carries
   its own 18+ and content restrictions on top of this.
4. **Run the copy through the banned-vocabulary gate** (or its wordlist, manually, until this repo has
   a direct way to invoke it) before shipping. This is the same gate that already caught five
   user-facing surfaces a careful manual review missed — ad copy is exactly the kind of surface where
   the removed vocabulary comes back.

## 7. Tone of voice — Don't list

Hype, salesy urgency, technical jargon in ads (don't say "data gap," "effort gap," "vectors," "game
theory" — translate to lived human feeling first, see `creative-style.md`), money/provider language,
ranking people, "high-earning" claims, purchase language.

## 8. Quality-check step before anything ships

Per Sree's own Aug 21 note: use a second, independent pass (a different model or a fresh session) to
check a finished ad against this file before it's considered ready to hand off for setup — don't let
the same reasoning pass that wrote the copy also be the only check that it's compliant.
