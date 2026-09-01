# Session resume — 2026-09-01 (Gen1 women's email drip — Brevo build)

Pick-up point for a new session (account/login switch). Read this first, then
`uv run ad-agent open`.

---

## 1. What this session did

Built the full Gen1 women's email drip in Brevo end to end: account, domain, sender, API
key, all 4 email templates (Hinglish copy + custom Grok/Flow GIF heroes), and — in
progress — the send automation itself.

Full narrative + all copy/build rules already committed to the repo:
[`research/outreach/email-drip-sequence.md`](research/outreach/email-drip-sequence.md) and
[`research/outreach/whatsapp-email-outreach-handoff.md`](research/outreach/whatsapp-email-outreach-handoff.md).
Memory notes: `project_email_marketing_brevo.md`, `project_email_drip_gen1.md` (both up to
date as of this session).

## 2. Exact state in Brevo (verify by logging in, org "Riteangle")

- **List** `Gen1 - Women (drip)` — id **#3**. Contains 1 contact (test: sreekanth.rnsm@gmail.com).
  Real leads NOT imported yet.
- **Templates** (Templates → Email), all **Active**:
  - `#1` Drip W1 - Invite — swagger/laugh GIF, "Move on toh karna hai, / par dhang se." caption
  - `#2` Drip W2 - Flood — sunglasses GIF, "14 log DM mein, ek bhi dhang ka nahi?" caption
  - `#3` Drip W3 - Proof — text-forward, "Verified, vibes nahi"
  - `#4` Drip W4 - Last Nudge — walking GIF, "Tumhari spot abhi bhi open hai, / par hamesha ke liye nahi."
  - All four were test-sent and visually verified in Gmail (inbox, not spam) during this session.
- **Automation** `Automation #1` (`https://app.brevo.com/automation/edit/1`) — **Inactive**,
  NOT yet activated. Built so far, top to bottom:
  1. Trigger: **Contact added to list** → `Gen1 - Women (drip) - #3`
  2. **Send an email** → message from template #1 (W1 invite) — wired, confirmed
  3. **Wait 3 days**
  4. **Send an email** → message from template #2 (W2 flood) — wired, confirmed
  5. **Wait 3 days**
  6. **Send an email** → message from template #3 (W3 proof) — wired, confirmed
  7. **Wait 4 days**
  8. → **Exit** (dead end right now — nothing after the wait)

## 3. Exact next step (pick up here)

**W4 (Last Nudge) is not yet wired into the automation.** The last thing done was saving
the "Wait 4 days" step (step ID #9) after W3. Next action: click **"Add Step here"**
below that wait, search "Send an email" (use `find`/`read_page` refs, NOT raw coordinates
— coordinate-clicking repeatedly hit the wrong sidebar item this session, see §5), place
it, then **"Add message" → "Your templates" → "Use template"** on **Drip W4 - Last Nudge**,
accept the design ("Use this design in automation"), Save the step. That completes the
4-email chain into Exit.

After that, still to do before this can go live:
- **Reply-To** on each Send-an-email step (or the sender default) → confirm it resolves to
  `hello@riteangle.dating`, not `team@go.riteangle.dating` (which can't receive).
- **Deliverability warm-up plan** (§ in email-drip-sequence.md) — do NOT bulk-import the
  real lead list and flip the trigger list to the full audience on day one. Ramp per the
  documented schedule.
- **List import** — pull + reconcile + gender-segment the real leads (the big remaining
  piece, separate from this automation build — see the outreach handoff file).
- Only then: **Activate automation** (currently Inactive) and swap list #3's membership
  from the test contact to the real segmented list.

## 4. Also true, unrelated to this thread (don't lose track)

A **different/parallel session** did research on building a **new landing page** for this
same drip (breakup-themed, no iOS lead form up top, Android CTA prominent, using
`girlboss-moodboard-w1830/asset-a.mp4` frames). That work is **research-only, paused, no
code written** — captured in memory `project_email_drip_new_landing_page.md`. Read that
file before touching `pocket-dating-coach/src/routes/get/`. Not part of this session's
scope; don't assume it's done or start it fresh — the notes say exactly what's left.

## 5. Gotchas hit this session (avoid repeating)

- Brevo's automation-builder sidebar list re-renders/reorders after searches; clicking a
  fixed pixel coordinate for "Send an email" or "Time delay" repeatedly landed on the wrong
  item (e.g. "Assign a user to a contact", a stray "Unsubscribed from emails" trigger got
  placed and had to be deleted). **Use `find` to get a fresh `ref_` for the exact list item
  every time**, don't reuse remembered coordinates across searches.
- The "Create new message" dialog's template cards shift position/zoom unpredictably after
  clicking "Your templates" — same fix: `read_page`/`find` for the specific "Use template"
  button ref, don't coordinate-click.
- Test-sending an email in Brevo (editor or automation) requires the recipient to already
  exist as a **contact** (`ERR_TEST_MAIL_NOT_SENT` / `email_without_list` otherwise) —
  created via `curl -X POST https://api.brevo.com/v3/contacts` using the key in
  `pocket-dating-coach/.env.local`.
- Saving template metadata (subject/sender) is lost if you enter the content editor without
  saving the outer form first — always Save on the overview screen before clicking Edit.

## 6. Housekeeping

Nothing from this session has been committed/pushed (git commands were blocked in this
session's sandbox). If picking this up in a fresh session, check `git status` — the
drip-sequence doc, GIF assets in `research/outreach/email-assets/`, and this file are all
present on disk but likely uncommitted.
