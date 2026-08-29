# Edit script — ENERGY KAHAN JAATI HAI · 20s · 9:16 Meta Reels/Stories

Assembly sheet for the four clips generated 2026-08-29. Timecodes are the finished cut; IN/OUT are
points in the source files.

**Every type card is unvalidated Hinglish.** No native speaker in the target register has read this
copy. That is a spend gate, not an edit gate — cut it, but hold the buy.

## Source clips

| # | file | usable window | the beat |
|---|---|---|---|
| A | `Woman_reacting_to_phone_message_202608291131.mp4` | 0–9s | eye-roll at ~8s |
| B | `Woman_reading_phone_in_library_202608291153.mp4` | 4–10s | phone face-down + private smile at ~9.6s |
| C | `Woman_puts_phone_down_at_202608291144.mp4` | 4–10s | the turn into golden light at ~9.5s |
| D | `Women_dancing_at_wedding_reception_202608291207.mp4` | 1–8s | the four-way laugh at ~2.5s |

All four are 720×1280. All four carry a Flow watermark bottom-right that must be cropped.

## The cut

```
┌─ 0:00 ──────────────────────────────────────────────── DRAIN ─┐
0:00.0   CLIP A   IN 5.0  OUT 9.0   (4.0s)   Meher, bedroom, night
         0:00.3   TYPE   Ghosting.
         0:02.0   TYPE   Fake profiles.
         Her face is flat. At 0:03 she rolls her eyes and drops her head
         back — CUT ON THE EYE-ROLL, not after it.
         HARD CUT

0:04.0   CLIP B   IN 5.8  OUT 9.8   (4.0s)   Kavya, library, day
         0:04.3   TYPE   Cheating.
         0:06.0   TYPE   Teen hafte ki texting jo kahin nahi jaati.
         She frowns at the phone, turns it face-down, goes back to her book.
         CUT ON the small private smile.
         HARD CUT

┌─ 0:08 ───────────────────────────────────────────────── TURN ─┐
0:08.0   CLIP C   IN 5.0  OUT 13.0  (5.0s)   Anaya, office, late afternoon
         0:09.0   TYPE   Ab samajh aaya energy kahan jaati hai?
         Phone face-down, pushed away. She sits back and looks out, and the
         light goes from grey to gold on her face. HOLD to the gold — this
         is the hinge of the film and it needs the extra second.
         SOFT CUT / 6-frame dissolve — the only soft transition in the cut

┌─ 0:13 ──────────────────────────────────────────────── PAYOFF ─┐
0:13.0   CLIP D   IN 1.0  OUT 8.0   (7.0s)   The wedding, all four
         0:13.5   TYPE   Date mat karo. Bas milo, aur jiyo.
         The four-way laugh lands at ~0:14.5. Let it play.
         0:17.0   TYPE   Apply karo →          + riteangle brand mark
         0:20.0   END
```

## Type treatment

- **Set in Gabarito.** The lowercase `riteangle` mark is non-negotiable brand (`creative-style.md`),
  and romanised Hinglish sets in Gabarito cleanly. No Devanagari in this cut —
  `lrn-2026-08-29-roman-script-is-an-audience-signal` says Devanagari signals a Hindi-heartland or
  older audience, so it is a separate test, not a styling choice.
- **All type overlaid in edit, never generated** (`creative-generation.md` §2).
- **Safe zones: nothing in the top 14% or bottom 20%.** Reels UI covers both. The `Apply karo →`
  card is the one that must not be eaten — put it in the middle third, not at the foot of frame.
- Drain cards are single words, hard on and hard off, no animation. The payoff card can hold.

## Audio

- **No dialogue anywhere in the cut.** `compliance.md` §6.2 — a generated woman narrating a
  first-person experience of Riteangle is what blocked the last MOVE-ON video. Silence is what makes
  this format shippable.
- **Clip D's own audio reads −19.6 dB mean, the profile of continuous content.** Check it by ear
  before using; strip it if there is any intelligible speech.
- **Bed a single music track across the whole cut** rather than using clip audio — it also masks the
  four clips having been generated separately. Meta Sound Collection or Flow-generated audio only; a
  commercial track is a licensing problem on a paid ad.
- **The cut must work muted.** Most Reels views are silent, so the type carries the entire argument
  on its own. Watch it with the sound off before approving.

## Known compromises, recorded rather than hidden

1. **The cast does not carry across scenes.** The film was designed so the woman drained in scene 1
   is the woman laughing in scene 4 — same face, both ends. Flow did not hold the cast
   (`lrn-2026-08-29-flow-character-reference-is-unreliable`), so clip D features women who do not
   match the earlier three. The ad still reads as "this happens / this is the alternative"; it no
   longer reads as "this happened to *her*". Accepted for this cut.
2. **Clip C's office is placeless** — glass-and-white corporate, the one shot that could be anywhere
   on earth. It is also the hinge, so it is the highest-value reshoot if there is another round.
3. **720×1280 against Meta's recommended 1080×1920**, then recompressed on delivery.
4. **Clip D has men visible in the background crowd** and sarees rather than the specified kurtas.
   Wardrobe was ruled the app owner's call on 2026-08-29.

## Before this spends a rupee

- [ ] Native-speaker read of every Hinglish line
- [ ] Listen to clips B and D for generated speech
- [ ] Watermarks cropped on all four
- [ ] Watched muted, end to end
- [ ] `destinations.yaml` `/get/w-apply` still says `paid_traffic: false` until a real arrival is
      seen in `marketing_page_views` under `page=get_w_apply`
