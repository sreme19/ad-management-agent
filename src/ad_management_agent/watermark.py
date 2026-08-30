"""Guardrail against pushing a creative with an AI-generation watermark baked in.

Why this exists
---------------
On 2026-08-30 a Snap Story Ad shipped with Google's "made with AI" sparkle — the
four-point star Flow (Google) stamps into the bottom-right corner of every still it
exports — baked into several plates. It reached a live, Approved ad before Sree
caught it by eye. This module is the guardrail so it cannot happen silently again.

The design decision, stated plainly
-----------------------------------
Pixel-detecting this mark reliably is not feasible with simple means, and a flaky
detector is worse than none — it was measured on the 2026-08-30 before/after set and
it both MISSED most watermarked frames (the sparkle is semi-transparent, so its
brightness swings with the background) and FALSE-POSITIVED on the ad's own white
caption type and on skin highlights. A hard gate built on it would block clean
pushes and hand out false confidence.

So the guarantee is *structural*, not detective, in two layers:

  1. `strip_flow_watermark()` — the mandatory crop. Every Google/Flow/Gemini-exported
     still MUST be run through this before it is used in a creative. The sparkle sits
     at a fixed offset from the bottom-right corner (~98px up), so cropping the bottom
     band removes it outright, on any export size, with no pixels reconstructed. This
     is what actually prevents the bug. `creatives/.../build.py` builds every plate
     through it.

  2. `require_clearance()` — the push refuses unless the creative's `qa.md` records an
     explicit, dated watermark clearance (`watermark-check: pass`). The corners were
     looked at, by a person or by the skill, and that was written down. This is wired
     into the same QA gate that already blocks a push with no recorded `pass`.

`scan()` remains, but only as a printed ADVISORY — it points the eye at the strongest
bright corner spot so a reviewer knows where to zoom. It never blocks a push. Treat a
low score as "nothing obvious here", never as "verified clean".

PIL-only on purpose: the core package depends only on pyyaml, and Pillow is already
present for the creative tooling.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Bottom band cropped off every Flow/Google source still. The sparkle centres ~98px
# above the bottom edge and spans up to ~137px; 150 clears it on both 9:16 and 16:9
# exports while touching neither side (subject stays horizontally centred).
FLOW_WATERMARK_BOTTOM_CROP = 150

# The qa.md token the push requires before it will build any creative object.
CLEARANCE_TOKEN = "watermark-check: pass"

CORNER_X, CORNER_Y = 0.78, 0.78  # advisory scan is limited to this corner band
WORK = 480                       # long edge the advisory scan runs at


class WatermarkNotCleared(RuntimeError):
    """A creative reached the push with no recorded watermark clearance in qa.md."""


def strip_flow_watermark(im, bottom: int = FLOW_WATERMARK_BOTTOM_CROP):
    """Return `im` with the bottom watermark band cropped off (a PIL Image in, out).

    The one place the crop amount is defined, so a build cannot use the wrong value
    or forget it. Call this on EVERY Google/Flow/Gemini-exported still before use.
    """
    w, h = im.size
    return im.crop((0, 0, w, max(1, h - bottom)))


def require_clearance(qa_path: str | Path) -> None:
    """Raise unless `qa_path` records an explicit watermark clearance.

    Checked by the push commands alongside the existing `pass` gate, so an ad cannot
    be created until the watermark check has actually been done and written down.
    """
    p = Path(qa_path)
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    if CLEARANCE_TOKEN not in text:
        raise WatermarkNotCleared(
            f"no watermark clearance in {p} — add a line '{CLEARANCE_TOKEN}' once every "
            "asset's corners have been checked for an AI-generation mark (the Flow/Gemini "
            "sparkle). Google/Flow stills must be cropped first (strip_flow_watermark / "
            "rules/creative-generation.md §7). Nothing was pushed."
        )


@dataclass
class Hit:
    path: str
    peak: int                 # local brightness contrast of the strongest corner spot
    pos: tuple[float, float]  # its (x, y) as fractions of the image size

    def __str__(self) -> str:
        return (f"{Path(self.path).name}: strongest bottom-right corner spot "
                f"peak={self.peak} at ({self.pos[0]:.2f},{self.pos[1]:.2f})")


def scan(path: str | Path) -> Hit:
    """ADVISORY only: report the strongest bright, desaturated spot in the corner band.

    A high value means "look here" — it does not mean a watermark, and a low value does
    not certify the asset clean. Never gate a push on this.
    """
    from PIL import Image, ImageFilter  # lazy: keeps the core import pyyaml-only

    im = Image.open(path).convert("RGB")
    W, H = im.size
    scale = WORK / max(W, H)
    small = im.resize((max(1, int(W * scale)), max(1, int(H * scale)))) if scale < 1 else im
    sw, sh = small.size
    gray = small.convert("L")
    local_mean = gray.filter(ImageFilter.BoxBlur(9))
    gpx, mpx, cpx = gray.load(), local_mean.load(), small.load()

    x0, y0 = int(sw * CORNER_X), int(sh * CORNER_Y)
    best, bx, by = 0, x0, y0
    for yy in range(y0, sh):
        for xx in range(x0, sw):
            contrast = gpx[xx, yy] - mpx[xx, yy]
            if contrast <= best:
                continue
            r, g, b = cpx[xx, yy][:3]
            if (max(r, g, b) - min(r, g, b)) < 55:  # desaturated / white-ish
                best, bx, by = contrast, xx, yy
    return Hit(path=str(path), peak=int(best), pos=(bx / sw, by / sh))


def advise(paths) -> list[Hit]:
    """Scan every asset and return the advisory hits (caller prints them)."""
    return [scan(p) for p in paths]
