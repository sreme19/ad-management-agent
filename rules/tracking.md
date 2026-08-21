# Tracking verification (UTM / attribution)

Source: incident found 2026-08-21 in `pocket-dating-coach`'s admin Users table — the "Ad" column was
blank for every single row. Investigation found **0 of 54** Snap-attributed installs over the prior
week ever carried an ad-level identifier, so no install could ever be joined back to the ad that
produced it. Read this before every `ad-setup-loop` handoff, and follow the checklist below before and
after every launch — this is not optional cleanup, it is the only thing that makes `ad-audit` possible
later.

## What actually happened (why "Snap auto-appends it" is not to be trusted)

A comment in `pocket-dating-coach`'s `traffic-quality.ts` asserted that Snapchat auto-injects `utm_id`
(the ad id) on every impression, verified once against specific creatives on 2026-08-10. That assumption
does not hold in general — of 54 Snap-attributed installs checked on 2026-08-21, **zero** carried a
`utm_id`, not even as an unresolved `{{macro}}` literal. The unresolved-macro case (which the parsing
code deliberately fails closed on) did not occur — the parameter was simply never present. Whatever ad
produced those installs had a destination URL with no tracking parameters attached at all, so
`pocket-dating-coach`'s `/get` landing page fell through to its own hardcoded default
(`utm_campaign=get_lp`, no ad set, no ad), and every one of those installs is permanently
unattributable — there is no click id, no ad id, nothing stored anywhere that a fix can retroactively
join back to a specific ad.

**Separately, this repo's own UTM scheme (below, and previously in `naming.md`) was itself out of sync
with what `pocket-dating-coach`'s join code actually reads.** `adSetKeyOf()` in `traffic-quality.ts`
only ever reads `utm_id` for Snap's ad-level id — it does not read `utm_content` for Snap. So even the
handful of installs that *did* carry a populated `utm_content` (a readable creative slug, from ad sets
that had at least partially set up their tracking template) still could not populate the Ad column. Two
independent gaps compounded: the ad's URL wasn't sending an id, and the doc telling people which
parameter to put it in was pointing at the wrong one for Snap.

## The URL every ad must carry — non-negotiable, checked before launch

```
https://www.riteangle.dating/get?utm_source={snapchat|meta}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adSet.id}}&utm_id={{ad.id}}&utm_content={{ad.name}}
```

- **`utm_id={{ad.id}}` is mandatory on Snap, set explicitly on the ad's own Website URL field.** Do not
  rely on Snap to append it — that assumption already failed once, silently, for a full week of spend.
- `utm_term` carries the ad set id (Snap) — already correct in `naming.md`, unaffected by this incident.
- `utm_content` carries a human-readable ad name/slug for readability and manual cross-checking. It is
  *not* what `pocket-dating-coach` joins on for Snap — `utm_id` is, so its presence in the URL is the
  one that actually matters for the Ad column and any ad-level `ad-audit` breakdown.
- On Meta, the equivalent ad-level id is `utm_content` (Meta's own macro convention;
  `traffic-quality.ts` reads it that way for the `meta` network specifically — don't cross the two
  networks' conventions).

## Pre-launch check — before a single rupee of spend, every ad, no exceptions

1. Open the ad's actual Website URL field in Ads Manager (not the campaign-level default, the specific
   ad's own field) and confirm all five parameters above are present with real macros, not left blank
   or copied from a template that predates this checklist.
2. Click the ad's own preview/swipe-up link (or paste the URL into a browser) and confirm it lands on
   `/get?...` with every macro resolved to a real value — a UUID for `utm_term`/`utm_id` on Snap, not a
   literal `{{adSet.id}}` or `{{ad.id}}` string. An unresolved macro means the platform's targeting
   step wasn't completed correctly and the ad should not go live until it is.
3. This takes under a minute and would have caught the 2026-08-21 incident before a single install was
   lost to it. Treat it as a hard gate in step 8 of `ad-setup-loop`'s procedure, not an optional nicety.

## Post-launch check — within the first hour of any campaign going live

Query `pocket-dating-coach`'s `user_acquisition` table (via the `ads_agent_ro` read-only role, or ask
the user to run it) for rows on the relevant network created since launch, and confirm they carry a
real `utm_term`/`utm_id` — not the landing page's hardcoded default (`utm_campaign=get_lp` with nothing
else). If every row since launch is hitting the default, tracking is broken for that ad and spend is
accumulating unattributable installs right now — flag it immediately rather than waiting for the next
scheduled `ad-audit` pass, since the whole week's spend in the 2026-08-21 incident was lost exactly this
way.

## Closing the loop

`log-setup` in the ledger should not be considered complete until the post-launch check above has run
at least once against real data. A recommendation whose IDs were logged but whose tracking was never
verified live is exactly the gap that produced this incident.
