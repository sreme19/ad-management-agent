# Generation-surface registry

Driven through the user's logged-in Chrome. Login status verified per session —
do not assume. Add a tool the moment it's tried; retire one that keeps failing the
gates.

## Round-1 lineup — face-forward stills (image)
| Tool | Surface | Strength | Login | Notes |
|---|---|---|---|---|
| Grok Imagine | grok.com / x.com/i/grok | photographic, in-house default | ? | watermark lands in corner — croppable |
| ChatGPT (GPT-image) | chatgpt.com | strong prompt adherence, faces | likely (in dl-allowlist) | can garble; good at direction |
| Gemini (Imagen / "nano banana") | gemini.google.com | photoreal people, editing | ? | strong at realistic Indian faces |
| Midjourney | midjourney.com | highest craft ceiling | ? (seat needed) | user-driven if gated |
| Ideogram | ideogram.ai | text-in-image (we overlay text, so lower priority) | ? | keep for end-card tests |

## Round-3 lineup — AI video
Opened 2026-08-28. Sora is retired before use: discontinued, API sunsets 2026-09-24, and it
never launched in India.

| Tool | Surface | Strength | Login | Notes |
|---|---|---|---|---|
| Google Flow (Veo) | labs.google/flow | motion-graphics formats; holds character across panels | yes (used 2026-08-28) | **Tried, round 3.** Defaulted to 1280x720 landscape — specify vertical explicitly. Backgrounds default Western. Free tier is Omni Flash, 15 credits/generation |
| Seedance 1.5 Pro | fal.ai | vertical native, audio included | — | ~$0.58 / 5s at 1080x1920. fal is India-payable (prepaid USD). No Hindi lip-sync |
| Wan 2.2 Animate | fal.ai (Apache-2.0, self-hostable) | motion + expression transfer from a reference video | — | `Move` mode only — `Replace` is face-swap and fails compliance. $0.08/video-sec at 720p |
| Kling | klingai.com | Motion Control, Cinema Studio, first/last-frame | ? | pricing and 9:16 support unverified |
| Runway | runwayml.com | VFX applied to real footage, not full generation | ? | $0.60 / 5s |
| ~~Sora~~ | — | — | — | **Retired unused** — no India availability, API sunsets 2026-09-24 |
