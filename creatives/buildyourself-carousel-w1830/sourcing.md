# Sourcing — one block per slide, in place of `prompts.md`

`creative-generation.md` §9 asks for `prompts.md` to hold "the full prompt text as
pasted into Grok" per variant. No new prompt was written for any slide here — this
file holds what §9 actually needs in that case: the exact source file behind each
asset, so a ranked read can still be attached to a specific input later via
`log-review`.

| Ad variant | File | Copy | Source | Notes |
|---|---|---|---|---|
| A | `a-ghosted/asset-a.jpg` | "Phir se ghost kar diya?" | `buildyourself-lead-w1830/_source/frames/Woman_sitting_on_bedroom_floor_202608292351.jpeg` | Meera, native 768×1376 — no crop needed. |
| B | `b-catfish/asset-a.jpg` | "Profile kuch aur, aadmi kuch aur." | `.../Woman_reading_laptop_at_cafe_202608292356.jpeg` | Native portrait. |
| C | `c-alone/asset-a.jpg` | "Kab tak?" | `.../Woman_sitting_alone_at_table_202608292351.jpeg` | Swapped in for a frame that put a man in sharp focus — see `brief.md`. |
| D | `d-enough/asset-a.jpg` | "Bas. Ab nahin." | `.../Tired_woman_looking_at_phone_202608292351.jpeg` | Native portrait. |
| E | `e-turn/asset-a.jpg` | "Khud ko bana sakti ho." | `.../Four_women_looking_into_camera_202608300008.jpeg` | The 4-panel collage — full width, letterboxed, not cropped (cropping it destroys the grid). |
| F | `f-strength/asset-a.jpg` | "Pehle apni taakat." | `.../Woman_completing_heavy_barbell_d…_202608300000.jpeg` | Landscape 1376×768, centre-cropped to 9:16. |
| G | `g-win/asset-a.jpg` | "Pehle apni jeet." | `buildyourself-lead-w1830/_source/clips/grok-video-90565286-….mp4` @ t=8.2s | Not a Flow still — pulled from the Grok animation at the toss's contact moment, per Sree's ask for the airborne serve. See `_derived/README.md` for the exact extraction command. |
| H | `h-calm/asset-a.jpg` | "Pehle apna sukoon." | `.../Woman_meditating_on_balcony_at_202608300006.jpeg` | Centre-cropped. |
| I | `i-world/asset-a.jpg` | "Pehle apni duniya." | `.../Woman_breathing_at_coastal_overlook_202608300006.jpeg` | Centre-cropped; picked over the back-to-camera cliff shot to stay clear of §4's "back-to-camera reveal" signifier. |
| J | `j-joy/asset-a.jpg` | "Pehle apni khushi." | `.../Woman_laughing_on_rooftop_terrace_202608300005.jpeg` | Centre-cropped. |
| K | `k-career/asset-a.jpg` | "Pehle apna career." | `.../Woman_smiling_in_modern_office_202608300005.jpeg` | Picked over the presenting-in-meeting-room frame to avoid the vest-top-in-a-boardroom wardrobe fault logged against the video. |
| L | `l-close/asset-a.jpg` | "Pehle tum. Phir koi aur." | `.../Four_women_standing_in_space_202608300005.jpeg` | Plain landscape group shot, letterboxed same as E for visual bookending. |
| M | `m-endcard/asset-a.jpg` | wordmark + tagline + CTA | same file as L, heavier dark wash | New type layer only — no photo content beyond L's. |

All type set in `build.py`, real Gabarito, white body / brand-pink `#FF3B6B`
keyword, on a dark footer gradient over the source photo — matching the shipped
video's on-screen treatment, not `moveon-properly-w2530`'s cream-card style
(different creative family).
