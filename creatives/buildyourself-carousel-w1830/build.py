"""Type layer for the BUILD-YOURSELF-FIRST carousel — 13 stills re-cutting the
shipped video (creatives/buildyourself-lead-w1830/asset-a.mp4) into a Snap photo
sequence, per Sree's 2026-08-30 direction. Shipped as 13 separate single-image
LEAD_GENERATION ads under the standing squad, not one Story-Ad sequence.

    uv run python creatives/buildyourself-carousel-w1830/build.py

No new Grok generation — per rules/creative-generation.md §2 the plate carries
no words and here the plates themselves are re-cut from assets this account
already generated and QA'd once (buildyourself-lead-w1830/_source/frames/, plus
one frame pulled from a Grok clip — see sourcing.md for the exact source of
every slide). All type is set fresh in real Gabarito.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"
D = Path(__file__).parent
FR = D.parent / "buildyourself-lead-w1830/_source/frames"
EX = D / "_derived"

INK = "#1B1020"
PINK = "#FF3B6B"
WHITE = "#FFFFFF"
SIZE = (1080, 1920)
MARGIN = 84
SAFE_TOP, SAFE_BOTTOM = 192, 1632


def face(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def fit_lines(dr, text, size, weight, max_w):
    while size > 24:
        f = face(size, weight)
        if dr.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return face(size, weight), size


def prep_plate(src_name):
    """Flow still -> exact 1080x1920, 9:16, centre-cropped."""
    im = Image.open(FR / src_name).convert("RGB")
    W, H = im.size
    tgt = W * 16 / 9
    if H > tgt:
        off = int((H - tgt) / 2)
        im = im.crop((0, off, W, off + int(tgt)))
    else:
        tgtw = int(H * 9 / 16)
        off = (W - tgtw) // 2
        im = im.crop((off, 0, off + tgtw, H))
    return im.resize(SIZE, Image.LANCZOS)


def prep_extracted(src_name):
    """Already 1080x1920 (cropped/scaled at extraction time from a Grok clip
    frame, watermark cropped per creative-generation.md §7) -- use as-is."""
    return Image.open(EX / src_name).convert("RGB")


def prep_grid(src_name):
    """For a full-width source (the 4-panel collage, or a plain landscape
    group shot): fit full width, letterbox top/bottom in ink."""
    im = Image.open(FR / src_name).convert("RGB")
    W, H = im.size
    neww = SIZE[0]
    newh = int(H * neww / W)
    im = im.resize((neww, newh), Image.LANCZOS)
    canvas = Image.new("RGB", SIZE, INK)
    y = (SIZE[1] - newh) // 2
    canvas.paste(im, (0, y))
    return canvas


def footer_gradient(im, top_y, strength=0.82):
    W, H = im.size
    grad = Image.new("L", (1, H), 0)
    for y in range(top_y, H):
        a = int(255 * strength * (y - top_y) / (H - top_y))
        grad.putpixel((0, y), min(a, 255))
    alpha = grad.resize((W, H))
    band = Image.new("RGB", (W, H), (10, 6, 12))
    im.paste(band, (0, 0), alpha)


def two_tone(dr, lines, top, size, weight="ExtraBold", leading=1.14):
    y = top
    for segs in lines:
        x = MARGIN
        f = face(size, weight)
        for text, colour in segs:
            dr.text((x, y), text, font=f, fill=colour)
            x += dr.textlength(text, font=f)
        y += int(size * leading)
    return y


def build(subdir, src, lines, footer_top=1300, is_grid=False, size=78, extracted=False):
    """Each ad is its own creative_ref (rules/naming.md's [VARIANT] token as a
    folder), because ad-agent snap-push resolves exactly `<creative_ref>/
    asset-a.jpg` -- one image per creative folder, no per-ad filename param.
    13 ads sharing one folder was tried first and doesn't fit that contract."""
    (D / subdir).mkdir(exist_ok=True)
    im = prep_grid(src) if is_grid else (prep_extracted(src) if extracted else prep_plate(src))
    footer_gradient(im, footer_top)
    two_tone(ImageDraw.Draw(im), lines, 1420, size)
    im.save(D / subdir / "asset-a.jpg", quality=94, subsampling=0)
    print(f"{subdir}/asset-a.jpg <- {src}")


