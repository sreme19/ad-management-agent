"""Web-ready imagery for /get/w, cut from plates this repo already approved.

    uv run python creatives/_web/prep-get-w-images.py

Writes into pocket-dating-coach/static/get-w/. That repo holds the page; this one
holds the plates and the rules they were made under, so the derivation lives here
and only the output crosses over. Re-run to re-cut.

THREE PLATES, ALL ALREADY THROUGH THE WOMEN'S LANE:

  hero.jpg       <- moveon-properly-w2530/clean-c5.jpg (bake-off round-1 winner,
                    Sree-approved). She addresses the camera in an ordinary cream
                    Indian home: rules/creative-generation.md section 1 speaker,
                    not object. Cropped to 3:4 ABOVE y=1650 because Gemini's
                    corner watermark sits below y=1700 — the ad covered it with a
                    cream scrim, the web cut drops it entirely. Cropped out, never
                    inpainted: no invented pixels, same standard the ad's QA used.

  phone-down.jpg <- fourteen-suitors-w1822/clean-a.jpg. Her hand, her chai, her
                    phone face-down on a cafe table. No face, no watermark. This
                    is the closed-tab moment from her POV.

  shortlist.jpg  <- fourteen-suitors-w1822/clean-b.jpg, which was generated with a
                    DELIBERATELY BLANK white screen so an interface could be
                    composited in later. That is what happens here: the screen's
                    four corners are found by thresholding for pure white (the
                    screen is exactly 255,255,255; the brightest bedsheet pixel is
                    204) and the shortlist render is perspective-warped into them.
                    Section 1 calls her interface the strongest available material
                    and no competitor shows one — they all show couples.

WHAT THE SHORTLIST RENDER MAY AND MAY NOT SAY. compliance.md #5 forbids copy
implying a hard numeric ranking of people, while creative-style.md sanctions "an
ordered shortlist" outright — so this shows position in HER list and never a score
or a rating. Faces are initials in circles, never photographs, which keeps it clear
of compliance.md section 6.1 (a man's real unenhanced photo appears nowhere in the
product, so it appears nowhere in its marketing) and matches how /get's own mockups
already draw people. Names are invented and the render is an illustration of the
interface, not a screenshot of anyone's real list.
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"
SRC = Path("/Users/performek5/Desktop/Code/ad-management-agent/creatives")
OUT = Path("/Users/performek5/Desktop/Code/pocket-dating-coach/static/get-w")

INK = (27, 16, 32)  # #1B1020, creative-style.md
PINK = (255, 59, 107)  # #FF3B6B
CREAM = (255, 243, 240)  # #FFF3F0
SURFACE = (251, 238, 233)  # #FBEEE9
HAIRLINE = (239, 222, 215)  # #EFDED7

JPEG = dict(quality=82, optimize=True, progressive=True)


def face(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def crop_ratio(im, top, height):
    """Vertical window at full width, then nothing else — no scaling, no resample."""
    return im.crop((0, top, im.width, top + height))


# ── the shortlist interface ──────────────────────────────────────────────────

ROWS = [
    ("A", "Arjun, 29", "Verified · Indiranagar"),
    ("K", "Karan, 31", "Verified · Koramangala"),
    ("R", "Rohan, 28", "Verified · HSR Layout"),
]


def shortlist_render(w=640, h=1470):
    """The ordered list, drawn at ~3x the screen it lands in so the warp stays sharp."""
    im = Image.new("RGB", (w, h), CREAM)
    dr = ImageDraw.Draw(im)
    pad = 44

    # Header — the wordmark is lowercase and spelled 'rite', always (creative-style.md).
    dr.text((pad, 74), "riteangle", font=face(40, "ExtraBold"), fill=INK)
    dr.text((pad, 156), "Your list", font=face(66, "ExtraBold"), fill=INK)
    dr.text((pad, 226), "In the order you asked for", font=face(34, "Medium"), fill=(120, 104, 116))

    y = 310
    for i, (initial, name, meta) in enumerate(ROWS, start=1):
        card_h = 190
        dr.rounded_rectangle(
            (pad, y, w - pad, y + card_h), radius=28, fill=SURFACE, outline=HAIRLINE, width=2
        )

        # Position in her list. A place in an order, never a score out of anything.
        dr.text((pad + 28, y + 24), str(i), font=face(30, "ExtraBold"), fill=PINK)

        cx, cy, r = pad + 96, y + card_h // 2, 44
        dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 214, 210))
        ini = face(40, "ExtraBold")
        bb = dr.textbbox((0, 0), initial, font=ini)
        dr.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), initial, font=ini, fill=INK)

        dr.text((cx + r + 28, y + 48), name, font=face(40, "Bold"), fill=INK)
        dr.text((cx + r + 28, y + 102), meta, font=face(29, "Medium"), fill=(126, 110, 122))
        y += card_h + 26

    # No fourth card, and no list running off the bottom edge. The product claim is
    # that the list is SHORT — a list bleeding past the fold would say the opposite
    # of the page it sits on. The space below closes the thought instead.
    y += 34
    end = face(30, "Bold")
    bb = dr.textbbox((0, 0), "That is today's list.", font=end)
    dr.text(((w - (bb[2] - bb[0])) / 2, y), "That is today's list.", font=end, fill=INK)
    sub = face(25, "Medium")
    bb = dr.textbbox((0, 0), "More only when they fit.", font=sub)
    dr.text(((w - (bb[2] - bb[0])) / 2, y + 46), "More only when they fit.", font=sub, fill=(150, 134, 146))
    return im


# ── perspective composite ────────────────────────────────────────────────────


def solve8(a, b):
    """Gaussian elimination with partial pivoting. numpy is not a dependency here."""
    n = 8
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[p] = m[p], m[col]
        pv = m[col][col]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col] / pv
            for k in range(col, n + 1):
                m[r][k] -= f * m[col][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def perspective_coeffs(dst_quad, src_size):
    """Coefficients for Image.PERSPECTIVE, which maps OUTPUT coords back to INPUT.

    dst_quad is TL,TR,BR,BL in the plate's coordinates; the source is the whole
    render, so its corners are the trivial rectangle.
    """
    w, h = src_size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    a, b = [], []
    for (X, Y), (x, y) in zip(dst_quad, src):
        a.append([X, Y, 1, 0, 0, 0, -X * x, -Y * x])
        b.append(x)
        a.append([0, 0, 0, X, Y, 1, -X * y, -Y * y])
        b.append(y)
    return solve8(a, b)


def find_screen_quad(im):
    """The blank screen, by threshold. Pure white is the screen and only the screen."""
    px = im.load()
    pts = [
        (x, y)
        for y in range(im.height)
        for x in range(im.width)
        if px[x, y][0] >= 250 and px[x, y][1] >= 250 and px[x, y][2] >= 250
    ]
    if not pts:
        raise SystemExit("no blank screen found in the plate — has it been re-cut?")
    return (
        min(pts, key=lambda p: p[0] + p[1]),  # TL
        max(pts, key=lambda p: p[0] - p[1]),  # TR
        max(pts, key=lambda p: p[0] + p[1]),  # BR
        min(pts, key=lambda p: p[0] - p[1]),  # BL
    )


def grow(quad, px_out):
    """Push each corner away from the quad's centroid by roughly px_out pixels."""
    cx = sum(p[0] for p in quad) / 4
    cy = sum(p[1] for p in quad) / 4
    out = []
    for x, y in quad:
        dx, dy = x - cx, y - cy
        d = (dx * dx + dy * dy) ** 0.5 or 1
        out.append((x + dx / d * px_out, y + dy / d * px_out))
    return out


