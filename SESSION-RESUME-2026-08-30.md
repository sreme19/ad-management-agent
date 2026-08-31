# Session resume — 2026-08-30 (Snap lead ingestion — FIXED via Google Sheets; loss was ~5 leads)

Pick-up point for a new session (account switch). Read this first, then
`uv run ad-agent open`.

> **UPDATE 2026-08-30 (later): resolved, and the loss was far smaller than this file first said.**
> The API webhook genuinely never delivers, but `marketing_leads` was already bulk-imported on
> 2026-08-29 (380 rows: 259 snap + 121 meta), so the real gap was only ~5 leads (now imported; DB at
> 385). The MOVEON lead form is now connected to a **Google Sheets direct integration** (the delivery
> path of record — see `rules/lead-delivery.md`), and the fix is encoded for future ads
> (`ad-setup-loop` step 8b, memory `project_snap_lead_delivery`). The "confirmed twice, nothing lands"
> narrative below was an artifact of `daily-ad-leads.ts`'s 1-day filter — read the CORRECTION section
> in `research/questions/q-2026-08-30-why-has-no-snap-lead.md`. Still to do: ongoing sheet→DB sync,
> connect the other forms.

---

## 1. The headline state — where to resume

**Real Snap lead-form submissions are not reaching Supabase at all. Confirmed twice,
5 minutes apart, from production logs. Root cause is still open — it looks like a
Snap-side delivery failure, not a bug in our receiver.**

Full write-up, evidence, and next actions are in
[`research/questions/q-2026-08-30-why-has-no-snap-lead.md`](research/questions/q-2026-08-30-why-has-no-snap-lead.md)
— read the **"New evidence (2026-08-30, later session)"** section at the bottom, it has
the detail. Summary below.

### What triggered this session
Sree saw a new lead notification in Snapchat for `VID_MOVE-ON-PROPER_A_20260829`
(10 leads, ₹44.75/lead per Ads Manager) and asked whether it was landing in Supabase.
It was not — and neither has anything else in the trailing 24h.

### What's confirmed
- **Registration is fine.** All 7 Snap lead forms (`ad-agent snap-leads forms`),
  including this ad's form, point correctly at
  `https://www.riteangle.dating/api/marketing/snap-lead`.
- **The receiver is up and logging** (`a7ed73c9`, live since 2026-08-30 12:08 IST,
  confirmed via `vercel logs`).
- **In the trailing 24h, exactly 5 requests hit the endpoint: 3 connectivity `GET`s,
  and 2 `POST`s that are both Snap's own synthetic sample lead (identical `lead_id`
  `13cbb197-9274-401d-aa87-0482bad1a307`) — not real submissions.** No signature
  errors, no parse errors, no stored/duplicate rows in that window — the receiver has
  never once processed a real payload.
- Re-ran `pocket-dating-coach`'s `daily-ad-leads.ts 1` twice, 5 min apart: identical
  result both times. Newest row in `marketing_leads` is still **29 Aug, 8:41 PM IST**
  (Divya Jedkha). Nothing from 30 Aug at all, despite Snap Ads Manager showing 10
  delivered leads on the live ad.

### What this means
Not our bug (signature/parsing/storage/dedupe have each been ruled out at different
points in this repo's history, and none has ever actually been exercised by a real
delivery). **Snap can reach us — the test payload proves that — but isn't forwarding
real form fills.**

### The exact next 3 steps (none done yet)
1. **Protect against loss now:** pull today's/this week's leads by hand — Ads Manager
   → Download → Account leads. 90-day clock, nothing is arriving automatically.
2. **Check Snap Ads Manager's own UI** for the lead form / integration — look for a
   delivery-health or error state the API (`GET /lead_gen/integrations/{id}`) doesn't
   surface. This is the one diagnostic not yet run.
3. **If the UI shows nothing wrong, open a Snap support case.** There is no further
   diagnostic to run against a channel that isn't calling us — this stopped being a
   code problem once the logs showed zero real deliveries.

---

## 2. Prior history, for context (already in git, don't re-derive)

- `68de0bd8` → `da82d33a` → `a27ddac8`: built the webhook receiver (signature over
  `{timestamp}.{body}`, header named `signature`, synthetic-test-payload filter).
- `cd2ce71`: Snap Ads Manager said 9 leads, `marketing_leads` had 7 — first diagnosis
  blamed the dedupe (unique indexes on phone/email).
- `6cfcd18`: **corrected** — the dedupe was not the cause. The two missing leads were
  never stored at all, and the 7 present rows were a manual bulk-import, not
  webhook-delivered. `marketing_lead_submissions` (a PII-free delivery-outcome table)
  was proposed as the fix for counting, but doesn't address non-delivery itself.
- `a7ed73c9`: added the unconditional inbound-POST log line used to produce this
  session's evidence.
- `research/questions/q-2026-08-30-why-has-no-snap-lead.md`: the open question this
  session's findings were appended to.

## 3. Unrelated housekeeping in the working tree

`git status` also shows unstaged deletions/adds under
`creatives/buildyourself-carousel-w1830/` (files moved into per-asset subfolders) and
a new `campaigns/buildyourself-carousel-a-w1830-snap/` — **unrelated to the lead-ingestion
investigation**, left over from earlier work this session. Not touched or resolved here;
don't assume they're part of this bug.

## 4. Housekeeping notes for the next session
- Nothing in this session was committed to git — the question-file update and this
  resume file are on disk only. Commit them (and decide what to do with the unrelated
  creative-folder changes in §3) before or as part of the next pickup.
- `uv run ad-agent open` is still the right first command.
