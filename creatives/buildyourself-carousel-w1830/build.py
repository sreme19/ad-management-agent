"""Type layer for the BUILD-YOURSELF-FIRST carousel — 13 stills re-cutting the
shipped video (creatives/buildyourself-lead-w1830/asset-a.mp4) into a Snap photo
sequence, per Sree's 2026-08-30 direction.

    uv run python creatives/buildyourself-carousel-w1830/build.py

No new Grok generation — per rules/creative-generation.md §2 the plate carries
no words and here the plates themselves are re-cut from assets this account
already generated and QA'd once (buildyourself-lead-w1830/_source/frames/, plus
one frame pulled from a Grok clip — see sourcing.md for the exact source of
every slide). All type is set fresh in real Gabarito.

Shipped as one Snap Story Ad (a tap-through COMPOSITE sequence, `snap-push-story`)
— NOT as 13 separate single-image ads, which is how this was first (wrongly)
built and pushed, then rolled back once Sree named the actual format he'd asked
for. Also writes `preview.png`: Snap's PREVIEW-tile media rejects JPEG outright
("Allowed extensions: png", discovered live on the first `snap-push-story` run,
not in advance from the docs), so the Story tile needs its own PNG export
alongside the 13 JPEG snaps.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Shared, single-source-of-truth watermark crop + advisory scan — so this build and
# the push gate agree on how a Google/Flow "made with AI" sparkle is removed.
from ad_management_agent.watermark import strip_flow_watermark, FLOW_WATERMARK_BOTTOM_CROP, scan

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

# Every Flow (Google) still carries the "made with Google AI" sparkle stamped at a
# fixed offset from the bottom-right corner -- ~98px up, ~96px in, the star spanning
# up to ~137px above the bottom edge. Sree's call 2026-08-30: CROP it out, don't
# inpaint -- remove real pixels rather than reconstruct them. strip_flow_watermark
# (150px off the bottom) clears the whole star in both 768x1376 and 1376x768 exports,
# while leaving the subject horizontally centred (no left/right crop). The crop amount
# lives in ad_management_agent.watermark so the build and the push gate can't drift.
def load_frame(name):
    """Open a Flow source frame with the bottom watermark band already cropped off."""
    return strip_flow_watermark(Image.open(FR / name).convert("RGB"))


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
    """Flow still -> exact 1080x1920, 9:16, centre-cropped (watermark band cropped)."""
    im = load_frame(src_name)
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
    group shot): fit full width, letterbox top/bottom in ink (watermark band cropped)."""
    im = load_frame(src_name)
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

# The Story tile shown before it's tapped open -- same frame as the first snap
# (a-ghosted), re-exported as PNG at Snap's required 3:5 tile ratio (not 9:16 --
# also discovered live, on the second snap-push-story attempt, after PNG-vs-JPEG
# was fixed on the first). 1080x1920 at 9:16 -> 1080x1800 at 3:5 needs 120px
# trimmed off the height; taken mostly off the bottom (20 top / 100 bottom) so
# her face stays centred and the headline -- which sits at y1420+ -- keeps a
# wide margin above the new bottom edge at y1820.
_prev = Image.open(D / "a-ghosted" / "asset-a.jpg").convert("RGB").crop((0, 20, 1080, 1820))
assert _prev.size == (1080, 1800), _prev.size  # 3:5 exactly, no resize needed
_prev.save(D / "preview.png")
print(f"preview.png <- a-ghosted/asset-a.jpg, cropped to {_prev.size} (3:5, Snap's tile ratio)")

# Advisory watermark scan -- points the eye at the strongest bright corner spot on
# each built plate so a reviewer knows where to zoom. NOT a pass/fail (see
# watermark.py): every Flow source went through strip_flow_watermark above, and the
# real gate is the recorded `watermark-check: pass` in qa.md that the push enforces.
print("\nCorner watermark advisory (crop already applied; look where peak is high):")
for beat in ["a-ghosted", "b-catfish", "c-alone", "d-enough", "e-turn", "f-strength",
             "g-win", "h-calm", "i-world", "j-joy", "k-career", "l-close", "m-endcard"]:
    print(f"  {scan(D / beat / 'asset-a.jpg')}")
