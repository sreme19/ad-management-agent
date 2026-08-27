"""Web-ready imagery for /get/w, cut from the current winning plates.

    uv run python creatives/_web/prep-get-w-images.py

Writes into pocket-dating-coach/static/get-w/. That repo holds the page; this one
holds the plates and the rules they were made under, so the derivation lives here
and only the output crosses over. Re-run to re-cut.

ROUND 2 (2026-08-27, Sree: "the images are not the best", Bumble as reference).
The round-1 cuts read static: every frame in the Bumble reference set catches
someone mid-motion or mid-laugh, and ours held still. Three new Gemini plates from
`_bakeoff/round-02-getw-bumble/candidates/` replace them:

  hero.jpg      <- gemini-hero-1.png   she laughs, head tipped, eyes creased
  moment.jpg    <- gemini-moment-1.png mid-step on a Bangalore street, glancing
                   back laughing (replaces phone-down.jpg on the page)
  shortlist.jpg <- gemini-phones-1.png three overlapping phones on cream, the
                   shortlist UI composited into the CENTRE one

WATERMARK HANDLING, per plate. Gemini stamps a translucent star bottom-right.
  hero:   star at (775-815, 1055-1100) -> bottom crop at y=1050 drops it; the cut
          lands mid-forearm, which is an ordinary editorial crop.
  moment: star at (790-830, 1030-1075) -> right crop at x=760 drops it, and the
          same cut removes the garbled background signage and the two distant
          background figures. One crop, three QA notes closed.
  phones: star at (785-850, 990-1060) on FLAT cream -> covered with a solid patch
          sampled from the surrounding background. Same operation as the ad's
          cream scrim (a solid over the mark, no generated detail), just local.

The round-1 derivation below is kept callable for provenance — the shipped
2026-08-27 morning images came from it.

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


def is_screen_white(rgb):
    """Bright AND neutral. The round-2 plate's screens render at ~(239,239,239),
    below the 250 threshold the round-1 plate satisfied — but they are perfectly
    neutral (max-min spread 0) where the cream ground is warm (spread 23+), so
    chroma separates them cleanly where brightness alone no longer does."""
    r, g, b = rgb
    # 215/12 rather than 225/8: the screen's edge pixels pick up a slight warm
    # reflection near the bezel and were failing the tighter test, which left a
    # sliver of original white outside the composite along the lower-right edge.
    # The ground sits at spread 23+, so 12 still separates cleanly.
    return min(r, g, b) >= 215 and max(r, g, b) - min(r, g, b) <= 12


def flood_white(im, seed):
    """Every screen-white pixel 4-connected to `seed`.

    A rectangular window is not enough on the round-2 phones plate: the three
    screens are all pure white and the tilted side screens poke into any box drawn
    around the centre one — the first cut of this warped the UI against a quad
    whose top-left corner belonged to the LEFT phone, and nothing visible landed.
    Connectivity is the property that actually distinguishes the centre screen,
    because the black bezels separate the white regions completely.
    """
    px = im.load()
    W, H = im.size
    seen = set()
    stack = [seed]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < W and 0 <= y < H):
            continue
        if not is_screen_white(px[x, y]):
            continue
        seen.add((x, y))
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    if not seen:
        raise SystemExit(f"no white region at seed {seed} — has the plate changed?")
    return seen


def find_screen_quad(im, seed=None):
    """The blank screen, by threshold. Pure white is the screen and only the screen.

    With `seed`, only the white region connected to that point counts — see
    flood_white. Without it, every pure-white pixel in the frame does (the round-1
    plate had exactly one white region, so that was enough there).
    """
    if seed is not None:
        pts = list(flood_white(im, seed))
    else:
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


def composite_screen(plate, ui, seed=None):
    if seed is not None:
        # Warp to the flood region's axis-aligned BOUNDING BOX, not the
        # extreme-corner quad. The screen has rounded corners, so its straight
        # quad bottom runs ABOVE the bottom bulge of the white region — mask
        # pixels below that line sampled outside the UI source and came back
        # black, which printed a row of dark dashes along the screen foot. The
        # bbox covers every flooded pixel by construction; the centre phone is
        # near enough axis-aligned that losing the ~5px tilt is invisible.
        screen = flood_white(plate, seed)
        xs = [pt[0] for pt in screen]
        ys = [pt[1] for pt in screen]
        quad = ((min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys)))
    else:
        quad = find_screen_quad(plate)
        screen = None

    # Grow the quad slightly and warp to THAT. Two problems are solved at once: the
    # quad is four straight lines through the extreme points, so it cuts the corners
    # off a screen with rounded ends and leaves slivers of the original white
    # showing; and warping to the exact quad means any mask pixel outside it samples
    # past the edge of the source and lands black. Growing the target fixes the
    # slivers and keeps every masked pixel inside the source. The UI scales up by
    # about two percent, which the render's own margins absorb.
    big = grow(quad, 9)
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
    if screen is not None:
        # Exactly the connected screen region, nothing else.
        for x, y in screen:
            mpx[x, y] = 255
    else:
        for y in range(plate.height):
            for x in range(plate.width):
                r, g, b = px[x, y]
                if r >= 245 and g >= 245 and b >= 245:
                    mpx[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5))

    region = Image.new("L", plate.size, 0)
    ImageDraw.Draw(region).polygon([(round(x), round(y)) for x, y in big], fill=255)
    mask = ImageChops.multiply(mask, region)

    out = plate.copy()
    out.paste(warped, (0, 0), mask)
    return out, quad


def cover_solid(im, box):
    """Patch over a mark on a near-uniform ground.

    The fill is the average of the pixels in a ring just outside the box — a
    single sampled pixel left a visible rectangle, because the cream ground
    carries a soft gradient and no one pixel matches the whole neighbourhood.
    Averaged, the patch sits inside JPEG noise.
    """
    l, t, r, b = box
    px = im.load()
    ring = []
    for x in range(max(0, l - 8), min(im.width, r + 8)):
        for y in (max(0, t - 8), min(im.height - 1, b + 7)):
            ring.append(px[x, y])
    for y in range(max(0, t - 8), min(im.height, b + 8)):
        for x in (max(0, l - 8), min(im.width - 1, r + 7)):
            ring.append(px[x, y])
    # Only warm ground pixels vote: the ring can graze a phone bezel or screen,
    # and averaging those in produced a visibly grey patch on the cream.
    warm = [c for c in ring if max(c) - min(c) >= 15 and min(c) >= 150]
    ring = warm or ring
    n = len(ring)
    fill = tuple(sum(c[i] for c in ring) // n for i in range(3))
    ImageDraw.Draw(im).rectangle(box, fill=fill)
    return im


R2 = SRC / "_bakeoff/round-02-getw-bumble/candidates"


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Hero — bottom crop at 1050 drops the watermark; cut lands mid-forearm.
    hero = Image.open(R2 / "gemini-hero-1.png").convert("RGB")
    hero.crop((0, 0, 896, 1050)).save(OUT / "hero.jpg", **JPEG)

    # Moment — right crop at 760 drops watermark, garbled signage and the two
    # distant background figures in one cut.
    moment = Image.open(R2 / "gemini-moment-1.png").convert("RGB")
    moment.crop((0, 0, 760, 1152)).save(OUT / "moment.jpg", **JPEG)

    # Shortlist — composite the UI into the CENTRE phone (the flood seed keeps
    # the side screens out), then crop the bottom at 970: the watermark star sits
    # at y990-1060, so the crop removes it outright and no cover patch is needed.
    # The right phone bleeding off the cut edge matches the reference frames.
    phones = Image.open(R2 / "gemini-phones-1.png").convert("RGB")
    composed, quad = composite_screen(phones, shortlist_render(), seed=(460, 580))
    composed.crop((0, 0, 928, 970)).save(OUT / "shortlist.jpg", **JPEG)

    for name in ("hero.jpg", "moment.jpg", "shortlist.jpg"):
        f = OUT / name
        im = Image.open(f)
        print(f"{name:14} {im.size[0]}x{im.size[1]}  {f.stat().st_size // 1024} KB")
    print("centre-screen quad:", quad)


def main_r1():
    """Round-1 derivation, kept for provenance. Produced the 2026-08-27 morning set."""
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


if __name__ == "__main__":
    main()
