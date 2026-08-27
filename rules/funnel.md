# Funnel rules — the search space every idea is drawn from

Source: Sree's 2026-08-27 session direction, recorded verbatim as
`research/notes/note-2026-08-27-womens-funnel-matrix.md`. This file exists because that direction is
**normative and standing** — "keep this entire matrix in front of you" is an instruction about what a
skill is allowed to propose, not an observation about the world, and the research store explicitly
cannot bind anything.

## 1. The funnel is a matrix, not a path — read this before proposing anything

Riteangle's women's funnel has one combination running: **static image → landing page → Play Store**.
That is one cell of a three-axis space, and it is the running cell for historical reasons, not because
the other cells were tested and rejected.

| axis | running today | the rest of the axis |
|---|---|---|
| **ad format** | static image, text overlay | carousel, video |
| **capture point** | none — the page hands off to the Play Store | on-platform lead form, email capture on the landing page, phone capture |
| **follow-up channel** | none — the install is the terminal event | call centre (outbound voice), WhatsApp |

**The axes are mix-and-match.** A video ad into an email capture consumed by WhatsApp is a legitimate
proposal shape; so is a carousel into the existing Play Store handoff. An idea that only ever varies
the creative angle inside the running cell has searched one column of this table.

**Do not drop an option because its prerequisites are missing.** The operator's instruction is
explicit that the unbuilt pieces are sequencing problems he intends to solve, not refusals. A blocked
option is a `hold` with a stated `--blocked-on`, never an option that goes unmentioned.

**The stated goal is women's leads.** The app download is what the current funnel happens to aim at.
Do not treat installs as the objective when a proposal could produce a contactable lead instead.

## 2. Sequence by friction, least first — and the ladder is not the obvious one

`ad-agent propose` and `snap-push` can only build the running cell. **Every other cell on this table
costs a code change, a change in another repo, or a legal entity** — see
`lrn-2026-08-27-matrix-options-are-code-changes`, which read the literals out of `snap.py` directly.

| rung | option | what it actually costs |
|---|---|---|
| 0 | another static image | nothing — the only thing pushable today |
| 1 | carousel / video | this repo: `snap.py` hardcodes `IMAGE` media, `WEB_VIEW` creative, `REMOTE_WEBPAGE` ad |
| 2 | email capture on `/get/w` | `pocket-dating-coach` route change, plus storage and consent |
| 3 | on-platform lead form | new objective (`snap.py` hardcodes `TRAFFIC`), new ad type, a lead-form resource `snap.py` has no call for |
| 4 | phone capture | rung 2's cost, and the consumer does not exist — see §3 |
| 5 | WhatsApp | in neither `networks.yaml` nor `destinations.yaml`; would run on Meta, where `creation: none` and no credential exists |

**Re-verify rung 1 and 3 against `snap.py` before quoting them.** That row is a claim about code on a
60-day clock, and one commit invalidates it. The code is the authority, not this table.

`budget.md`'s ₹800–1,200/day floor funds one or two ad sets at a time, so the ladder is a real
constraint and not a preference — the matrix has more testable cells than the budget can read at once.

## 3. Two corrections that a proposal must not get wrong

**On-platform lead forms are not untried, and not burned.** They ran, and returned 98% male
submissions — but `creative-generation.md` §1 attributes that to creative POV plus a submit-optimised
objective, and leaves the format itself unjudged. Both causes have since changed: the POV rule now
exists, and `/get/w` exists as a women-framed destination. Treat lead forms as a **re-run candidate**.
Do not cite the 98/2 split as evidence against the format — and note that no sample size or date range
is recorded for it anywhere (`q-2026-08-27-the-98-2-split-has-no-n`).

**A phone field has no consumer today.** The call centre is blocked on a company that is not
registered. Phone capture is therefore not a reason to add a field to `/get/w`; **email is the field to
test first** on that page. Re-read this section when the registration status changes —
`lrn-2026-08-27-callcentre-blocked-on-registration` carries the review date.

## 4. What this file does not do

It does not authorise anything. A cell on this table still passes every other gate: `compliance.md`
first, `destinations.yaml`'s audience match (no override flag), `budget.md`'s floor, `networks.yaml`'s
`creation` field. Widening the search space is not widening what may ship.
