# The rules

Every skill reads eight files under `rules/` live, every time &mdash; never from memory, and never
restated inside a skill file. If a rule gets refined mid-conversation, the skill edits the file in place
in the same turn; these are living documents, not a snapshot taken once and reused forever. This mirrors
`job-hunt-agent`'s own pattern (its `research.py` fit filter and `draft.py` style rules work the same
way): read the source, don't improvise, and keep the file current so the next session and the next
`ad-audit` run both see the same rules a person just refined.

```mermaid
flowchart TB
    Compliance["rules/compliance.md\nhard, App-Store-enforced —\nnever negotiable"]
    Targeting["rules/targeting.md\naudience personas, age/gender\nbands, geography"]
    Creative["rules/creative-style.md\ntone, taglines, first-party stats,\nvisual identity, competitors"]
    Naming["rules/naming.md\ncampaign/ad-set/ad naming,\nalready in production use"]
    Budget["rules/budget.md\noperating envelope,\nkill/double rule"]
    Tracking["rules/tracking.md\nUTM scheme, pre-/post-launch\nverification checklist"]
    Generation["rules/creative-generation.md\nPOV rule, Grok prompt skeleton,\nnegative list, QA gate"]
    Destinations["rules/destinations.yaml\nwhose POV each landing page\noccupies — enforced in code"]
    Networks["rules/networks.yaml\nper-network UTM conventions,\nand what may be created — read by the code"]

    Setup["ad-setup-loop"] --> Compliance & Targeting & Creative & Generation & Destinations & Networks & Naming & Budget & Tracking
    Audit["ad-audit"] --> Budget
    Ideation["ad-ideation"] --> Compliance & Targeting & Creative & Budget
    Intake["ad-intake"] --> Compliance & Creative & Generation
```

## `rules/compliance.md` &mdash; the one file every finished draft is checked against

These come from the product's own marketing knowledge base, not from this repo's design process, and
they're enforced, not aspirational: the iOS build was actually **rejected by Apple under App Store
Guideline 1.1.4 ("compensated dating") on 2026-08-03**, and the codebase now has an automated
banned-vocabulary gate that fails the build if the removed wording reappears anywhere.

The rule worth understanding in full, because it's easy to flatten by accident: **money is never an
attraction signal in ad copy.** No lane may imply money, luxury, being kept, or a giver/receiver pair.
The matching *backend* is allowed to model "provider energy" as a real preference some women in the
casual segment genuinely have &mdash; that's a real signal worth matching on. **The ad copy itself may
never say it, imply it, or visually signal it.** Model it in the algorithm; never say it in the creative.
Everything else follows the same shape: no purchase language (there are no in-app purchases), referral
cash is never a rupee figure in copy, never call the membership "high-earning" (the approved phrasing is
"identity-verified and established professionals"), a man's real unenhanced photo never appears in an
ad, AI imagery is labelled, and everyone shown is 18+ without exception.

A finished draft that trips any of this is a decision for the app owner to make &mdash; never a copy
edit a skill quietly fixes and moves past.

## `rules/targeting.md` &mdash; who an ad set is actually for

Four named personas, picked one per ad set and named in the ad-set slug: **The Invisible Man**
(28&ndash;38, months of near-zero matches), **The Flooded Woman** (25&ndash;35, drowning in
low-quality matches), **The Second-Chapter Person** (post-divorce/late-30s+, wants seriousness without
family-mediated matchmaking), and **The Casual but Selective Woman** (18&ndash;28, the persona where the
provider-energy distinction above matters most). The core priority band is Women 18&ndash;30, Men
25&ndash;38, with two different creative treatments inside the women's band &mdash; wild-experience
energy for 18&ndash;22, security/safety/loyalty framing for 25&ndash;30. Geography prioritizes Bangalore,
then Delhi/Hyderabad, matching where the platform's own membership already concentrates. Ad sets are
always split by gender &mdash; never mixed.

## `rules/creative-style.md` &mdash; how it sounds and looks

Confident, precise, direct; never hype, jargon, or urgency. The primary tagline is **"Meet who you
actually want &mdash; in minutes, not months,"** with several site-native alternatives to rotate rather
than reuse across every ad in a set. Quotable numbers are first-party and measured &mdash; e.g. a median
12-minute time-to-first-match for men, or 54% of platform messages sent by an AI companion on someone's
behalf &mdash; quoted as rates and medians, never totals, since the platform is early and a total reads
as small in a way a rate doesn't. The visual identity is deliberately light (brand pink/coral on cream)
in a category where every rival ships a dark UI, using **Gabarito** throughout and the lowercase
wordmark **"riteangle."** This file also holds the competitive-landscape notes `ad-ideation` and
`ad-intake` both research against.

