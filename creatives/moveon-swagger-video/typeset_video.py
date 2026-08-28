"""Type layer for the MOVE-ON-PROPER swagger video (Google Flow, round 4).

    uv run python creatives/moveon-swagger-video/typeset_video.py

Video sibling of moveon-properly-w2530/typeset.py. Same rule, same reason: per
rules/creative-generation.md §2 the plate carries no words, so Flow generates
picture only and every glyph is set here in the real Gabarito. That keeps the
lowercase 'riteangle' spelling exact (it carries the pun), keeps the ad
re-cuttable — a new hook is a string edit, not a regeneration — and keeps the
§7 safe areas honest.

Layout note, learned the hard way on this export. Flow's "9:16" setting gives a
vertical *canvas*, not vertical *footage*: the 720x1280 file carried a 720x702
near-square picture inset on white. Cropping 9:16 out of that would throw away
half the width and upscale a ~395px-wide source, so instead the picture is
seated as a rounded card on the cream ground, with type above and below it.
Flow's white surround becomes a deliberate #FFF3F0 frame, and the captions sit
on clean ground rather than fighting the footage. The crop is detected per
file, so a later full-bleed export needs no code change.

What it does, in one ffmpeg pass:
  1. finds and crops off Flow's white surround
  2. seats the real picture as a rounded card on a 1080x1920 cream ground
  3. draws each timed caption above the card, tagline + wordmark below
  4. appends a cream end card
  5. normalises audio to -14 LUFS

That last one is not cosmetic. The round-3 Flow export peaked at exactly
-0.0 dBFS against a -20.4 dB mean, which clips harshly on phone speakers.

Drop the Flow export in this folder as `source.mp4` and run. Output is
`asset-a.mp4`.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"
D = Path(__file__).parent

# creative-style.md visual identity
INK = "#1B1020"
PINK = "#FF3B6B"
CREAM = (255, 243, 240)  # #FFF3F0

OUT = (1080, 1920)
MARGIN = 84
SAFE_TOP, SAFE_BOTTOM = 192, 1632  # §7 — platform chrome sits outside these

SRC = D / "source.mp4"
DEST = D / "asset-a.mp4"
BUILD = D / "_build"

END_CARD_SECONDS = 2.0

CARD_W = 1000
CARD_X = (OUT[0] - CARD_W) // 2
CARD_Y = 430
CARD_RADIUS = 28

# The type layer. Change a string here and re-run — that is the whole point of
# keeping words out of the generator.
CAPTIONS = [
    (0.0, 2.0, [("Move on karne ko", INK), ("sab bolte hain.", INK)]),
    (2.0, 4.0, [("Kaise karna hai,", INK), ("woh koi nahi batata.", INK)]),
    (4.0, 6.2, [("Dhang se.", PINK)]),
]

CAPTION_SIZE = 76
FOOT_TAGLINE = "Verified, not vibes."
END_TAGLINE = "Verified, not vibes."


def face(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def fit(dr, text, size, weight, max_w):
    """Shrink until text fits max_w. Returns (font, size)."""
    while size > 20:
        f = face(size, weight)
        if dr.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return face(size, weight), size


def wordmark(dr, y, size=54, x=MARGIN):
    """'rite' in ink, 'angle' in pink — two draws so the pun is exact."""
    f = face(size, "Bold")
    dr.text((x, y), "rite", font=f, fill=INK)
    w = dr.textlength("rite", font=f)
    dr.text((x + w, y), "angle", font=f, fill=PINK)


def furniture_png(lines, card_h, path):
    """One full-frame layer: cream everywhere, with a rounded transparent hole
    where the footage shows through. Because the hole is punched here, the card
    gets its rounded corners for free and the type sits on clean ground."""
    im = Image.new("RGBA", OUT, CREAM + (255,))
    max_w = OUT[0] - 2 * MARGIN

    # Punch the card hole.
    hole = Image.new("L", OUT, 255)
    ImageDraw.Draw(hole).rounded_rectangle(
        [CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + card_h],
        radius=CARD_RADIUS, fill=0,
    )
    im.putalpha(hole)

    dr = ImageDraw.Draw(im)

    # Caption, in the cream band above the card.
    size = min(fit(dr, t, CAPTION_SIZE, "ExtraBold", max_w)[1] for t, _ in lines)
    font = face(size, "ExtraBold")
    leading = int(size * 1.12)
    y = CARD_Y - 40 - leading * len(lines)
    y = max(y, SAFE_TOP + 20)
    for text, colour in lines:
        dr.text((MARGIN, y), text, font=font, fill=colour)
        y += leading

    # Tagline + wordmark, in the cream band below the card.
    foot = CARD_Y + card_h + 48
    ft, st = fit(dr, FOOT_TAGLINE, 56, "ExtraBold", max_w)
    dr.text((MARGIN, foot), FOOT_TAGLINE, font=ft, fill=INK)
    wordmark(dr, foot + int(st * 1.28), size=46)

    im.save(path)
    return path


def end_card_png(path):
    """Cream ground, tagline, wordmark. Appended after the footage rather than
    laid over it — Flow's last frame is her face, the wrong place for a
    wordmark."""
    im = Image.new("RGB", OUT, CREAM)
    dr = ImageDraw.Draw(im)
    max_w = OUT[0] - 2 * MARGIN

    ft, st = fit(dr, END_TAGLINE, 82, "ExtraBold", max_w)
    y = (OUT[1] - st) // 2 - 60
    dr.text((MARGIN, y), END_TAGLINE, font=ft, fill=INK)
    wordmark(dr, y + int(st * 1.5), size=60)

    im.save(path)
    return path


def probe(src):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(src)],
        capture_output=True, text=True, check=True,
    ).stdout
    info = json.loads(out)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    return int(v["width"]), int(v["height"]), float(info["format"]["duration"]), has_audio


def content_box(src, w, h):
    """Find the real picture inside Flow's white surround. cropdetect only
    understands black borders, so the frame is negated first."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(src), "-vf",
         "negate,cropdetect=limit=0.08:round=2:reset=0", "-frames:v", "120",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    hits = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", r.stderr)
    if not hits:
        return w, h, 0, 0
    cw, ch, cx, cy = (int(v) for v in hits[-1])
    if cw < w * 0.4 or ch < h * 0.2:  # implausible — trust the full frame
        return w, h, 0, 0
    return cw, ch, cx, cy


