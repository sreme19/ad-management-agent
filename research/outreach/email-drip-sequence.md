# Riteangle Email Drip — Sequence + Copy (v2 draft)

Created 2026-08-31. First-draft structure and copy for the **Gen 1** email drip that runs
on Brevo (`go.riteangle.dating`). Companion to
[`whatsapp-email-outreach-handoff.md`](whatsapp-email-outreach-handoff.md) — read that for
the channel/foundation state.

**Status:** DRAFT copy. Two placeholders are the operator's call: the consent/opt-out line
(Email 1) and the CTA destination (Play Store install vs. an on-page signup). Final copy
passes `rules/compliance.md` before anything ships.

---

## Register (locked)

Body is **genuine code-switched Hinglish** — Hindi and English mixed through the actual
sentences, romanized (not Devanagari), the way urban Gen-Z Indians text. NOT English with a
Hindi sprinkle; NOT pure Hindi. Product nouns stay English where they'd naturally be said
that way (invite, match, shortlist, early access, AI, swipes); Hindi is the connective
tissue. Voice per `rules/creative-style.md`: confident, precise, empathetic without
softness — no hype, no salesy urgency, no money/ranking/high-earning language.

## The arc

| # | Day | Purpose | Hook(s) | Primary KPI it tests |
|---|-----|---------|---------|----------------------|
| 1 | 0 | The invite (what they consented to) | — (neutral) | Click → install |
| 2 | +3 | The frustration, in their register | W: `FOURTEEN-SUITORS`/`MOVE-ON-PROPER` · M: `DESOLATE-MAN` | Which hook lands (CTOR) |
| 3 | +6 | Proof / how it works | `VERIFIED-DELETED`, `MONOTONIC-PROGRESS` + first-party stats | CTR on the mechanic |
| 4 | +10 | Honest last nudge, then exit | balance/early-access (real reason, no fake urgency) | Final conversion + complaint watch |

- **Two tracks** (women / men) share the skeleton; Emails 2–3 fork on the hook.
- **`unclear`-gender bucket:** Email 1 only, then holds — never a mis-gendered hook.
- **Exit:** signs up → drip stops (needs conversion event wired). Bounce/complaint/unsub → immediate suppression.

## Automation flow (Brevo)

Entry (contact added + tagged `gender`,`source`) → Email 1 → wait 3d → converted? exit :
Email 2 → wait 3d → converted? exit : Email 3 → wait 4d → converted? exit : Email 4 → exit.
Optional (sparingly, Email 1 only): resend to non-openers after 48h with Subject B.

## Deliverability warm-up (mandatory — brand-new subdomain)

Do not blast the whole list on Email 1. Ramp while complaint rate < 0.1%:
Day 1 ~50 → Day 2 ~100 → Day 3 ~200 → then double daily.

## KPI targets (starting hypotheses)

| Metric | Target | Note |
|--------|--------|------|
| Delivery | ≥ 97% | bounce < 2% |
| Open (Email 1) | 35–50% | ⚠️ Apple MPP inflates opens — don't optimize on this alone |
| CTR (Email 1) | 8–12% | high, it's the consented invite |
| CTOR | 15–25% | the real engagement read |
| Lead → signup | 5–10% over the sequence | the metric that matters; needs conversion event |
| Unsubscribe | < 0.5% / email | |
| Spam complaint | < 0.1% | HARD guardrail — pause the drip if breached |

