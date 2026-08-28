---
id: lrn-2026-08-28-setting-google-flow-s-video
subject: creative
claim: 'Setting Google Flow''s video default to 9:16 yields a vertical canvas, not
  vertical footage: the generated picture is near-square and inset on white, so the
  file''s dimensions overstate the usable image'
source: platform-doc
confidence: high
sample_n: null
status: open
created: '2026-08-28'
last_confirmed: '2026-08-28'
review_after: '2027-02-24'
derived_from: note-2026-08-28-google-flow-step-by-step
questions: []
recs: []
promoted_to: null
---

## Claim

Setting Google Flow's video default to 9:16 yields a vertical canvas, not vertical footage: the generated picture is near-square and inset on white, so the file's dimensions overstate the usable image

## Evidence

- (2026-08-28) (2026-08-28) Measured off the round-4 export, Woman_walking_and_laughing_in_202608282045.mp4, generated immediately after Agent settings > Video generation default was switched from 16:9 to 9:16. ffprobe reports 720x1280 h264, 24fps, 6.016s, AAC - correctly vertical. But the real picture is only 720x702 at offset +0+290, letterboxed on white top and bottom. Detected with negate,cropdetect: plain cropdetect returns the full frame because it only recognises BLACK borders and Flow's surround is white. Two consequences. (1) The file's stated dimensions overstate the usable image by nearly half its height, so an aspect-ratio check on ffprobe output alone passes a file that is not actually 9:16 footage - round 3's failure would not have been caught by that check either. (2) Cropping 9:16 out of the 720x702 picture needs a 395px-wide window, which upscaled to 1080 is unusably soft; the workable route is to seat the near-square picture as a card on the cream ground with type above and below, which also puts captions on clean ground rather than over footage. Resolution is a second, separate shortfall: 720x1280 against the 1080x1920 every other asset in this repo uses. Tier was Omni 1.1 Flash, cost 10 credits, both recorded for the first time.
