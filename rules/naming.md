# Naming convention

Source: Sree's Aug 7 log (already in production use — confirmed against live `ad_spend_daily` /
`marketing_page_views` rows in `pocket-dating-coach`, e.g. `RA_TRAFFIC_GET_IN_BLR_TOF_202608`). Every
`ad-setup-loop` recommendation must use this convention exactly — a name that doesn't parse breaks the
join between spend and traffic in `pocket-dating-coach`'s own analytics (see
`ad-analytics.ts`'s `adSetKeyOf`/name-reconciliation logic, which exists specifically to patch up
naming drift).

## Campaign

```
RA_TRAFFIC_GET_IN_[GEO]_[FUNNEL]_[YYYYMM]
```

Example: `RA_TRAFFIC_GET_IN_BLR_TOF_202608`

| Part | Meaning | Example |
|---|---|---|
| `RA` | RiteAngle (brand short code) | `RA` |
| `TRAFFIC` | Campaign objective (traffic to website) | `TRAFFIC` |
| `GET` | Destination / landing page (`/get`) | `GET` |
| `IN` | Country (India) | `IN` |
| `[GEO]` | City/region | `BLR`, `DEL`, `HYD`, or `PAN` (pan-India) |
| `[FUNNEL]` | Funnel stage | `TOF` (top of funnel), `MOF`, `BOF` |
| `[YYYYMM]` | Launch month | `202608` |

## Ad set

```
[AUDIENCE]_[AGE]_[GENDER]_[SIGNAL]
```

`[AUDIENCE]` is the persona/segment name from `targeting.md` (e.g. `CASUAL`, `INVISIBLE-MAN`,
`FLOODED-WOMAN`). `[SIGNAL]` is the creative angle or landing-page variant (e.g. `STORY`, `LPV` for
landing-page-view optimized). Matches the pattern already live, e.g. `MEN_25-40_CASUAL_STORY_IND-LPV`.

## Ad (creative)

```
[FORMAT]_[HOOK]_[VARIANT]_[DATE]
```

`[FORMAT]` — `IMG`, `VID`, `STORY`, `COLLECTION`. `[HOOK]` — a short slug for the emotional hook used
(see `creative-style.md`'s "ad-ready threads" for the vocabulary — e.g. `CAMERA-JUDGE`,
`FOURTEEN-SUITORS`, `DESOLATE-MAN`). `[VARIANT]` — `A`/`B`/`C` for a/b tests of the same hook.

## Why this matters beyond tidiness

`pocket-dating-coach`'s ad-set rollup is keyed on ad set (not campaign — two live campaigns have shared
an identical name with different ids before), and it joins spend to traffic by parsing this exact
structure out of both the network's own naming and the landing-page UTM. A recommendation that doesn't
follow this convention doesn't just look messy — it produces an ad set that `ad-audit` cannot reliably
attribute spend or performance to later.

## UTM scheme (append to every landing URL)

```
https://www.riteangle.dating/get?utm_source={snapchat|meta}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adSet.name}}&utm_content={{ad.name}}
```

`utm_term` carries the ad set name/id, `utm_content` carries the ad (creative) id — this is what
`ad-analytics.ts`'s `adSetKeyOf` parses on the traffic side of the join.
