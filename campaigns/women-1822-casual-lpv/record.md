---
rec_id: rec-2026-08-21-women-1822-casual-lpv
network: snap
status: live
campaign_name: RA_TRAFFIC_GET_IN_PAN_TOF_202608
ad_set_name: WOMEN_18-22_CASUAL_LPV
ad_name: STORY_FOURTEEN-SUITORS_A_20260824
campaign_id: 6f8c30ab-ad74-4525-b441-f18ced852515
ad_set_id: 1b993192-30b9-47e5-9e1a-cd0f11607292
ad_id: 7f2b4ccc-a150-480d-9230-3bdc48ea9bfb
targeting_summary: 'Snapchat, women only, 18-22, pan-India, Android-weighted. CASUAL-SELECTIVE
  persona at the 18-22 treatment: wild-experiences/social-energy register, feminist-coded
  hook. Interests: Dating & Relationships, Travel, Lifestyle, Nightlife - deliberately
  not narrowed further. Pan-India rather than BLR-first as a stated deviation (targeting.md''s
  broader-audiences-win note for LPV objectives; BLR-narrow women''s set underperformed).
  Success metric: landing-page views, not signups.'
creative_ref: creatives/fourteen-suitors-w1822
destination_url: https://www.riteangle.dating/get/w
budget_cap_inr_per_day: 1000.0
duration_days: 5
created: '2026-08-21'
amended: '2026-08-26'
executed: '2026-08-26'
---

## Brief (proposed)

# Brief — women 18–22, casual-selective, LPV relaunch

## What triggered this

Direct ask (2026-08-21): "we are losing out on women... I need to push an ad for women."

Backed by the same-day `ad-audit` pass over 2026-07-22 → 2026-08-21:

- Women are **19 of 151 signups (12.6%)**, a 6.9:1 male skew.
- **Eight** women-targeted ad sets have run, spending **₹1,791**, for **zero attributed signups**.
- Of those eight, **four are flagged `paidButNoTraffic`** (₹924 charged for clicks that produced no
  landing-page view at all): `WOMEN_18-35_CASUAL_STORY_IND_LEADS` (₹484), `SC_F_19-30_India` (₹223),
  `RA_LEADS_WOMEN_18-34_IN_20260818` (₹188, still ACTIVE), `Female 18-22` (₹29).
- **Not one of the eight names conforms to `rules/naming.md`.** Per that file, a non-parsing name breaks
  the spend↔traffic join in `pocket-dating-coach`'s own analytics — which is a partial explanation for
  the zero-signup reading, independent of real performance.

## The actual finding this ad set acts on

`Female 18-22-LPV` is the **best-performing ad set in the account on tap rate** — 20.9%, n=110, CI
[14.4–29.4%], clearing `MIN_SAMPLE = 30`. Higher than the best men's set
(`MEN_25-40_CASUAL_STORY_IND-LPV`, 15.3%, n=295).

It is funded at roughly **₹44/day** against `rules/budget.md`'s **₹800–1,200/day** minimum viable
floor — about 5% of the floor. Per that file, anything below the floor is "a system check, not a real
experiment," because the delivery algorithm never exits its learning phase.

So the gap on women is not an untested hypothesis. **The winning women's audience has already been
found and is being starved, misnamed, and surrounded by four broken ad sets consuming half the
women's budget.** This recommendation relaunches that exact combination under a conforming name, at
the funding floor, with the tracking protocol actually applied.

## Persona and audience