Reply-To on every campaign → `hello@riteangle.dating` (the `team@go.` sender can't receive).

---

# Copy

Merge field shown as `{{first_name}}`. Every email carries the unsubscribe footer (required).

## Email 1 — The Invite · Day 0 · both tracks

- **Subject A:** `{{first_name}}, tumhara riteangle invite ready hai`
- **Subject B:** `{{first_name}}, jiska wait tha — woh invite aa gaya 💌`
- **Preview:** `No swipes. Sirf matches jo actually matter karte hain.`

> Hi {{first_name}},
>
> Tumne bola tha — jab invite ready ho toh batana. Toh bata rahe hain: ready hai. 🎉
>
> riteangle koi aur swipe-saara-din wali app nahi hai. **Yahan swipes hote hi nahi.** Saara mushkil kaam AI karta hai — aise log dhoondhna jo sach mein tumhare liye sahi hain. Matlab tum milte ho unse jinse tum *actually* milna chahte ho — mahino mein nahi, minuton mein.
>
> Tumhari early-access spot open hai.
>
> **[ Claim your invite → ]**
>
> — Team riteangle
>
> *Yeh email isliye mili kyunki tumne riteangle.dating pe early access ke liye sign up kiya tha. [consent / opt-out line — Sree to finalize]. Interested nahi? [Unsubscribe].*

## Email 2 — The Frustration · Day +3 · forks by track

### Women — `FOURTEEN-SUITORS` / `MOVE-ON-PROPER`
- **Subject A:** `14 log DM mein, ek bhi dhang ka nahi?`
- **Subject B:** `Move on toh karna hai — par dhang se`
- **Preview:** `Ek shortlist jo sach mein kuch matlab rakhti hai.`

> {{first_name}},
>
> Sach baat yeh hai — problem kabhi *kam* logon ki thi hi nahi. Problem hai flood: chaudah DMs, koi order nahi, aur tum bas… tab band kar deti ho.
>
> riteangle isko ulta karta hai. Sort karne ke liye ek dher nahi — tumhe milti hai ek **shortlist**, jahan log pehle se fit ke liye vetted hain. Chunna AI karta hai. Tumhe bas aana hai.
>
> Move on toh karna hai. Bas, dhang se.
>
> **[ See your shortlist → ]**

### Men — `DESOLATE-MAN` + 12-min stat
- **Subject A:** `Mahino ka silence, phir ek option jo corner jaisa lage`
- **Subject B:** `{{first_name}}, ab sach mein choice hai`
- **Preview:** `First match tak median time: 12 minute.`

> {{first_name}},
>
> Pattern tumhe pata hai. Hafton tak kuch nahi, phir achanak ek match jo choice kam aur majboori zyada lagta hai.
>
> riteangle alag chalta hai. **Men ke liye signup se first match tak median time — 12 minute.** Mahine nahi. Aur yeh asli choice hai — woh ek option nahi jo bas reply karne ko mil gaya.
>
> **[ Get matched → ]**

## Email 3 — Proof / How It Works · Day +6 · shared spine, forked angle

- **Subject A:** `Verified, vibes nahi`
- **Subject B:** `riteangle actually kaam kaise karta hai (30 sec)`
- **Preview:** `Emotional heavy lifting AI sambhaalta hai. Control tumhare paas.`

> {{first_name}},
>
> Jaayaz sawaal — *yeh alag kyun hai?* Teen asli wajah:
>
> - **Kaam AI karta hai.** riteangle pe aadhe se zyada messages ek AI companion ne kisi ki taraf se bheje — matlab emotional heavy lifting sambhal jaata hai, aur control phir bhi tumhare paas rehta hai, bina mental load ke.
> - **Verify, phir delete.** Proof ek baar check hota hai aur gayab — [women: *usse bolne ke points nahi milte, prove karne ke milte hain, aur woh document tum kabhi dekhti hi nahi* / men: *tum fit prove karke upar aate ho — chupke se un logon se peeche nahi padte jinhe dekh bhi nahi sakte*].
> - **Sach mein balanced.** Zyaadatar Indian dating apps 70–90% men hote hain. riteangle almost even hai. Ek asli community, koi queue nahi.
>
> **[ Get your invite → ]**

## Email 4 — Honest Last Nudge · Day +10 · mostly shared

- **Subject A:** `Aakhri baar, {{first_name}} — promise`
- **Subject B:** `Tumhari spot rok ke rakhi thi — kyun, batate hain`
- **Preview:** `Koi pressure nahi. Bas ek khula darwaza.`

> {{first_name}},
>
> Yeh aakhri baar hai jab hum nudge karenge — pakka.
>
> Hum early access ko jaan-boojh kar balanced rakhte hain (isiliye community 90% ek gender wali nahi hai). Tumhari spot abhi bhi open hai, par inhe hum hamesha ke liye rok ke nahi rakhte.
>
> Agar riteangle tumhare liye nahi hai — no hard feelings, [unsubscribe] kar do aur hum ruk jaayenge. Par agar iska koi bhi hissa waisa laga jiski tumhe talaash thi:
>
> **[ Claim your spot → ]**
>
> — Team riteangle

---

## Visuals (women's track) — from the Grok/Flow "Tumse Na Ho Paayega" girlboss arc

**Email-video reality:** you cannot embed a *playing* video in email (Gmail/Outlook strip
`<video>`). So we use **hero stills** or an **animated GIF** (autoplays in most clients), and
if we ever want the full clip, an image with a ▶ overlay that *links* to the hosted video.

Source: `creatives/girlboss-moodboard-w1830/` (Grok stills + Flow scenes; `_source/` is
gitignored). Email-ready exports (Grok watermark cropped per pipeline rule, resized,
optimized) live in `research/outreach/email-assets/`:

**Default = GIF (motion), mixable with stills later** (Sree, 2026-08-31). **Openers must be
youthful / colorful / attractive / vibrant** — never a slow "origin" beat. Each asset has a
GIF + a still export, so any email can swap format.

| Email | Beat | GIF (default) | Still (mix option) | Why |
|-------|------|---------------|--------------------|-----|
| 1 (invite) | **Swagger — laughing, coral/pink wall** | `swagger-opener-400.gif` (0.9MB) | `swagger-opener-480.jpg` (19KB) | Youthful, on-palette, joyful — pops in the inbox |
| 2 (frustration) | Street walk / high-standards | `scene4-motion-280.gif` (0.9MB) | `scene4-hero-480.jpg` (55KB) | Confident "bigger life" — energetic, not dull |
| 4 (last nudge) | Rooftop / "on her own terms" | `scene5-motion-280.gif` (0.7MB) | `scene5-hero-480.jpg` (40KB) | Confident payoff |

REJECTED as openers: the girlboss origin frames (scene1 bedroom-mirror etc.) — too dull;
the fourteen-suitors chai still — too flat. GIF specs: ~280–400px wide, 8–10fps, 2s,
watermark cropped, palette-optimized under ~1MB. Email 3 (proof) stays image-light or uses a
product-UI still. Overtly skin-heavy frames (beach/pool swimsuit) held back during warm-up
(spam-filter risk on a fresh subdomain).

Notes:
- **Display width** ~320–360px in the email (these are 9:16 portrait; full width would
  dominate on desktop). Mobile-first — most opens are on phones.
- **Swimsuit scenes (S6 beach / S7 pool) deliberately excluded** from email heroes — Snap
  kept them mild; email hero + spam-filter risk isn't worth it. Clothed scenes only.
- **Hosting:** images must be *hosted*, not attached — upload to Brevo's image gallery (or
  serve from `go.riteangle.dating`) when building the campaign. Attachments hurt
  deliverability and won't render inline.