def composite_screen(plate, ui):
    quad = find_screen_quad(plate)

    # Grow the quad slightly and warp to THAT. Two problems are solved at once: the
    # quad is four straight lines through the extreme points, so it cuts the corners
    # off a screen with rounded ends and leaves slivers of the original white
    # showing; and warping to the exact quad means any mask pixel outside it samples
    # past the edge of the source and lands black. Growing the target fixes the
    # slivers and keeps every masked pixel inside the source. The UI scales up by
    # about two percent, which the render's own margins absorb.
    big = grow(quad, 5)
    warped = ui.transform(
        plate.size, Image.PERSPECTIVE, perspective_coeffs(big, ui.size), Image.BICUBIC
    )

    # The mask is the measured white region INTERSECTED with that grown quad. The
    # threshold alone is not enough: at 245 it also catches the brightest folds of
    # the bedsheet, and painting the warp onto pixels that far from the screen is
    # what put a black smudge on the bed. The threshold keeps the warp off the black
    # bezel; the polygon keeps it on the phone.
    px = plate.load()
    mask = Image.new("L", plate.size, 0)
    mpx = mask.load()
    for y in range(plate.height):
        for x in range(plate.width):
            r, g, b = px[x, y]
            if r >= 245 and g >= 245 and b >= 245:
                mpx[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(3))

    region = Image.new("L", plate.size, 0)
    ImageDraw.Draw(region).polygon([(round(x), round(y)) for x, y in big], fill=255)
    mask = ImageChops.multiply(mask, region)

    out = plate.copy()
    out.paste(warped, (0, 0), mask)
    return out, quad


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Hero — 3:4 above the watermark line, framed on her face with headroom.
    c5 = Image.open(SRC / "moveon-properly-w2530/clean-c5.jpg").convert("RGB")
    crop_ratio(c5, 150, 1440).save(OUT / "hero.jpg", **JPEG)

    # Phone-down — 4:5, wall for breathing room above the table.
    a = Image.open(SRC / "fourteen-suitors-w1822/clean-a.jpg").convert("RGB")
    crop_ratio(a, 520, 1350).save(OUT / "phone-down.jpg", **JPEG)

    # Shortlist — interface warped into the blank screen, then cropped to 4:5.
    b = Image.open(SRC / "fourteen-suitors-w1822/clean-b.jpg").convert("RGB")
    composed, quad = composite_screen(b, shortlist_render())
    crop_ratio(composed, 300, 1350).save(OUT / "shortlist.jpg", **JPEG)

    for p in ("hero.jpg", "phone-down.jpg", "shortlist.jpg"):
        f = OUT / p
        print(f"{p:16} {Image.open(f).size[0]}x{Image.open(f).size[1]}  {f.stat().st_size // 1024} KB")
    print("screen quad:", quad)


if __name__ == "__main__":
    main()
