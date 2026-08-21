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