def build():
    if not SRC.exists():
        sys.exit(f"no source video at {SRC}\n"
                 f"Export from Flow and save it there as source.mp4")

    BUILD.mkdir(exist_ok=True)
    w, h, dur, has_audio = probe(SRC)
    cw, ch, cx, cy = content_box(SRC, w, h)
    print(f"source: {w}x{h}, {dur:.2f}s, audio={'yes' if has_audio else 'no'}")
    if (cw, ch) != (w, h):
        print(f"  Flow surround detected — real picture is {cw}x{ch} at +{cx}+{cy}")

    card_h = round(CARD_W * ch / cw)
    if CARD_Y + card_h + 200 > SAFE_BOTTOM:
        print(f"  WARNING: card is {card_h}px tall and crowds the §7 bottom safe line.")
    print(f"  card: {CARD_W}x{card_h} at +{CARD_X}+{CARD_Y}")

    furn = [furniture_png(lines, card_h, BUILD / f"furn{i}.png")
            for i, (_, _, lines) in enumerate(CAPTIONS)]
    card = end_card_png(BUILD / "endcard.png")

    inputs = ["-i", str(SRC)]
    for p in furn:
        inputs += ["-i", str(p)]
    inputs += ["-loop", "1", "-t", str(END_CARD_SECONDS), "-i", str(card)]

    fc = [
        # Cream ground, and the footage cropped free of Flow's white surround.
        f"color=c=0x{CREAM[0]:02X}{CREAM[1]:02X}{CREAM[2]:02X}:"
        f"s={OUT[0]}x{OUT[1]}:d={dur},fps=30[bg]",
        f"[0:v]crop={cw}:{ch}:{cx}:{cy},scale={CARD_W}:{card_h},setsar=1,fps=30[pic]",
        f"[bg][pic]overlay={CARD_X}:{CARD_Y}[seated]",
    ]
    cur = "seated"
    for i, (start, end, _) in enumerate(CAPTIONS):
        nxt = f"v{i}"
        fc.append(f"[{cur}][{i + 1}:v]overlay=0:0:"
                  f"enable='between(t,{start},{end})'[{nxt}]")
        cur = nxt

    card_idx = len(furn) + 1
    fc.append(f"[{card_idx}:v]scale={OUT[0]}:{OUT[1]},setsar=1,fps=30[card]")
    fc.append(f"[{cur}][card]concat=n=2:v=1:a=0[vout]")

    if has_audio:
        fc.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,asetpts=N/SR/TB[a0]")
        fc.append(f"anullsrc=channel_layout=stereo:sample_rate=44100,"
                  f"atrim=0:{END_CARD_SECONDS}[a1]")
        fc.append("[a0][a1]concat=n=2:v=0:a=1[aout]")
        amap = ["-map", "[aout]", "-c:a", "aac", "-b:a", "128k"]
    else:
        amap = ["-an"]

    cmd = (["ffmpeg", "-y"] + inputs
           + ["-filter_complex", ";".join(fc), "-map", "[vout]"] + amap
           + ["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
              "-crf", "18", "-movflags", "+faststart", str(DEST)])

    print("running ffmpeg…")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit("ffmpeg failed")

    ow, oh, odur, _ = probe(DEST)
    print(f"{DEST.name} written — {ow}x{oh}, {odur:.2f}s")


if __name__ == "__main__":
    build()
