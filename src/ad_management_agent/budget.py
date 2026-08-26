"""Numbers lifted out of rules/budget.md so code can enforce them.

Every other file under `rules/` is prose read live by a skill. These three
figures are the ones code has to act on — a pre-launch refusal and a loose-end
report cannot parse a paragraph — so they are mirrored here, deliberately and
visibly. If rules/budget.md changes, change these in the same commit.

From rules/budget.md, "Operating envelope" and "Test -> measure -> kill/double":

  * Minimum viable daily spend: Rs 800-1,200 per active ad set. Below the floor
    the delivery algorithm rarely exits its learning phase, so anything under it
    is "a system check, not a real experiment."
  * Kill or double after 3-5 days, or 50-100 events, whichever comes first.
"""
from __future__ import annotations

MIN_VIABLE_DAILY_INR = 800.0
MAX_VIABLE_DAILY_INR = 1200.0

KILL_WINDOW_DAYS_MIN = 3
KILL_WINDOW_DAYS_MAX = 5


def below_floor(daily_inr: float | None) -> bool:
    return daily_inr is not None and float(daily_inr) < MIN_VIABLE_DAILY_INR


def floor_note(daily_inr: float) -> str:
    return (
        f"Rs {daily_inr:.0f}/day is below rules/budget.md's Rs "
        f"{MIN_VIABLE_DAILY_INR:.0f}-{MAX_VIABLE_DAILY_INR:.0f} minimum viable floor, so the "
        "delivery algorithm may never exit its learning phase and a weak read will be "
        "inconclusive rather than evidence."
    )
