# Instagram competitor probe — Aug 26, 2026

Full sweep of all 24 competitors named in the matrix Sree shared, plus Riteangle's own baseline.
Method note (see `README.md`): Instagram exposes no demographic split on likes/comments for accounts
we don't own. Findings below use engagement rate against follower count, comment-thread tone, and each
account's structural audience skew (Bumble/Aisle skew female by product design) — never individual
commenter profiling.

**Tooling limitation, stated plainly** (unchanged from the first pass): the browser tool could not
persist image/video files to this folder — `save_to_disk` produced no file this session could locate,
and pulling the raw CDN URL via the DOM/API was actively blocked (signed auth tokens, correctly
guarded). Every post below was viewed and read directly, with its own link recorded per Sree's
follow-up ask — nothing here is a saved asset.

## Full roster — all 24 rows plus Riteangle

| # | Name | Handle | Followers | Posts | Notes |
|---|---|---|---|---|---|
| 1 | Tinder | [@tinder_india](https://www.instagram.com/tinder_india/) | 172K | 2,204 | See below — event/campaign-led, not feed-led |
| 2 | Bumble | [@bumble_india](https://www.instagram.com/bumble_india/) | 238K | 37 | Deep-dived in the first pass — see pattern section |
| 3 | Hinge | [@hinge](https://www.instagram.com/hinge/) | 288K | **9** | Almost no organic presence at all |
| 4 | Schmooze | — | — | — | No official account found under any search variant tried |
| 5 | Knot | [@knot.dating](https://www.instagram.com/knot.dating/) | 37.7K | 45 | "India's First AI Matchmaker for the top 1%" — direct positioning overlap with us |
| 6 | Betterhalf | [@betterhalfai](https://www.instagram.com/betterhalfai/) | 141K | 2,993 | See reputation-risk finding below |
| 7 | Shaadi.com | [@shaadi.com](https://www.instagram.com/shaadi.com/) | 312K | 2,693 | Strong hook ("Sirf scroll karoge ya kabhi phere bhi loge?"), weak engagement |
| 8 | BharatMatrimony | [@bharatmatrimony](https://www.instagram.com/bharatmatrimony/) | 89.6K | 4,892 | Highest post volume on the list; near-zero engagement per post |
| 9 | Riteangle | (own) | — | — | Baseline, not competitor |
| 10 | Badoo | [@badoo](https://www.instagram.com/badoo/) | 546K | 277 | Generic, no distinct hook |
| 11 | OkCupid | [@okcupid](https://www.instagram.com/okcupid/) | 94.4K | 785 | Values/identity-led (Pro Choice, Voter Badge, Climate) — not India-relevant |
| 12 | Tantan | — | — | — | No official account found |
| 13 | FRND | [@frndapp](https://www.instagram.com/frndapp/) | 583K | 1,245 | Voice/social-first, "for people who love talking" — largest India-relevant account by far |
| 14 | Aisle | [@aislenetwork](https://www.instagram.com/aislenetwork/) | 158K | 932 | Deep-dived in the first pass |
| 15 | Woo | — | — | — | No official Indian "Woo" account found; wooplus_dating (132K) is a different product (curvy dating, different market) |
| 16 | QuackQuack | [@quackquackapp](https://www.instagram.com/quackquackapp/) | 205K | 1,314 | Success-story highlight taxonomy; recent content is low-effort meme reposts |
| 17 | Coffee Meets Bagel | [@coffeemeetsbagel](https://www.instagram.com/coffeemeetsbagel/) | 467K | 3,454 | "Let's date for something real" — same anti-casual positioning as everyone else |
| 18 | Happn | [@happnindia](https://www.instagram.com/happnindia/) | 152K | 460 | Astrology-themed highlights ("Astro Crush," "ABC Dating") — notable India-cultural adaptation |
| 19 | match.com | — | — | — | No official/verified account found |
| 20 | Plenty of Fish | [@plentyoffish](https://www.instagram.com/plentyoffish/) | 145K | 1,041 | Recent grid is UGC/testimonial-to-camera style — same pattern as Bumble's winners |
| 21 | Seeking | — | — | — | No official account found — likely policy-blocked (see note below) |
| 22 | SDM Dating | — | — | — | No official account found |
| 23 | Ashley Madison | — | — | — | No official account found — both plausible handles belong to unrelated people (a drag performer, a fitness/beauty influencer who happens to share the name) |
| 24 | Sugar Book | — | — | — | No official account found |

**7 of the 24 have no discoverable official Instagram presence at all** (Schmooze, Tantan, Woo,
match.com, Seeking, SDM Dating, Sugar Book), plus Ashley Madison's brand account specifically.
Notably, **all four Western casual/affair-adjacent apps (Seeking, SDM, Ashley Madison, Sugar Book)**
are in this group — consistent with Meta's community standards discouraging infidelity-coded content
from running mainstream organic or paid social at all. That's a real category constraint, not just a
research gap, and it's further reason those four should stay out of our own creative reference set per
`rules/compliance.md`.

## Cross-account pattern (now confirmed across ~17 accounts, not just 3)

**Brand-voice organic content is dead across nearly the entire category.** Sampled recent/pinned posts
and their engagement rate against follower count:

| Account | Post | Likes | Followers | Rate |
|---|---|---|---|---|
| Shaadi.com | ["The Damad" reel](https://www.instagram.com/p/DcbF4UIIsXQ/) | 49 | 312K | 0.016% |
| BharatMatrimony | (hover count on grid) | 6 | 89.6K | 0.007% |
| Coffee Meets Bagel | (hover count on grid) | 119 | 467K | 0.025% |
| Happn India | [Friends reel](https://www.instagram.com/p/DbqMhRYo1z1/) | 26 | 152K | 0.017% |
| QuackQuack | [meme repost](https://www.instagram.com/p/Db-C8ceT6Fm/) | 55 | 205K | 0.027% |
| Betterhalf | [pinned 2024 post](https://www.instagram.com/p/C55zPauIvd2/) | 215 | 141K | 0.15% |
| Knot.dating | [brand film](https://www.instagram.com/p/DaPNaRXzOZz/) | 76 | 37.7K | 0.20% (small account, real engaged comments) |
| Bumble (brand) | [carousel](https://www.instagram.com/bumble_india/p/DcVX_8ojoO7/) | 244 | 238K | 0.10% |
| **Bumble × @ahillyeah** | [creator reel](https://www.instagram.com/ahillyeah/reel/DcGeS7nvFIY/) | **11,600** | — | **~2%+ on the creator's own base** |
| **Aisle brand film** | [pinned campaign](https://www.instagram.com/p/DTDGjvjAboi/) | **6,238** | 158K | **3.9%** |

The gap isn't small — it's the difference between a rounding error and an actual result. **Only two
things broke the pattern across all 24 accounts**: (1) creator/UGC-partnership content (Bumble, and
Plenty of Fish's recent testimonial-to-camera reels), and (2) one genuinely produced brand-campaign
film with a real emotional thesis (Aisle's "Better Because of Love"). Everything else — daily-caption
carousels, meme reposts, punny type-overlays — reads as noise regardless of account size or post
volume. BharatMatrimony posting **4,892 times** for single-digit likes per post is the starkest version
of this: volume without a format that works is just cost.

## New finding: a real public reputation risk sits inside Betterhalf's comment section

Betterhalf's [second pinned post](https://www.instagram.com/p/C5z_DRxok2i/) (2024, IPL-themed, still
live) has its top comments — unmoderated, still visible — reading: *"organized scam and I'll be
reporting this to our consumer court," "Worst app ever, even after payment, still not getting
response," "They never delete your profile even on your request, so most profiles you see are dead,"*
and *"membership ke baad paise mangte hai like brokers."* This is first-party, public evidence — not a
hypothesis — of exactly the trust failure `rules/creative-style.md` already cites for Shaadi/Jeevansathi
("verification failures and scams"). It also makes Riteangle's actual promise ("Real match guaranteed.
If a match goes quiet, we replace it") land as a direct, checkable answer to a documented competitor
complaint, not a generic trust claim.

## Positioning notes worth carrying into `ad-ideation`

- **Knot.dating explicitly sells income and Aadhaar verification as a feature**, openly discussed in
  its own comments ("the income Aadhaar verification thing is actually smart"). This is a live example
  of a competitor doing the exact thing `rules/targeting.md`'s provider-energy rule forbids us from
  doing in copy — useful as a contrast case, not a model.
- **FRND (583K followers, voice-first, "for people who love talking")** is the single largest
  India-relevant account on the whole list and the closest category-mate to Riteangle's AI-conversation
  mechanic. It positions as social/friendship rather than romantic, which may be why it isn't in the
  matrix's dating rows — but it's the account most worth a deeper follow-up if VoiceAI positioning
  becomes a priority.
- **Tinder India runs almost no daily-feed content and instead does recurring IRL/cultural-moment
  campaigns** (QueerMadeWeekend, a Diesel collab, consent-focused content, "Camp Tinder" mixers).
  Different playbook entirely from feed-content — worth knowing this is Tinder's actual strategy before
  benchmarking our feed performance against theirs.
- **Happn India's astrology-themed highlights** ("Astro Crush") are a concrete example of India-specific
  cultural adaptation beyond generic swipe-app tropes — a possible unused angle for us.
- **Shaadi.com's hook line** — "Sirf scroll karoge ya kabhi phere bhi loge?" ("Will you just scroll, or
  actually get married?") — directly attacks swipe/scroll culture from the matrimony side. Structurally
  similar to our own "No swiping. Ever." but from the opposite direction (attacking casual apps by name
  vs. attacking the swipe mechanic itself).

## Suggested next step

Same as the first pass: feed the Bumble/Aisle creator and brand-film patterns into `ad-ideation` as
reference hooks. New addition — the Betterhalf reputation-risk finding is strong enough to be worth a
line in ad copy testing (something adjacent to "Real match guaranteed" positioned as a direct answer to
"my membership fee bought silence"), subject to `rules/compliance.md` review before it ships.

---

## Addendum — 27 Aug 2026: accounts the 26 Aug sweep missed

The sweep above called itself a full pass over "all 24 competitors named in the matrix Sree shared."
That matrix was the boundary, not the market. One account found during a 27 Aug scanning session was
not on it:

| Name | Handle | Market | Positioning | Assets held |
|---|---|---|---|---|
| VLNCY | [@vlncy.dating](https://www.instagram.com/vlncy.dating/) | Bangalore only | "50:50 men-to-women ratio, guaranteed"; "Equality doesn't mean *more* choices. It means *better* choices."; compatibility-based matching; tagline DATE WITHOUT SURPRISES | `vlncy.dating/` — 3 files |

See `research/notes/note-2026-08-27-vlncy-pool-balance-positioning.md` for the full read, and
`lrn-2026-08-27-vlncy-owns-better-not-more` for why it matters to the women's lane.

**Assets now persist.** The tooling limitation recorded above — that no competitor image could be
saved — was a browser-tool limitation, not a repo one. Screenshots handed over directly save fine.
`shaadi.com/` and `vlncy.dating/` hold real files as of this date. The same NOT-SHIPPABLE rule in
`README.md` governs them: reference for a brief, never reuse.

---

## Addendum — 28 Aug 2026: adjacent-category reference (`_adjacent-category/`)

25 phone screenshots handed over 28 Aug 2026. **None of these accounts is a dating competitor**, so
they are not rows in the matrix above and they are not filed as competitors. They are kept because
they sell to the same person the `FLOODED-WOMAN` and `CASUAL-SELECTIVE` lanes are aimed at — Indian
women 18–30 on Instagram — and because categories with a product to photograph show the format split
more cleanly than dating does. Same NOT-SHIPPABLE rule as everything else in this folder.

| Account | Category | Assets | What it is here for |
|---|---|---|---|
| [@newme.asia](https://www.instagram.com/newme.asia/) | Fashion D2C | `_adjacent-category/newme.asia/` — 4 | Posts built to be forwarded share at 0.40–0.49; the produced product carousel shares at 0.16 |
| [@nykaafashion](https://www.instagram.com/nykaafashion/) | Fashion marketplace | `_adjacent-category/nykaafashion/` — 6 | A repeating brand template at 90–177 likes against one untemplated diary line at 576 |
| [@heynnnow](https://www.instagram.com/heynnnow/) | Fashion (NNNOW by Arvind) | `_adjacent-category/heynnnow/` — 2 | The same sibling occasion as newme, same week, for **1 like**; plus a reel carrying Instagram's own "AI content" label |
| [@durex.india](https://www.instagram.com/durex.india/) | Sexual wellness | `_adjacent-category/durex.india/` — 3 | 116K likes on a brand-voice still, and 65.8K shares against 37.6K likes on another — the only thing seen anywhere that beats every creator in this set |
| @lamastoreindia, @gametheoryindia | Paid ads caught in scroll | `_adjacent-category/misc-paid/` — 2 | One phone-grade UGC ad, one price-and-discount ad; format specimens only |
| [@induviduality](https://www.instagram.com/induviduality/) | Illustrator (Indu Harikumar) | `_organic-creators/induviduality/` — 8 | Eight years of reader-submitted dating stories holding a women's audience with no brand and no budget |

**One warning that must travel with this folder.** Four of the eight `induviduality` posts are
sexually explicit. That account is filed as a lesson about a *mechanic* — ask your audience for the
story, illustrate it, name the series — and is **not** a creator-partnership candidate. Nothing about
it survives Meta's dating-vertical scrutiny (`lrn-2026-08-28-meta-dating-needs-written-permission`)
or the Apple 1.1.4 history behind `rules/compliance.md`.

Full reads: `research/notes/note-2026-08-28-fashion-feed-format-split.md`,
`note-2026-08-28-durex-moment-jack.md`, `note-2026-08-28-induviduality-crowdsourced.md`.
