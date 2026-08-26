# Build sheet — Snap Ads Manager

`rec-2026-08-21-women-1822-casual-lpv` · built by hand, field by field. Nothing in this repo touches
Ads Manager; this is what you paste.

**Do not attach a Lead Form to this ad.** The lead-form objective is what produced the 98% male lead
flow — it optimises toward whoever submits cheapest, and men submit dating lead forms far more
readily. This ad set is optimised for landing-page views instead, which is also the metric it will be
judged on.

## 1 · Campaign

| Field | Value |
|---|---|
| Name | `RA_TRAFFIC_GET_IN_PAN_TOF_202608` |
| Objective | **Website Traffic** |
| Status | Paused while you build — enable only after step 5 |

An identically-named campaign may already exist. Reuse it rather than creating a second: two live
campaigns have shared a name with different ids before, which is why `pocket-dating-coach`'s rollup
keys on ad set, not campaign.

## 2 · Ad set

| Field | Value |
|---|---|
| Name | `WOMEN_18-22_CASUAL_LPV` |
| Optimisation goal | **Landing Page Views** — not Swipe Ups, not Impressions |
| Gender | **Female only** |
| Age | **18 – 22** |
| Location | **India**, no city narrowing |
| Interests | Dating & Relationships · Travel · Lifestyle · Nightlife |
| Device / OS | **Android only** |
| Daily budget | **₹1,000** |
| Schedule | **5 days**, then it stops |
| Placement | Snap Stories / between-content vertical |

**Age must read 18, never 17.** `compliance.md` §6.3 is absolute and Snap's dating category enforces
its own 18+ on top.

**Pan-India is a deliberate deviation** from `targeting.md`'s Bangalore-first rule, recorded in the
brief: the BLR-narrow women's set returned 22 views on ₹296, materially worse than the un-narrowed
set, and for a landing-page objective broad delivery usually wins early.

**Android only** because the Play listing is the install destination — iOS is TestFlight, and the
analytics show 81 Android attributed members against 1 iOS.

## 3 · Ad

| Field | Value |
|---|---|
| Name | `STORY_FOURTEEN-SUITORS_A_20260824` |
| Format | Single Image |
| Creative | `creatives/fourteen-suitors-w1822/asset-a.jpg` (1080×1920) |
| Brand name | `Riteangle` |
| Headline | `A shortlist that means something.` |
| Call to action | **More** |

The headline is 33 characters against Snap's 34 limit. It is the women-specific tagline from
`creative-style.md`, trimmed. **Not** "Sign up" as the CTA — that promises a form this ad set does not
run.

## 4 · Website URL — paste exactly, on the AD, not the campaign

```
https://www.riteangle.dating/get/w?utm_source=snapchat&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adSet.id}}&utm_id={{ad.id}}&utm_content={{ad.name}}
```

`utm_id={{ad.id}}` is the one `pocket-dating-coach` actually joins on for Snap. Do not assume Snap
appends it — that assumption silently cost a full week of spend on 2026-08-21.

Note the path is `/get/w`, not `/get`. `/get` is the men's page and the destination gate will refuse
any future proposal that points this audience at it.

## 5 · Pre-launch check — before you enable anything

1. Open the **ad's own** Website URL field and confirm all six parameters are present.
2. Click the ad's preview / swipe-up link. Confirm you land on `/get/w?...` with every macro resolved
   to a real value — a UUID for `utm_term` and `utm_id`, not a literal `{{adSet.id}}`.
3. Confirm the page you land on says **"Your list, already in order"**. If it says "Her AI talks to him
   first" you are on `/get` and the URL is wrong.

Only then enable the campaign. This takes under a minute and is the step the 2026-08-21 incident
skipped.

## 6 · After it is live

Send back the real **campaign id, ad set id and ad id**. They get logged with:

```
ad-agent log-setup rec-2026-08-21-women-1822-casual-lpv --network snap \
  --campaign-id <real> --ad-set-id <real> --ad-id <real>
```

Within the first hour, the post-launch check runs against live rows — confirming arrivals carry a real
`utm_id` rather than the landing page's default. `log-setup` is not complete until that has passed once.

## 7 · When to judge it

Per `budget.md`: review at **3–5 days or 50–100 landing-page views**, whichever comes first, then kill
or double.

Do not read tap rate before **30 events** — below `MIN_SAMPLE` the endpoint returns `null` rather than a
rate, on purpose. A null there is the gate working, not a broken number.

**This is a single-ad launch.** Variant B is blocked on the ranked-shortlist render and C is unbuilt, so
this test answers "does the audience-plus-destination fix work," not "which creative wins."
