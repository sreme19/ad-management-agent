# Ads Manager setup checklist — RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608

Route (a): manual creation, decided 2026-08-29. Covers BOTH ad sets
(rec-2026-08-29-moveon-lead-w1824-meta and rec-2026-08-29-moveon-lead-w2530-meta).
Work top to bottom; every field that has burned us before is marked WHY.

## 0. Before opening Ads Manager

- [ ] Finish the asset: Gabarito type, Meta Sound Collection track (shape: sparse -> bloom at 8s ->
      full at 13s), 1080x1920 render, watermark CROPPED not delogo'd. The rough is the picture
      lock, not the upload.
- [ ] Native-speaker read of every Hinglish line (asset + form + this copy). SPEND gate — you can
      build everything below and leave it paused without this; you cannot enable.
- [ ] Compliance §8 independent pass on the finished asset, in a fresh session.

## 1. Campaign

| field | value |
|---|---|
| Buying type | Auction |
| Objective | **Leads** |
| Campaign name | `RA_LEADS_GETW-APPLY_IN_PAN_TOF_202608` |
| Special ad categories | **Dating** — declare it; being flagged later is worse |
| Advantage campaign budget (CBO) | **OFF** — WHY: meta-push refuses CBO because it silently ignores ad-set budgets; the same logic binds a manual build |

## 2. Ad set A (repeat for B with the age band changed)

| field | value |
|---|---|
| Name | `WOMEN_18-24_CASUAL_MOVEON-LEAD` (B: `WOMEN_25-30_...`) |
| Conversion location | **Instant forms** |
| Performance goal | Maximise number of leads |
| Facebook Page | the riteangle page (id in config.local.yaml -> meta.page_id) |
| Budget | **Rs 300/day** |
| Schedule | start paused-now, end +5 days once enabled |
| Location | India (country, not a city) |
| Age | 18–24 (B: 25–30) |
| Gender | **Women** |
| **Advantage detailed targeting / audience expansion** | **OFF** — WHY: commit a29fe59; omitting it means ON, and expansion-off is the whole 98/2 defence |
| Detailed targeting | leave broad — gender+age+OS carry the test |
| Operating system | **Android only** — WHY: standing owner directive 2026-08-28; iOS has no app |
| Placements | Advantage+ is fine (video is 9:16; feed crops centre-safe) |

## 3. Instant form (build once, attach to both ads)

- Form name: `RA_LEAD_GETW-APPLY_202608`
- Type: **More volume** (autofill; the friction thesis)
- Intro: optional — skip for v1, the ad did the selling
- Questions, exactly three, all autofill: **First name · Phone number · Email**
- Privacy policy: `https://www.riteangle.dating/privacy-policy` (verified 200, 2026-08-29)
- **Thank-you screen** — the funnel hinge:
  - Headline: `Bas ek step baaki hai` · Body: `Aapka apply almost complete hai.`
  - Button: **View website** → `Complete karo`
  - URL, ad set A (utm_term/utm_content filled with REAL ids after creation — placeholders never):
    ```
    https://www.riteangle.dating/get/w-apply?utm_source=fb&utm_medium=paid_social&utm_campaign=WOMEN_18-24_CASUAL_MOVEON-LEAD&utm_term=<ADSET_ID>&utm_content=<AD_ID>&ra_lead={{lead_id}}
    ```
  - WHY literal: unresolved macros cost a week of unattributable spend on 2026-08-21;
    `{{lead_id}}` is the ONE macro that must stay a macro — it is the whole join.
  - B gets its own URL with its own campaign/ids — do not share one URL across ad sets.

## 4. Ad (one per ad set, same creative)

| field | value |
|---|---|
| Name | `VID_MOVE-ON-PROPER_A_20260829` |
| Format | Single video, 9:16, 1080x1920 |
| Primary text | `Ghosting. Fake profiles. Teen hafte ki texting jo kahin nahi jaati.` / `Ab samajh aaya energy kahan jaati hai?` / `Date mat karo. Bas milo, aur jiyo.` / `Riteangle har aadmi ko verify karta hai — usse pehle ki woh aap tak pahunche.` |
| Headline | `Apply karo — sirf 18+` |
| Description | `Abhi sirf Android par.` |
| CTA button | **Apply Now** |
| Copy status | ran clean against the 1.1.4 wordlist 2026-08-29 (18 patterns, 0 hits) — the wordlist is English-only and cannot see Hindi (q-2026-08-29-...banned-strings-sh), so the native-speaker read doubles as the Hindi compliance read |

## 5. Leave everything PAUSED, then

1. `ad-agent log-setup` both recs with the real campaign/ad-set/ad ids.
2. Paste the real ids into both thank-you URLs (step 3) — they didn't exist until now.
3. Tracking pre-launch check (rules/tracking.md): open each ad's preview, tap through, confirm
   /get/w-apply loads with every param resolved and `ra_lead` present.
4. One test submission end to end: form -> thank-you -> page -> age tap -> confirm the row in
   `marketing_apply_gate` carries your ra_lead. Delete the test lead in Meta after.
5. Enable is YOUR click, never automated. Within the first hour: post-launch check — rows in
   `marketing_page_views` under page=get_w_apply with real utm_term, not the default.

## 6. Standing numbers

- Kill: **>30% of week-1 leads male** -> pause both ad sets, diagnose before respending.
- Kill/double: 3–5 days or 50–100 leads, whichever first.
- CSV pull: **Sree, daily**, from Meta Lead Center. Under-18 rows (flagged by
  `marketing_apply_gate.qualified=false`) are DELETED in Meta, not skipped — DPDP.
- Expected verdict at Rs 300/day: `inconclusive` on A-vs-B; the test answers "do women submit".