## `rules/creative-generation.md` &mdash; how an asset actually gets made

Added 2026-08-24, after the first live lead campaigns returned **98% male lead-form submissions and
100% male `/get` store taps**. The diagnosis was that this is decided at generation time, not at
targeting time, so the fix had to be a rule about how creative is produced.

The load-bearing one is the **POV rule**: *the person an ad is targeting is the person whose point of
view the frame occupies &mdash; never the thing being looked at.* Three of the first four live ads put a
woman in the frame as its object, and an ad that shows a desirable woman recruits men whatever the ad
set's gender setting says. So women's creative gets no woman as the object of the frame at all; it
occupies her point of view instead. The same rule applies symmetrically to men's creative &mdash; a
woman shown as the reward is the same giver/receiver framing `compliance.md` forbids, just pointed the
other way.

The rest is production discipline. **Generate the plate, never the typography** &mdash; image models
garble text, the lowercase `riteangle` wordmark in Gabarito is a brand mark that can't be left to a
sampler, and a plate with no text baked in can be re-cut for a new hook without regenerating the image.
The **standing negative list** names signifiers rather than concepts (no gowns, ballrooms, marble,
chandeliers, luxury cars, nobody kneeling or serving), because a generator can act on those and can't
act on "no provider framing." And Grok is explicitly **the wrong tool for some assets**: where the
creative *is* the product's interface, it's briefed from the existing renders in Figma instead.

Every generated asset then passes a **QA gate** &mdash; checked as an image, not as copy &mdash; with a
verdict of `pass`, `regenerate` (naming the prompt clause to change), or `escalate` (a compliance hit,
which is the app owner's decision). Per `compliance.md`, that check is a separate pass from the one that
wrote the prompt.

## `rules/destinations.yaml` &mdash; a rule file the code enforces itself

Every other file under `rules/` is read by a skill and applied with judgment. This one backs a **hard
gate in the CLI**: `ad-agent propose` refuses to write a record whose ad-set audience doesn't match the
framing of the page it sends traffic to.

It exists because of the second half of the same finding. Riteangle's `/get` landing page is written in
the second person to a man throughout &mdash; *"She asked how you spend your weekends," "then she sees
you," "never a ranking against men he cannot see."* She is third person on every line. A woman who taps
a women's ad lands on a page explaining how a man gets in front of her, which is a complete explanation
for 100% of store taps being male. There is no public women's page to send her to instead: the women's
invite flow is token-gated and can't receive paid traffic at all.

The registry records, per page, whose point of view its copy occupies, whether it can take paid traffic,
and the date someone actually read it to classify it. **There is deliberately no override flag**, and
`ad-agent amend` can't launder one either &mdash; a blocked proposal is unblocked by building the page
and registering it. Unregistered pages fail closed rather than being assumed safe, the same way
`tracking.md`'s parsing does.

## `rules/naming.md` &mdash; the convention every recommendation must match exactly

Already in production use, confirmed against live rows in `pocket-dating-coach`'s own database (e.g.
`RA_TRAFFIC_GET_IN_BLR_TOF_202608`). Campaign names follow
`RA_TRAFFIC_GET_IN_[GEO]_[FUNNEL]_[YYYYMM]`; ad sets follow `[AUDIENCE]_[AGE]_[GENDER]_[SIGNAL]`; ads
follow `[FORMAT]_[HOOK]_[VARIANT]_[DATE]`. This isn't cosmetic &mdash; `pocket-dating-coach`'s own
analytics joins spend to traffic by parsing this exact structure out of the network's own naming and the
landing-page UTM parameters. A name that doesn't parse produces an ad set `ad-audit` can never reliably
attribute performance to later.

## `rules/budget.md` &mdash; the envelope every proposal is checked against