- **Men's-track visuals:** TBD — this arc is women-only. Men's emails stay text-forward for
  now, or use a product-UI still (shortlist / progress bar) if one gets rendered.

## Copy + build rules learned from Email 1 test round (2026-09-01) — apply to ALL drip emails

1. **No em-dashes anywhere** (Sree: "projects AI"). Use commas and full stops.
2. **Subjects must not depend on merge fields** — a missing FIRSTNAME renders ", tumhara…".
   Personalization lives in the body, structured so blank degrades cleanly ("Hey {{FIRSTNAME}} 👋",
   no comma after the merge).
3. **Hero GIFs must carry embedded messaging** — a pretty face with no text "makes no sense"
   (Sree). Typeset captions in Gabarito (ink #1B1020 / pink #FF3B6B on cream #FFF3F0 band),
   same pipeline as ad creatives; never AI-generated glyphs. Email 1 uses the MOVE-ON-PROPER
   line ("Move on toh karna hai, / par dhang se.") with body bridge "Breakup ke baad ka glow?
   Yahi toh hai. ✨" — breakup hook is the chosen opener for women (Sree).
4. **GIF's FIRST FRAME must be the money frame** (Outlook shows only frame 1).
5. **Unsubscribe = Brevo's "Unsubscribe link (global)" link type on a word**, never a typed
   `{{ unsubscribe }}` (renders as a giant raw tracking URL).
6. **Make the hero image itself link to the CTA URL** (mobile users tap the image).
7. **Test-send requires the recipient to exist as a contact** (Brevo error `email_without_list`),
   or FIRSTNAME renders blank. Add the tester to a list first (done via API: contact
   sreekanth.rnsm@gmail.com in list #3).
8. **Brevo editor gotcha:** subject/sender edits on the template overview are LOST if you enter
   the content editor without saving first; sender field can clear after Save & quit — re-check
   both before every activate.
9. **Consent line:** dropped entirely (Sree's call, 2026-09-01) — footer is just the
   "yeh email isliye mili kyunki tumne early access ke liye sign up kiya tha" line + linked
   Unsubscribe. No [TBD] placeholders in anything that can be test-sent.
10. Gmail may show a "message is in Hindi / Translate" banner on Hinglish — cosmetic, accepted.

**Built so far in Brevo:** list `Gen1 - Women (drip)` (#3) · template #1 `Drip W1 - Invite
(Gen1 Women)` (ACTIVE: swagger breakup-caption GIF hero linked to CTA, Hinglish body with
bridge line, pink CTA button with UTMs `gen1-drip-w1`, compliant footer). Test-sent to Sree
and iterated 2026-09-01. Emails 2-4 not built yet.

## Open items before ship

1. **Consent/opt-out line** in Email 1 — operator writes (DPDP call).
2. **CTA destination** — Play Store install vs. on-page signup; determines conversion-event wiring.
3. **Compliance pass** (`rules/compliance.md`) on all bodies.
4. First-party stats used (12-min median, 54% AI-sent, ~2:1 balance) are from
   `rules/creative-style.md` — re-verify they're still current before send.
