# Competitor landing pages vs Riteangle's Snap destinations — Aug 26, 2026

Triggered by the current Snap campaign sending traffic to `/get` (men) and `/get/w` (women) — see
`rules/destinations.yaml` for what those pages are and why the split exists. Goal stated by Sree:
figure out how to make the women's landing page more welcoming and better at capturing real leads.

Same tooling limitation as the Instagram probe (`../index.md`): pages viewed and read in full, text
and screenshots inspected directly, but files could not be persisted to this folder — see queued links
below to save any of these by hand.

## Queued links (open and review directly)

- Riteangle men's: https://www.riteangle.dating/get
- Riteangle women's: https://www.riteangle.dating/get/w
- Aisle marketing site: https://www.aisle.co/
- Aisle App Store listing + reviews: https://apps.apple.com/in/app/aisle-indian-dating-app/id1001481078
- TrulyMadly: https://trulymadly.com/
- Shaadi.com: https://www.shaadi.com/
- (dead end) betterhalf.ai — domain now redirects straight to a Play Store search, no landing page live

## The core finding: Riteangle has no lead-capture mechanism at all

Both `/get` and `/get/w` have exactly one CTA, repeated three times down the page: **"Get the Android
app"**, a straight link to the Play Store. There is no email field, no phone field, no "notify me,"
nothing that captures a contactable lead before the visitor leaves riteangle.dating. Every competitor
landing page below captures something *first*:

| Site | First ask | Mechanism |
|---|---|---|
| **TrulyMadly** | Phone number, above the fold | OTP-style mobile capture form sits directly in the hero, before any value-prop copy. The visitor commits before they've even scrolled. |
| **Shaadi.com** | A guided preference picker, above the fold | "I'm looking for a [Woman] aged [22–27] of religion [—] and mother tongue [—] → Let's Begin." Four dropdowns embedded in the hero image. This isn't a lead form yet — it's a warm-up: get a small, easy commitment before asking for contact info on the next screen. Classic foot-in-the-door pattern, and it's sitting on India's highest-volume matrimony site for a reason. |
| **BharatMatrimony** | Name + phone number, above the fold | Same OTP-capture pattern as TrulyMadly — "Profile created for [self/daughter/son/...] → Enter the name → Enter Mobile Number → Register Free," with the OTP flow directly under the hero headline. Confirms this is the category-standard pattern across matrimony players, not a one-off from a single competitor. |
| **Aisle** | Nothing — same as us | `aisle.co` is a pure brand/culture site (mission statement, couple stories, press). Their actual paid-traffic destination is a `bit.ly` deep link straight to the App Store listing — no custom landing page at all. Aisle's real "lead capture" happens inside the app-store install, same structural gap we have. |
| **Riteangle** | Nothing | Play Store button, three times. The "lead" is a Play Store click, which is a worse signal than a phone number: no way to re-contact someone who clicks and doesn't install, or installs and drops off before verifying. |

**This is the single highest-leverage fix available.** If the stated goal is capturing real leads of
women — not just app installs — `/get/w` needs a first-party capture step (phone or email) before or
alongside the Play Store button, the way TrulyMadly, Shaadi.com, and BharatMatrimony all do — three
independent matrimony/mass-market players converging on the identical pattern is a strong signal it's
not incidental. Right now every visitor who isn't ready to install Android-only software on the spot is
lost with no way to follow up. Given `rules/targeting.md` already flags that broad top-of-funnel traffic
often outperforms narrow targeting early on, an uncaptured drop-off here is compounding — Snap spend is
buying visits that leave no trace.

BharatMatrimony's footer also carries one explicit differentiation line worth noting: *"This website is
strictly for matrimonial purpose only and not a dating website."* Matrimony players draw that line
loudly; it's a reminder that `/get/w`'s own copy sits deliberately between dating and matrimony
(`rules/targeting.md`'s "dating → matrimony" direction) and should keep doing so on purpose, not by
default.

## What "welcoming" looks like on the competitor pages, concretely

- **Shaadi.com leads with a personalization question, not a pitch.** The first thing a visitor does is
  answer a question about *their own* search, not read four bullet points about the product. That's
  what "welcoming" cashes out to in practice — the page performs like a conversation, not a brochure.
  `/get/w`'s hero is copy-identical in structure to `/get`'s (same H1, same sub-head, same button) with
  only the comparison-table and stat bullets swapped underneath — the page still opens by talking *at*
  her rather than asking her anything.
- **Trust badges sit next to the ask, not three scrolls below it.** Shaadi.com stacks "30-Day Money
  Back Guarantee / Blue Tick = 40% more requests / 80 Lakh Success Stories" directly under the hero
  form. Riteangle's strongest first-party numbers (14 suitors ranked, 2:1 ratio, 54% AI-sent messages,
  12-min median) are real and better than anything a competitor can cite — but they land after the
  fold, past the point most visitors have already decided whether to trust the page.
- **TrulyMadly names "Safety For Women" as a standalone feature pillar** (no screenshots or downloads
  of profile photos allowed in-app) — a concrete, believable safety mechanic, not a generic "we care
  about safety" line. `/get/w`'s closest equivalent ("Proof, never stored — he proves it, you never see
  the file") is actually a stronger and more specific claim than TrulyMadly's, but it's buried in a
  six-item feature grid near the bottom rather than positioned as the headline trust signal.
- **A real complaint from Aisle's own App Store reviews is directly relevant here**: a 1-star review
  says the app "even asks ur salary... too shallow... isn't love supposed to be blind?" — this is
  first-party evidence, from an actual user, of exactly the reaction `rules/compliance.md` rule #1 and
  the provider-energy ban in `rules/targeting.md` are designed to prevent. It's usable as supporting
  evidence the next time that rule needs defending, not just an internal hypothesis.

## Recommendations for `/get/w`, in priority order

1. **Add a lead-capture step** — phone or email, inline or as a lightweight "get notified when iPhone
   ships" / "we'll text you the download link" moment — so a Snap visitor who bounces before installing
   still becomes a contactable lead. This is the gap nothing else on this list fixes.
2. **Pull one stat (14 suitors, ranked) and the "proof never stored" claim up next to the hero CTA**,
   not just lower on the page — competitor pages put trust signals where the decision actually happens.
3. Consider a light interactive moment before the CTA (Shaadi.com's pattern) — even something small
   like "what matters most to you: security, adventure, or both?" mapping to the `CASUAL-SELECTIVE`
   vs `25–30` creative split already defined in `rules/targeting.md` — to make the page feel like it's
   responding to her rather than reciting at her.
4. Not a page fix, but adjacent: Aisle's own paid funnel (Instagram bio → bit.ly → App Store, no
   landing page) is the one competitor pattern *not* to copy — it's structurally identical to our
   current gap, not a model to follow.

This is a landing-page/product change, not something `ad-agent` or the ad rules can act on directly —
flagging it here as ad-ideation/ad-setup-loop input per Sree's ask; the actual page edit belongs to
whoever owns the `pocket-dating-coach` routes (per the note already in `rules/destinations.yaml` about
`/get/w`'s deploy history).
