---
name: ad-leads-daily
description: The daily lead readout for Riteangle's Snap and Meta lead campaigns — who came in (name, email, timestamp, inferred gender), how many the network says came in, and what happened on the landing page and in the store afterwards. Use whenever the user asks what leads arrived, who came in today or yesterday, how many leads Snap/Meta produced, or wants the standing daily lead report.
---

# The daily lead readout (mode 10)

This is a fixed report, asked most days. It has one hard rule, and it exists because the
report was wrong the first time it was ever run.

## The rule: reconcile before you present

**Never present a lead count taken only from our own database.** On 2026-08-29 Snap Ads
Manager reported 9 leads and `marketing_leads` held 7. Nothing was broken and nothing
errored — the two missing submissions were people who had already submitted an earlier
Riteangle form, so the unique indexes on `whatsapp_e164` and `lower(email)` dropped them
and `recordAdLead` returned a contented `duplicate: true`. The list of seven names looked
exactly like a complete day. The app owner caught it, from a screenshot, twice.

That is the third instance of one failure shape, already written down twice in this repo
(`lrn-2026-08-28-channel2-rls-blocks-every-read`,
`lrn-2026-08-29-snap-lead-webhook-only`): **a channel that returns nothing and reads as an
honest zero.** Assume it is happening again until a number from outside our database says
otherwise.

So the report opens with the count and the delta, and the names come second.

## Running it

```bash
cd ../pocket-dating-coach && npx tsx --env-file=.env.local scripts/daily-ad-leads.ts 1
```

The script lives in `pocket-dating-coach`, not here, and that is deliberate: leads are
contact details, this repo records ad plans and outcomes. Run it there, read the result,
report it in the session. Nothing is written back here.

For the aggregate, campaign-level picture that *is* this repo's business:

```bash
ad-agent fetch-analytics --start <YYYY-MM-DD> --end <YYYY-MM-DD>
```

**Known blind spot:** as of 2026-08-30 that endpoint returns no lead metric at all — views,
taps, spend, leaderboard, LP funnel, and nothing about leads. It cannot be used to check a
lead count. Until that changes, the reconciliation number comes from Ads Manager by hand.

## What to report, in this order

1. **Reconciliation.** Delivered vs stored per network, and the delta against Ads Manager.
   If `marketing_lead_submissions` is missing from the output, say plainly that the report
   cannot verify its own completeness, and ask for the Ads Manager number rather than
   presenting the DB count as the day's total.
2. **The leads.** Network, name, email, timestamp.
3. **Gender — inferred, and labelled as inferred.** Derive it in-session from the first
   name; do not add a column to the script for it. Indian first names carry real ambiguity
   (`Kiran`, `Jyoti`, `Harpreet`, and any single-word handle like `Rosy`), the audience
   targeting is gendered, so a wrong guess quietly corrupts the read on who the creative is
   reaching. Mark every uncertain one `unclear` rather than guessing, and never present the
   split as a measured figure.
4. **Landing page and installs — aggregate only.** See the limit below.
5. **Anything that looks like a test.** Internal submissions reach the live forms
   (`chris.datingcoach@gmail.com` on 2026-08-29). Flag them; do not silently include them
   in a count you are handing over as demand.

## The attribution limit — do not present around it

`marketing_leads.visit_id` and `marketing_apply_gate.ra_lead` are **null on every row**.
Those are the only two keys that can join a named lead to a landing-page visit or an
install, so "how many of *these people* clicked through" is not answerable today:

- **Snap** never had a per-lead id. Its form end-page URL carries ad-squad-level UTMs and
  `ra_src=form` and nothing person-specific, because Snap documents no macro for it. This
  is structural — it will not be fixed by a change on our side.
- **Meta** has `ra_lead={{lead_id}}` on the form's button URL, and the macro is not
  resolving. `wiki-export/Command-Cheatsheet.md` says not to enable the campaign until an
  apply-gate row carries a real `ra_lead`; it was enabled anyway.

So report landing-page arrivals, store taps and installs as **campaign-level counts**, and
say so. Never write a sentence of the form "3 of the 9 leads visited the landing page" —
that number does not exist.

Landing-page arrivals also need de-botting: the raw count includes prefetchers and crawlers
arriving several-per-second. The script drops bursts, but the filter is a heuristic, so give
a range rather than a false-precision figure when the clusters are ambiguous.

## Related

- `rules/tracking.md` — what the UTMs and `ra_*` params are supposed to carry.
- `ad-audit` (mode 6) — the campaign-performance loop this report feeds.
- `supabase/migrations/20260830120000_create_marketing_lead_submissions.sql` in
  `pocket-dating-coach` — why the count and the person are two different tables.
