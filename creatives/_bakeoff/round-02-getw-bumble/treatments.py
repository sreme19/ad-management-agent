"""Round-02 treatment candidates — the palette question, on pixels.

    uv run python creatives/_bakeoff/round-02-getw-bumble/treatments.py

NOT GENERATED CANDIDATES. These are grades and crops of the round-1 hero plate,
run because generation was blocked this session (no reachable browser) and the
Bumble-versus-cream question can be answered without new pixels. A grade cannot
fix the actual round-1 weakness — she is holding still, and every Bumble frame has
someone caught mid-motion — so whatever wins here still wants a real generation
round behind it.

  t1-bw      Bumble's B1 treatment: black-and-white, editorial contrast. Their
             "Love Stories" post is a monochrome photograph carrying yellow display
             type, and it is the most distinctive thing in the observed set.
  t2-cream   The riteangle-native answer: keep the cream ground, buy the editorial
             quality with contrast and a tighter crop instead of with desaturation.

Both are cropped tighter than the shipped hero (y 300 rather than 150). Bumble
crops close; the shipped version has a lot of room above her head, which is part of
why it reads like a webcam still rather than a photograph someone chose.

Yellow appears in NEITHER file, deliberately. On the page the accent belongs in CSS,
not burned into a photograph — and #FFC629 is a direct competitor's brand colour,
which is a decision for the page, not something to bake irreversibly into an asset.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

SRC = Path("/Users/performek5/Desktop/Code/ad-management-agent/creatives")
OUT = Path(__file__).parent / "candidates"

# y=1650 is the floor: Gemini's watermark sits below y=1700 on this plate and the
# ad covered it with a scrim from there. Everything here crops above it.
CROP_TOP, CROP_H = 300, 1350

JPEG = dict(quality=86, optimize=True, progressive=True)


def plate():
    im = Image.open(SRC / "moveon-properly-w2530/clean-c5.jpg").convert("RGB")
    return im.crop((0, CROP_TOP, im.width, CROP_TOP + CROP_H))


def t1_bw(im):
    """Editorial monochrome. Autocontrast first so the curve has the full range to
    work with, then push contrast — a flat greyscale conversion reads as a
    desaturated colour photo, which is the cheap version of this look."""
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=(0.5, 0.5))
    g = ImageEnhance.Contrast(g).enhance(1.18)
    return g.convert("RGB")


def t2_cream(im):
    """Same photograph, kept warm. Contrast and a touch of saturation do the work
    the desaturation does in t1, so the cream ground survives."""
    out = ImageEnhance.Contrast(im).enhance(1.12)
    out = ImageEnhance.Color(out).enhance(1.06)
    return ImageEnhance.Brightness(out).enhance(1.02)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = plate()
    for name, fn in (("t1-bw", t1_bw), ("t2-cream", t2_cream)):
        dest = OUT / f"{name}.jpg"
        fn(base).save(dest, **JPEG)
        print(f"{name:10} {Image.open(dest).size[0]}x{Image.open(dest).size[1]}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
