# WhatsApp + Email Outreach Campaign — Handoff

Status as of 2026-08-31. Written to be picked up cold in a fresh session (different
account/credits) — read this file top to bottom before doing anything else.

> **Latest progress is in the "## Progress log" section below — read it first.** The
> original plan (steps 1–7) is unchanged, but the email channel now has a live
> foundation (Brevo) that the plan text below predates.

## Progress log

### 2026-08-31 — Email channel foundation stood up (Brevo)

Tool chosen: **Brevo** (free tier), for three reasons that fit this campaign: free tier
bills on daily send volume (300/day) not contact count, so a large lead list doesn't
force a paid plan; a real visual drip/automation builder + KPI dashboard; and **native
WhatsApp campaigns in the same account**, so the later WhatsApp extension (steps 5/6
below) becomes turning on a channel we already know rather than integrating a second
vendor. Driven via Claude-in-Chrome; API preferred for the actual send/sync work.

Architecture decision (locked): **transactional stays on Resend** (`send.riteangle.dating`,
Amazon SES — unchanged, do not touch). **Marketing/drip runs on Brevo** from a *separate*
dedicated subdomain so marketing spam-complaint risk never bleeds into the transactional
domain's reputation.

What's live now:
- **Brevo account** created (org name "Riteangle", Free plan). Owner login is a
  Riteangle-controlled address (not analytics@demandlane.com).
- **Sending subdomain `go.riteangle.dating`** — authenticated **and branded**
  (DKIM + DMARC both pass). Set up via **NS delegation** (Brevo-managed DNS): two NS
  records at Porkbun (`go` → `ns1.sendinblue.com`, `go` → `ns2.sendinblue.com`). Because
  the whole `go.` zone is delegated to Brevo, the branded tracking-link subdomain
  (`email.go.riteangle.dating`) needed **no extra Porkbun records**. Porkbun is the
  registrar (DNS on Cloudflare backend); login is Sree's.
