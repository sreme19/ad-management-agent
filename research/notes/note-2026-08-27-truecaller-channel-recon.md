---
id: note-2026-08-27-truecaller-channel-recon
title: "Truecaller as a third ad network \u2014 channel recon"
source: platform-doc
captured: '2026-08-27'
learnings:
- lrn-2026-08-27-truecaller-selfserve-exists
- lrn-2026-08-27-truecaller-access-is-gated
- lrn-2026-08-27-truecaller-business-is-not-ads
- lrn-2026-08-27-truecaller-ad-business-shrinking
- lrn-2026-08-27-truecaller-skew-is-unestablished
- lrn-2026-08-27-truecaller-registry-entry-is-honest-blocker
---

# Truecaller as a third ad network — channel recon, 2026-08-27

Driven through the operator's logged-in Chrome. Every URL below was visited in
this pass; nothing here is from memory.

## What exists

- **`adsmanager.truecaller.com` — "Truecaller Ads Manager", the self-serve platform, and it is
  alive.** Built on DanAds (self-serve ad-booking vendor; the Truecaller/DanAds partnership dates
  to a late-2017 launch aimed explicitly at India and Africa). Its own landing copy states:
  four-step booking (placement -> targeting -> creative -> budget/schedule), payment via Adyen,
  campaigns can start serving "in just 48 hours", A/B testing across creatives, self-serve pause
  and targeting edits, automated email reports. A "50% off your first campaign" promo is offered.
- **Targeting axes named on the public page:** location, age, gender, and "what products they
  could be searching for on Truecaller's app" — i.e. some intent/search signal we have no analogue
  for on Snap. Third-party media resellers additionally describe carrier, handset and day/time
  targeting, but that is reseller copy, not Truecaller's own.
- **Billing currency includes INR** (options offered: EUR, USD, INR, KES, SEK). The registration
  form's timezone also pre-selected (UTC+05:30) Chennai/Kolkata/Mumbai/New Delhi from our IP.
  So India is a first-class billing market, and ledger figures in rupees map 1:1 with no FX step.

## What does NOT exist

- `ads.truecaller.com` -> 404. `www.truecaller.com/ads` -> 404. `business.truecaller.com/advertising`
  -> 404.
- **`business.truecaller.com` ("Truecaller for Business") does not sell audience advertising at all.**
  Its Products menu is Verified Caller ID / Verified Messages / Verified Campaigns / Business Chat,
  then Dialing Intelligence / Number Intelligence, then User Authentication. Advertising is not in it.
  That site is a sales-led B2B motion ("Get in touch"), and it is a different product from Ads Manager.
  Worth knowing so we don't chase the wrong funnel.
- **No public spec sheet, rate card, minimum budget, or creative-size list anywhere.** The only
  "Support" surface on Ads Manager is a contact form (`/contacts`, and a `adsmanager@truecaller.com`
  mailto on error pages). Placements, minimum spend and creative dimensions are all behind the login.

## Access is gated, and the gate ends in a CAPTCHA

"Register" routes to **`adsmanager.truecaller.com/request-access`**, not to an open signup.
Flow: pick **Direct advertiser** (vs Agency) -> a single form -> submit -> Truecaller emails back
a promo code / access. Fields, in order:

- Contact: Name, Company Name, Email Address, Confirm Email Address, "I confirm that this is a
  company email" checkbox.
- Advertiser Information: Phone Number (country-coded), Country, City, State/Province, Street & No.,
  Zip/Post Code, Time Zone, Website, "I confirm that this is a company address" checkbox,
  Company description.
- Billing Address: default-or-different toggle, VAT number (or an "I don't have VAT Number" checkbox),
  Currency.
- Then **Google reCAPTCHA ("I'm not a robot")** and SUBMIT.

The reCAPTCHA and the company/billing identity data make this a human step by construction — the
agent cannot complete it, and shouldn't.

## The surrounding advertiser site is stale

`advertisers.truecaller.com` (linked from Ads Manager as "Back to Truecaller Ads") still reads
**© 2023 Truecaller AB**, its `/brand-stories` page returns a Nuxt server error, and `/audiences`
redirects to a login. Its headline product is described as "Brand Ads" — themed notifications on
incoming and missed calls — with community stats quoted at 450M MAU / 1B+ downloads.

## The business context, which is not encouraging

From public reporting, not from Truecaller's own advertiser pages:

- Truecaller advertising revenue fell from SEK 331m (Q2 2025) to SEK 200m (Q2 2026), ~40% down;
  Q1 2026 was -44% in SEK / -34% constant currency.
- Cause: roughly one third of ad traffic from its largest demand partner (reported as Google) was
  lost after an August 2025 algorithmic flag on Truecaller's inventory. The flag was reported removed
  around June 2026, with Truecaller itself saying it is too early to call the long-term impact.
- ~70 roles cut in the ad business (reported May 2026). Recurring revenue (Premium + Truecaller for
  Business) is now ~47% of sales vs 32% in Q1 2025 — the company is deliberately rotating away from ads.

Two readings, both plausible and neither yet evidenced: distressed inventory may be cheap for a small
advertiser, or a shrinking ad org means a stale self-serve product and thin support. The © 2023 site
and the broken page are weak evidence for the second.

## Audience skew — NOT established

The only gender figure findable publicly is Similarweb's, and it is **truecaller.com website traffic
(~60% male / 40% female), not the Indian app user base.** That is a different population from
350M+ Indian app MAU and must not be used as the app's split. This matters more than any other open
item: `rules/destinations.yaml` records that the first live lead campaigns produced 98% male
submissions and 100% male `/get` store taps, and `rules/budget.md` prices women at ~8x men
(~Rs 200 vs ~Rs 25 per signup) precisely because women are the scarce side. If Truecaller's Indian
audience skews male, it supplies more of the side we already oversupply, and the channel is a
distraction regardless of how cheap the CPM is.

## Sources visited
- https://adsmanager.truecaller.com (+ /contacts, /request-access, /login)
- https://business.truecaller.com (+ Products menu, /advertising -> 404)
- https://advertisers.truecaller.com (+ /audiences -> login, /brand-stories -> 500)
- https://www.truecaller.com/ads -> 404
- danads.com Truecaller partnership announcement; investing.com / telecompaper / prnewswire /
  androguider coverage of Q1-Q2 2026 ad revenue; Similarweb truecaller.com audience panel.