`CASUAL-SELECTIVE` (`rules/targeting.md` persona #4), at the **18–22** age treatment specifically.

Per `targeting.md`, 18–22 creative should telegraph wild experiences — partying, travel, adventure,
social energy — and the Aug 9 note records that hard-hitting, feminist-coded copy ("Stop scrolling
through guys who just want attention") tests well in this band. That is the register here, not the
security/safety/loyalty register reserved for 25–30.

**Provider-energy handling:** this is the persona where `compliance.md` rule #1 bites hardest. The
creative sells the *verified lifestyle / social-currency* signal — travel history, an established
career, things proven rather than claimed — and never money, luxury, or being taken care of. Nothing
in the copy or the visual may imply a giver/receiver pair.

## Success metric

**Landing-page views** (matches the `LPV` signal and the `TOF` funnel stage in the campaign name).

Secondary read: store taps. **Not** signups — with the `snapchat`-vs-`snap` network-label split still
unfixed, only 7 of 151 signups in the whole account can be joined to an ad set that carries cost, so
signup count is not yet a trustworthy verdict metric for any ad set.

Kill/double gate per `rules/budget.md`: review at **3–5 days or 50–100 landing-page views**, whichever
comes first.

## Targeting

Snapchat, women only, 18–22, pan-India. A single-gender ad set per `targeting.md` ("never a
mixed-gender ad set"). Android-weighted device targeting, since the Play Store listing is the primary
install destination and iOS is TestFlight-only — confirmed by the analytics showing 81 Android
attributed members against 1 iOS member.

Interest categories drawn from `targeting.md`'s approved lifestyle list: Dating & Relationships,
Travel, Lifestyle, Nightlife. Deliberately **not** narrowed further than that.

**Geography — stated deviation.** `targeting.md` names Bangalore first, then Delhi/Hyderabad. This ad
set goes pan-India (`PAN`) instead, for two reasons drawn from that same file and from live data: (1)
`targeting.md` explicitly notes that for a web-landing-page traffic objective, "broader audiences often
outperform narrow ones early — let the platform's own delivery algorithm find who actually swipes up";
and (2) the BLR-narrow women's set `Women_18-30_BLR_Lifestyle_Auto` returned 22 views and 4 taps on
₹296, materially worse than the un-narrowed `Female 18-22-LPV`. If pan-India clears the tap-rate bar,
a BLR-concentrated MOF set is the natural follow-up.

## Creative

`creatives/` is currently empty apart from its README, so this is a **new asset to commission**, not an
existing one to reuse. It lands in `creatives/` per decision #11 once produced.

**Format:** Snap Story, vertical 9:16. Per `creative-style.md`'s production constraint, six seconds is
short and this product's best moments are conversations — so this is a **scripted, purpose-built
conversation asset**, not lifestyle stock footage, with the emotional beat landing in the first two
seconds.

**Beat 1 (0–2s) — the hook.** On-screen text: *"Stop scrolling through guys who just want attention."*
Cream ground, no imagery competing with the line.

**Beat 2 (2–4s) — the product.** The woman's ranked shortlist UI (an interface render that already
exists — per `creative-style.md`, brief from these rather than commissioning new illustration). Shows
an *ordered* list, which is the whole point against the flood.

**Beat 3 (4–6s) — the close.** Tagline: *"You finally have a shortlist that means something."* —
the women-specific site-native alternative, not the primary tagline. Wordmark lowercase **riteangle**.

**Supporting stat, optional overlay on beat 2:** "The median woman here has 14 suitors." A first-party
median, which `creative-style.md` explicitly sanctions quoting (rates and medians, never totals).

**Visual identity, per `creative-style.md`:** cream ground `#FFF3F0`, brand pink `#FF3B6B` for accent,
ink `#1B1020` for text, Gabarito throughout. **Light, not dark** — deliberate, since every major rival
ships dark creative and cream reads as the differentiator in-feed before a word is read. Amber and red
are functional status colours only and must not appear as decorative accents.

**Per `compliance.md` §6 and Sree's Aug 21 note:** Indian models, no visible AI-tool watermark, no AI
glitching artefacts. If any man appears, it must be an AI-enhanced portrait of the kind the product
itself renders — never a real unenhanced photo. 18+ throughout.

## Budget and duration

**₹1,000/day for 5 days — ₹5,000 total.**

Mid-point of `rules/budget.md`'s ₹800–1,200 minimum viable range, and 5 days is the outer edge of the
kill/double window. No deviation from the envelope: ₹5,000 against a ₹50,000/month budget of which only
₹3,434 has been spent in the last 31 days — the account is running at roughly a ₹8k/month pace and is
underspending, not overspending.

**Funding source — recommended.** Pause the three ACTIVE `paidButNoTraffic` ad sets, which are charging
for clicks that produce no landing-page views: `GET_ID_M_2840_ANDROID` (₹307), `SC_MEN_28-38_BLR_CASUAL`
(₹289), `RA_LEADS_WOMEN_18-34_IN_20260818` (₹188) — ₹785 recovered. Caveat carried over from the audit:
landing-page-view tracking itself appears to have broken around Aug 16 (views collapse to near-zero
while taps and signups continue), so a `paidButNoTraffic` flag may be instrumentation rather than a
misrouted URL. Check each ad's Website URL field before pausing.

## Open risk

This ad set's predecessor recorded 0 signups on a 20.9% tap rate. That is either (a) genuine
drop-off between the landing page and the Play Store for this audience, or (b) the network-label
attribution break hiding real signups. **This ad set cannot distinguish between the two.** Fixing the
`snapchat`→`snap` / `ig`→`meta` label join in `pocket-dating-coach` is what makes the difference
legible, and it should be treated as a prerequisite for any *scaling* decision that follows this test —
though not for running the test itself, since landing-page views are measured upstream of the break.

## Amendment (2026-08-24)

- Reason: Hook slug ATTENTION-SEEKERS is not in creative-style.md's ad-ready-threads vocabulary, which naming.md requires [HOOK] to draw from; the real hook is the flood. Repointing creative_ref at the prompt pack written 2026-08-24.
- `ad_name`: 'STORY_ATTENTION-SEEKERS_A_20260821' → 'STORY_FOURTEEN-SUITORS_A_20260824'
- `creative_ref`: 'creatives/story-attention-seekers-a' → 'creatives/fourteen-suitors-w1822'

## Amendment (2026-08-26)

- Reason: The women's destination now exists and is verified. /get/w deployed 2026-08-25, beacon endpoints fixed 2026-08-26 (pocket-dating-coach e9b45a83), tracking.md pre-launch checks passed against the live URL.
- `destination_url`: 'https://www.riteangle.dating/get' → 'https://www.riteangle.dating/get/w'

## Execution

- Date: 2026-08-26
- Campaign ID: 6f8c30ab-ad74-4525-b441-f18ced852515
- Ad set ID: 1b993192-30b9-47e5-9e1a-cd0f11607292
- Ad ID: 7f2b4ccc-a150-480d-9230-3bdc48ea9bfb
- Deviated from brief: Effective daily spend is Rs 300, not the Rs 1,000 proposed. The ad squad carries Rs 1,000/day but a campaign-level Daily spend cap of Rs 300 was set before launch and the lower figure binds. That is below rules/budget.md's Rs 800-1,200 minimum viable floor, so the delivery algorithm may not exit its learning phase. Treat a weak read as inconclusive rather than as evidence against this audience: the predecessor Female 18-22-LPV holds the account's best tap rate (20.9%, n=110) and was starved at ~Rs 44/day, which is the exact failure this recommendation was written to correct. Raising or clearing the campaign cap is what makes the result readable. Also created via ad-agent snap-push rather than by hand — first API-created ad set in this ledger.
