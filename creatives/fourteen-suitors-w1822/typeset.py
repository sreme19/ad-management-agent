"""Type layer for the FOURTEEN-SUITORS plates.

Lives beside the creative, not in scripts/, for the same reason prompts.md does:
it is the reproducible input that produced asset-a.jpg. Re-running it regenerates
the asset exactly; editing a line here is how the next variant gets cut.

    python3 creatives/fourteen-suitors-w1822/typeset.py

Per rules/creative-generation.md §2 the plate carries no words; every glyph is
set here, in the real Gabarito, so casing and palette are exact rather than
retyped by hand each time a variant is cut.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"
D = Path("/Users/performek5/Desktop/Code/ad-management-agent/creatives/fourteen-suitors-w1822")

INK  = "#1B1020"   # creative-style.md
PINK = "#FF3B6B"

MARGIN = 84
SAFE_TOP, SAFE_BOTTOM = 192, 1632      # §7: platform chrome sits outside these


# Grok stamps its watermark in a fixed box at the bottom right. It sits in the
# bottom 4% of the frame, which is dead space on both plates, so it comes off by
# CROP rather than by inpainting — no invented pixels. Inpainting was tried first
# and left a visibly soft patch; see qa.md.
CROP_H = 1716                      # watermark's top edge is at y=1716 in the raw
CROP_W = round(CROP_H * 9 / 16)    # 965 — keeps 9:16 while trimming symmetrically
OUT = (1080, 1920)                 # Snap / Meta Story spec


def prepare(raw, clean):
    """raw plate -> watermark-free 1080x1920, ready for type."""
    im = Image.open(D / raw).convert("RGB")
    W, _ = im.size
    off = (W - CROP_W) // 2
    im = im.crop((off, 0, off + CROP_W, CROP_H)).resize(OUT, Image.LANCZOS)
    im.save(D / clean, quality=95, subsampling=0)
    print(f"{raw} -> {clean} {OUT[0]}x{OUT[1]}")


def face(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def draw_lines(dr, lines, top, size, weight="ExtraBold", leading=1.10, x=MARGIN):
    """lines: list of (text, colour). Returns the y the block ends at."""
    f = face(size, weight)
    y = top
    for text, colour in lines:
        dr.text((x, y), text, font=f, fill=colour)
        y += int(size * leading)
    return y


def wordmark(dr, y, size=52, x=MARGIN):
    """Lowercase always — the casing and the 'rite' spelling carry the pun."""
    f = face(size, "Bold")
    dr.text((x, y), "rite", font=f, fill=INK)
    w = dr.textlength("rite", font=f)
    dr.text((x + w, y), "angle", font=f, fill=PINK)


def build(src, dest, headline, head_top, head_size, mark_y):
    im = Image.open(D / src).convert("RGB")
    dr = ImageDraw.Draw(im)
    draw_lines(dr, headline, head_top, head_size)
    wordmark(dr, mark_y)
    im.save(D / dest, quality=95, subsampling=0)
    print(f"{dest} written ({im.size[0]}x{im.size[1]})")


HEADLINE = [
    ("Stop scrolling", INK),
    ("through guys who", INK),
    ("just want attention.", PINK),
]

prepare("raw-a.jpg", "clean-a.jpg")
prepare("raw-b.jpg", "clean-b.jpg")

# A — the wall is empty from the top to roughly y=1000, so the block sits high.
# Wordmark sits under the headline, not at the foot: the foot of this frame is
# table, phone and hand, where an ink mark loses contrast and legibility.
build("clean-a.jpg", "asset-a.jpg", HEADLINE, head_top=250, head_size=96, mark_y=632)

# B — only the top ~500px is clear wall, so the type is tighter and smaller.
build("clean-b.jpg", "preview-b.jpg", HEADLINE, head_top=200, head_size=74, mark_y=490)
