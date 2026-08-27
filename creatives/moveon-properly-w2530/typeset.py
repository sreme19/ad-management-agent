"""Type layer for the MOVE-ON-PROPER plate (bake-off winner c5, Gemini).

    uv run python creatives/moveon-properly-w2530/typeset.py

Per rules/creative-generation.md §2 the plate carries no words; every glyph is
set here in the real Gabarito so casing and the lowercase 'riteangle' spelling
are exact. Mirrors fourteen-suitors-w1822/typeset.py.

The plate (c5) is a cream-palette photo, not an empty wall, so unlike the
fourteen-suitors plates this one needs a soft cream scrim at the foot to keep the
tagline + wordmark legible over her top — and that scrim also covers Gemini's
small corner watermark, so no aggressive crop is needed.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"
D = Path("/Users/performek5/Desktop/Code/ad-management-agent/creatives/moveon-properly-w2530")
CAND = D.parent / "_bakeoff/round-01-moveon/candidates"

INK  = "#1B1020"   # creative-style.md
PINK = "#FF3B6B"
CREAM = (255, 243, 240)   # #FFF3F0 ground

MARGIN = 84
OUT = (1080, 1920)
SAFE_TOP, SAFE_BOTTOM = 192, 1632   # §7 platform chrome sits outside these


def face(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def fit(dr, text, size, weight, max_w):
    """Shrink until text fits max_w. Returns the font that fits."""
    while size > 20:
        f = face(size, weight)
        if dr.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return face(size, weight), size


def prepare(src, clean):
    """winner plate -> exact 1080x1920, 9:16, centre-cropped."""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    tgt = W * 16 / 9
    if H > tgt:                      # too tall -> trim height evenly
        off = int((H - tgt) / 2)
        im = im.crop((0, off, W, off + int(tgt)))
    else:                            # too wide -> trim width evenly
        tgtw = int(H * 9 / 16)
        off = (W - tgtw) // 2
        im = im.crop((off, 0, off + tgtw, H))
    im = im.resize(OUT, Image.LANCZOS)
    im.save(D / clean, quality=95, subsampling=0)
    print(f"{Path(src).name} -> {clean} {im.size[0]}x{im.size[1]}")


def scrim(im, top_y, strength=0.94, solid_from=1700):
    """Cream gradient from transparent at top_y to `strength`, then fully opaque
    below solid_from — the opaque footer both seats the wordmark and hides
    Gemini's corner watermark, which sits in the bottom right."""
    W, H = im.size
    grad = Image.new("L", (1, H), 0)
    for y in range(top_y, H):
        if y >= solid_from:
            a = 255
        else:
            a = int(255 * strength * (y - top_y) / (solid_from - top_y))
        grad.putpixel((0, y), a)
    alpha = grad.resize((W, H))
    band = Image.new("RGB", (W, H), CREAM)
    im.paste(band, (0, 0), alpha)


def draw_lines(dr, lines, top, size, weight="ExtraBold", leading=1.12):
    f = face(size, weight)
    y = top
    for text, colour in lines:
        dr.text((MARGIN, y), text, font=f, fill=colour)
        y += int(size * leading)
    return y


def wordmark(dr, y, size=54):
    f = face(size, "Bold")
    dr.text((MARGIN, y), "rite", font=f, fill=INK)
    w = dr.textlength("rite", font=f)
    dr.text((MARGIN + w, y), "angle", font=f, fill=PINK)


def build(clean, dest):
    im = Image.open(D / clean).convert("RGB")
    scrim(im, top_y=1430)                        # foot only; her face stays clean
    dr = ImageDraw.Draw(im)

    # Hook — top third, on clean cream wall. Auto-fit so it never overflows.
    max_w = OUT[0] - 2 * MARGIN
    f1, s1 = fit(dr, "Move on toh karna hai —", 76, "ExtraBold", max_w)
    dr.text((MARGIN, 236), "Move on toh karna hai —", font=f1, fill=INK)
    f2, _ = fit(dr, "par dhang se.", s1, "ExtraBold", max_w)
    dr.text((MARGIN, 236 + int(s1 * 1.12)), "par dhang se.", font=f2, fill=PINK)

    # Tagline + wordmark — on the cream scrim, kept above the §7 safe line 1632.
    ft, st = fit(dr, "Verified, not vibes.", 62, "ExtraBold", max_w)
    dr.text((MARGIN, 1466), "Verified, not vibes.", font=ft, fill=INK)
    wordmark(dr, 1466 + int(st * 1.15))

    im.save(D / dest, quality=95, subsampling=0)
    print(f"{dest} written ({im.size[0]}x{im.size[1]})")


prepare(CAND / "gemini-3-beautiful.png", "clean-c5.jpg")
build("clean-c5.jpg", "asset-c5-a.jpg")