def build_endcard(subdir, src):
    im = prep_grid(src)
    footer_gradient(im, 900, strength=0.94)
    dark = Image.new("RGB", SIZE, INK)
    im = Image.blend(im, dark, 0.35)
    dr = ImageDraw.Draw(im)
    max_w = SIZE[0] - 2 * MARGIN
    f1, s1 = fit_lines(dr, "riteangle", 130, "ExtraBold", max_w)
    dr.text((MARGIN, 1280), "riteangle", font=f1, fill=PINK)
    ft, st = fit_lines(dr, "Men, dating, relationships...", 52, "Medium", max_w)
    dr.text((MARGIN, 1280 + int(s1 * 1.2)), "Men, dating, relationships...", font=ft, fill=WHITE)
    dr.text((MARGIN, 1280 + int(s1 * 1.2) + int(st * 1.25)), "jab tum taiyaar ho.", font=ft, fill=WHITE)
    fc, _ = fit_lines(dr, "Apply now →", 44, "Bold", max_w)
    dr.text((MARGIN, 1650), "Apply now →", font=fc, fill=PINK)
    (D / subdir).mkdir(exist_ok=True)
    im.save(D / subdir / "asset-a.jpg", quality=94, subsampling=0)
    print(f"{subdir}/asset-a.jpg <- endcard")


build("a-ghosted", "Woman_sitting_on_bedroom_floor_202608292351.jpeg",
    [[("Phir se ", WHITE), ("ghost", PINK), (" kar diya?", WHITE)]])

build("b-catfish", "Woman_reading_laptop_at_cafe_202608292356.jpeg",
    [[("Profile kuch aur, ", WHITE)], [("aadmi ", PINK), ("kuch aur.", WHITE)]], footer_top=1250, size=68)

build("c-alone", "Woman_sitting_alone_at_table_202608292351.jpeg",
    [[("Kab ", WHITE), ("tak?", PINK)]])

build("d-enough", "Tired_woman_looking_at_phone_202608292351.jpeg",
    [[("Bas. ", WHITE), ("Ab nahin.", PINK)]])

build("e-turn", "Four_women_looking_into_camera_202608300008.jpeg",
    [[("Khud ko ", WHITE), ("bana sakti ho.", PINK)]], footer_top=1420, is_grid=True, size=68)

build("f-strength", "Woman_completing_heavy_barbell_d…_202608300000.jpeg",
    [[("Pehle apni ", WHITE), ("taakat.", PINK)]])

build("g-win", "tennis-jump-serve-contact.jpg",
    [[("Pehle apni ", WHITE), ("jeet.", PINK)]], extracted=True)

build("h-calm", "Woman_meditating_on_balcony_at_202608300006.jpeg",
    [[("Pehle apna ", WHITE), ("sukoon.", PINK)]])

build("i-world", "Woman_breathing_at_coastal_overlook_202608300006.jpeg",
    [[("Pehle apni ", WHITE), ("duniya.", PINK)]])

build("j-joy", "Woman_laughing_on_rooftop_terrace_202608300005.jpeg",
    [[("Pehle apni ", WHITE), ("khushi.", PINK)]])

build("k-career", "Woman_smiling_in_modern_office_202608300005.jpeg",
    [[("Pehle apna ", WHITE), ("career.", PINK)]])

build("l-close", "Four_women_standing_in_space_202608300005.jpeg",
    [[("Pehle tum.", WHITE)], [("Phir koi aur.", PINK)]], footer_top=1420, is_grid=True, size=68)

build_endcard("m-endcard", "Four_women_standing_in_space_202608300005.jpeg")