A roughly ₹50,000/month total operating budget, split 40&ndash;50% testing, 40&ndash;50% exploiting
proven winners, and 10% retargeting once there's signal to retarget against. A minimum viable daily
spend of ₹800&ndash;1,200 per active ad set &mdash; below that, the platform's own delivery algorithm
rarely exits its learning phase. The **kill/double rule**: pause a losing ad set after 3&ndash;5 days or
50&ndash;100 events, whichever comes first, and move its budget to whatever's winning. This file also
carries the `MIN_SAMPLE = 30` confidence floor `ad-audit` inherits from `pocket-dating-coach` itself.

## `rules/tracking.md` &mdash; the UTM scheme, and why it's now a hard gate

Added 2026-08-21, after an incident where **zero of 54** Snap-attributed installs over a full week
carried an ad-level id &mdash; every one of them landed in `pocket-dating-coach`'s admin dashboard with
a blank "Ad" column, permanently unattributable, because the ad's own destination URL never had
`utm_id` appended and the code comment's assumption that "Snapchat appends it automatically" turned out
not to hold. A separate, compounding bug: this repo's own naming convention had previously told people
to put the Snap ad id in `utm_content`, but `pocket-dating-coach`'s join code only ever reads `utm_id`
for Snap &mdash; so even a correctly-filled-in `utm_content` would never have shown up as an ad name.

The corrected URL every ad must carry:

```
https://www.riteangle.dating/get?utm_source={snapchat|meta}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_term={{adSet.id}}&utm_id={{ad.id}}&utm_content={{ad.name}}
```

`utm_id={{ad.id}}` is now set explicitly on every ad's own Website URL field &mdash; never assumed. Two
checks are non-negotiable parts of `ad-setup-loop`'s procedure, not optional follow-up:

- **Pre-launch** (before any spend): open the ad's actual Website URL field and confirm every macro is
  present and set at the ad level, then click the ad's own preview/swipe-up link and confirm every
  macro resolved to a real value &mdash; not blank, not a literal `{{adSet.id}}`/`{{ad.id}}` string.
- **Post-launch** (within the first hour of real traffic): query `pocket-dating-coach`'s
  `user_acquisition` table for the network just launched and confirm real rows are landing with
  `utm_term`/`utm_id` populated, not the landing page's hardcoded default. `log-setup` isn't considered
  closed until this has run once against live data.

## Read next

- [How the four modes work](How-the-four-modes-work) &mdash; where each of these files gets read in the
  loop
- [Safety-and-guardrails](Safety-and-guardrails) &mdash; the boundary rules that sit outside `rules/`,
  in `SPEC.md` itself
- [Agent registry](Agent-Registry) &mdash; which skill reads which file, traced through the actual
  procedure steps

## `rules/networks.yaml` &mdash; the other rule file the code reads directly

Added 2026-08-26, deliberately **before** a third network was added rather than after. Until then
`snap` and `meta` were a two-value list hardcoded in four places, and `utm_source: "snapchat"` was a
string typed into a Snap-only function.

A network is not a string. It is four things, and two of them already differ between the two networks
in ways that have caused real bugs:

| | why it is here |
|---|---|
| `utm_source` | Snap's key is `snap` and its `utm_source` is `snapchat`. That mismatch is why only 7 of 151 signups could be joined to an ad set carrying cost. Both spellings are known in this repo and nowhere else. |
| `ad_join_param` | The analytics reads `utm_id` as the ad id on Snap and `utm_content` on Meta. Crossing them silently breaks ad-level attribution. |
| `ad_set_join_param` | Which parameter carries the ad-set id. |
| `creation` | `none`, or `paused-only`. |

**The `creation` field can only ever refuse**, and that distinction is the whole reason it is allowed
to live in an editable text file. The code consults it *in addition to* its own checks, never instead
of them. Setting `meta: creation: paused-only` grants nothing — `snap-push` refuses a non-Snap record
before it ever reads the registry, there is no Meta client to call, and no Meta credential exists to
call it with. What actually holds the paused-only line is the absence of credentials and the
transport-layer refusal in `snap.py`. See [Why it's built this way](Safety-and-guardrails).

The file leads with the argument against using it. `rules/budget.md` puts minimum viable spend at
&#8377;800&ndash;1,200/day per ad set against a &#8377;50,000/month envelope &mdash; one or two properly
funded ad sets at a time. Adding a network does not add reach; it splits the same money below the
floor, which is the exact failure the current live women's record exists to correct. A new network
also has to be taught to `pocket-dating-coach`, or its spend cannot join to its traffic &mdash; and
that join is already broken for the two networks here.