- **Sender** `Riteangle <team@go.riteangle.dating>` — auto-verified (no confirmation
  email needed since the domain is authenticated; the subdomain can't *receive* mail).
  The old default sender `chris@wardrobeofamonk.com` (non-compliant, Default DKIM / no
  DMARC) was **deleted** — all senders now pass the Google/Yahoo/Microsoft bulk rules.
- **API key** `riteangle-outreach-claude` generated (Active, expires 2027-08-31). Stored
  as `BREVO_API_KEY` in **`pocket-dating-coach/.env.local`** (gitignored). NOT in
  ad-management-agent (zero-API by design). Note: Brevo keys also die after 90 days of
  inactivity; IP restriction left OFF deliberately (Claude Code sessions run from
  varying IPs).

Carried-forward reminders for the build:
- **Reply-To** must be set to a monitored inbox on the *root* domain (e.g.
  `hello@riteangle.dating`, which already receives) on every campaign — `team@go.` sends
  but cannot receive. This is a per-campaign setting, done at send time.
- Consent/DPDP note from decision #2 still stands: first email should open with an
  explicit "you gave us your email when you signed up for early access" reminder + clear
  unsubscribe, and warm the new subdomain slowly (complaint rate is what kills a fresh
  sending subdomain).

Not yet done on the email side: no contacts imported, no list built, no drip/automation,
no templates, no copy, nothing sent. Next up: import the segmented lead list (with the
reconcile-against-Ads-Manager caveat below), then build the drip + KPI targets.

## The ask

Riteangle has collected leads (name, email, and/or phone) through Snap/Meta lead ads.
Goal: reach the female-identified subset of these leads via WhatsApp and email.

## Decisions already made (do not re-ask these)

1. **Gender segmentation method**: run a name-inference pass over the *whole* lead list
   (same heuristic `ad-leads-daily` uses — classify by first name as woman/man/unclear,
   flag ambiguous names rather than guessing). Not limited to the self-declared
   `audience` field, which is often null.
2. **Consent/legal gap**: the user (Sree) is handling this call personally. Do not gate
   further work on it, but also do not silently treat it as resolved — the current
   lead-capture consent copy ("Used once, to tell you when your invite is ready. Not
   shared, and 18+ only") does **not** cover marketing outreach by email/WhatsApp. No
   `consent_at`/`opted_in` column exists in the DB.
3. **WhatsApp BSP (Business Solution Provider) selection**: the user is picking and
   setting this up personally (Meta Business Manager verification, BSP account,
   message-template pre-approval). Don't research/recommend one unless asked again —
   wait for them to name it, then build the client against whatever they chose.

## What's true about the data today (verified 2026-08-30, read-only)

- Lead PII (`marketing_leads` table) lives in **pocket-dating-coach's** Supabase, never
  in ad-management-agent. `ads_agent_ro` (the DB role ad-management-agent uses) is
  **not** granted this table on purpose — it's a contact list, not analytics. Only
  `marketing_lead_submissions` (counts/status, no PII) is readable from here.
- Pull script already exists: from the **pocket-dating-coach** repo run
  `npx tsx --env-file=.env.local scripts/daily-ad-leads.ts [days]` (note: `.env.local`,
  there is no plain `.env` there).
- `contact_kind` distinguishes two very different things stored in the same
  `whatsapp_e164` column:
  - `whatsapp` — she typed the number into our own form herself.
  - `phone` — Snap prefilled it from her Snap account; **not confirmed to be a WhatsApp
    number, and not something she typed with WhatsApp contact in mind.** Messaging this
    group via WhatsApp is the exact DPDP risk flagged in the migration that created this
    column (`20260829144332`).
- No `gender` column exists. `audience` (`man`/`woman`) is self-declared and frequently
  null — not the same as the name-inference approach chosen above.
- DB lead counts have undercounted the network's real count before (silent webhook
  miss; dedup silently dropped 2 of 9 leads on 2026-08-29). **Always reconcile against
  Snap/Meta Ads Manager's own export before treating a pulled list as final** — see
  memory `feedback_reconcile_before_presenting`.
- Email: **Resend** is already wired and live (`hello@riteangle.dating`,
  `pocket-dating-coach/src/lib/server/email.ts`) but transactional-only — no marketing
  template, no unsubscribe mechanism yet.
- WhatsApp: **zero infrastructure exists** — no API client, no credential, no entry in
  `rules/networks.yaml` / `rules/destinations.yaml`. Open research question on file:
  `research/questions/q-2026-08-27-whatsapp-has-no-registry-path.md`.
- `email_drip_events` table exists (migration `20260815063050`) referencing
  `smartlead_campaign_id` — but **zero code anywhere integrates Smartlead**. Reserved
  shape only, not a working integration.

## The plan, step by step

1. **Pull the raw list** — from a pocket-dating-coach session, run this against
   `marketing_leads`:
   ```sql
   select id, first_name, last_name, email, whatsapp_e164, contact_kind,
          audience, source, page, status, submitted_at
   from marketing_leads
   where status <> 'invalid'
     and (email is not null or (whatsapp_e164 is not null and contact_kind = 'whatsapp'))
   order by submitted_at asc;
   ```
   This deliberately excludes `contact_kind='phone'` rows with no email (see DPDP note
   above). Including that riskier group is a decision the user must make explicitly.
2. **Reconcile** the row count against Snap/Meta Ads Manager's own lead count before
   trusting it as complete.
3. **Gender segmentation** — hand the `first_name`/`last_name` columns to a session and
   have it classify woman/man/unclear per the decision above. Output: female subset +
   a separate "unclear — review before sending" bucket, never silently guessed.
4. **Email build** (in pocket-dating-coach repo): extend the existing Resend sender with
   an actual marketing template and a real unsubscribe mechanism — neither exists today.
5. **WhatsApp build**: once the user has picked/set up a BSP and has a credential, write
   the client and register the channel in `rules/networks.yaml` /
   `rules/destinations.yaml` (currently absent entirely). Templates must be pre-approved
   by Meta before any send — free-form outbound marketing text is not allowed.
6. **Copy** — draft both message bodies (Hinglish/Gen-Z tone matching existing creative
   voice) with a placeholder for the consent/opt-out line, which the user is writing
   personally. Do not invent DPDP-compliant consent language unprompted — that's the
   user's call per decision #2 above.
7. **Small test batch → track back** — sends and `status`/`contacted_at` updates happen
   through pocket-dating-coach's own write path, not ad-management-agent (this repo
   stays read/plan-only by design — see `project_db_write_path`).

## Not started yet

**Done (2026-08-31):** the email-channel *foundation* — see "## Progress log" above
(Brevo account, `go.riteangle.dating` authenticated+branded, sender, API key).

**Still pending:** everything that uses that foundation — no list pulled, no contacts
imported, no gender segmentation run, no drip/templates/copy built, nothing sent. On the
WhatsApp side, no BSP chosen and no infrastructure exists. This file plus the Progress
log is the full state; nothing has silently progressed further than what's listed here.
