# Round 02 ledger — /get/w landing imagery

**Round status: DISPATCHED 2026-08-27 evening**, after the Claude-in-Chrome
extension reconnected (the fix was a full Chrome restart after re-login). Three
slots, one Gemini fresh-chat candidate each, driven through the user's Chrome per
`README.md`. All three accepted on first generation — no re-rolls needed, which
says more about the sharpened prompts (mid-laugh / mid-step / blank-screens) than
about luck; round 1 needed five candidates for one hero.

## Generated candidates — scores /37.5

| id | slot | gates | stop-scroll ×2 | craft ×2 | brand-fit ×1.5 | palette ×1 | type-space ×1 | **total** |
|---|---|---|---|---|---|---|---|---|
| `gemini-hero-1` | hero | pass* | 4.5 → 9.0 | 4.5 → 9.0 | 5.0 → 7.5 | 5 → 5.0 | 3.5 → 3.5 | **34.0** |
| `gemini-moment-1` | moment | pass* | 4.0 → 8.0 | 4.5 → 9.0 | 4.5 → 6.75 | 4 → 4.0 | 4.0 → 4.0 | **31.75** |
| `gemini-phones-1` | interface | pass* | 3.5 → 7.0 | 5.0 → 10.0 | 4.5 → 6.75 | 5 → 5.0 | 5.0 → 5.0 | **33.75** |

\* every gate pass carries a handled caveat — see per-candidate notes. Scored by
the same session that wrote the prompts, so per `README.md` these numbers are
provisional until a second pass re-scores them.

### gemini-hero-1 (896×1200) — ADVANCED, shipped as hero.jpg
Mid-laugh, head tipped, eyes creased, real skin texture (visible acne — reads
human, not retouched), cream room, dusty-rose tee. Exactly the reference's energy
with none of its yellow. Gemini ✦ at (775-815, 1055-1100): **bottom crop at
y=1050 removes it**; the cut lands mid-forearm, an ordinary editorial crop.
34.0 versus the round-1 treatments' 29.75 ceiling — the generation round beat the
best possible grade of the old plate by 4+ points, which settles the "grades
cannot fix this" claim with a number.

### gemini-moment-1 (928×1152) — ADVANCED, shipped as moment.jpg
Mid-step on a real-reading Bangalore street, glancing back laughing, kurta + tote.
Three QA flags, all removed by ONE cut (right crop at x=760): the ✦ at
(790-830, 1030-1075), the garbled background signage ("KAANNA ENGLISH"), and two
distant background men. The men were probably not a §6.1 violation — generated,
distant, backs turned, unidentifiable — but the crop makes the question moot.
Palette 4 not 5: golden-hour sand, warm but not the flat cream ground.

### gemini-phones-1 (928×1152) — ADVANCED, composited into shortlist.jpg
Three phones on cream, centre forward, screens blank as instructed — the plate the
composite pipeline was built for, replacing the round-1 hands-on-bed plate. The
shortlist UI is warped into the CENTRE screen only. Composite lessons that cost
three cuts, recorded in `_web/prep-get-w-images.py`: (1) three white screens mean
threshold alone finds the wrong quad — flood-fill from a seed pixel and use
connectivity, since the bezels separate the regions; (2) this plate's screens are
(239,239,239), under round 1's ≥250 threshold — chroma (spread ≤12 vs the ground's
23+) is the durable test, not brightness; (3) warp to the flood region's BOUNDING
BOX, not its extreme-corner quad — rounded screen corners bulge below the quad's
straight bottom edge, and masked pixels outside the warp source print black
dashes. The ✦ at (785-850, 990-1060) fell to a bottom crop at y=970, which also
matches the reference frames' phones-bleeding-off-the-edge composition.

## Treatment candidates (pre-dispatch, kept for the palette finding)

**Superseded by the generated round above.** Their purpose was served: they
established that a grade cannot fix the round-1 plate (t2-cream tied the shipped
hero at 29.75) and that abandoning cream costs more than monochrome buys
(t1-bw 26.25). Yellow was then ruled out entirely by Sree — the page palette does
not change. No pixels were generated. Both browser surfaces
were unreachable this session (in-app browser blocked by policy; Claude-in-Chrome
extension reported not connected), and per `README.md` generation runs through the
user's logged-in Chrome. The rows below are TREATMENTS of the round-1 hero plate,
run to settle the Bumble-versus-cream palette question without new pixels.

