"""Structured, machine-readable targeting on a ledger record.

`targeting_summary` is prose — it carries the *reasoning* for an audience, which
is what a human reads. It is not something a machine can push. Until this module
existed, `snap-push` compensated with a hardcoded dict for the one ad set it had
ever pushed, which meant a second recommendation would have been created with the
first one's audience *and diffed clean*, because the read-back was compared
against the same hardcoded dict rather than against the brief.

So a record now carries both: prose for the human, and a normalized `targeting`
block for the pusher. The prose may say anything; this block is validated.

Kept network-neutral on purpose, and that paid off on 2026-08-27: adding Meta was a
second translator (`to_meta`) plus a second read-back builder, not a second spec
format. The spec the ledger stores is unchanged, so one record can be pushed to
either network without being rewritten.
"""
from __future__ import annotations

from . import destinations

GENDERS = ("FEMALE", "MALE")
OS_TYPES = ("ANDROID", "IOS")

# Snap spells its device values this way; ours are uppercase for CLI symmetry.
_SNAP_OS = {"ANDROID": "ANDROID", "IOS": "iOS"}

# Meta disagrees with Snap on the type of nearly every field in this spec, which is
# the whole reason a translator exists per network rather than one shared payload:
#   gender   Snap "FEMALE"        Meta 2        (1 = male, 2 = female)
#   ages     Snap "18" / "50+"    Meta 18 / 65  (ints; 65 is Meta's open-ended top)
#   country  Snap "in"            Meta "IN"     (uppercase)
#   os       Snap "iOS"           Meta "iOS"    (agrees, by luck rather than design)
_META_GENDER = {"MALE": 1, "FEMALE": 2}
_META_OS = {"ANDROID": "Android", "IOS": "iOS"}

# Meta has no open-ended age band the way Snap's `50+` is. Its maximum is 65, which
# Meta itself renders as "65+", so an open-ended spec maps onto it.
META_MAX_AGE = 65

# compliance.md: "18+ without exception". Snap's own dating category enforces it
# on top of our rule, so a spec below 18 is refused here rather than rejected
# later by the platform.
MIN_LEGAL_AGE = 18


class TargetingError(ValueError):
    """Raised when a targeting spec is malformed, or contradicts its own record."""


def _age(value, field: str) -> str:
    """Ages are strings on Snap's API; `50+` is the open-ended top band."""
    s = str(value).strip()
    if s.endswith("+"):
        if field == "min_age":
            raise TargetingError("min_age cannot be open-ended; use a number")
        head = s[:-1]
    else:
        head = s
    if not head.isdigit():
        raise TargetingError(f"{field} must be a number (or `50+` for max_age), got {value!r}")
    return s


def build(
    *,
    gender: str,
    min_age,
    max_age,
    countries: list[str],
    os: str | None = None,
    expansion: bool = True,
    regulated_content: bool = True,
) -> dict:
    """Normalize CLI input into the block that goes on the record. Validates."""
    spec = {
        "gender": (gender or "").upper(),
        "min_age": _age(min_age, "min_age"),
        "max_age": _age(max_age, "max_age"),
        "countries": [c.strip().lower() for c in (countries or []) if c.strip()],
        "os": (os or "").upper() or None,
        "expansion": bool(expansion),
        # Dating is a regulated category on Snap. An ad squad without this flag is a
        # different, and rejectable, ad squad — so it defaults on rather than being
        # something a caller has to remember.
        "regulated_content": bool(regulated_content),
    }
    validate(spec)
    return spec


def validate(spec: dict) -> None:
    if not isinstance(spec, dict):
        raise TargetingError(f"targeting must be a mapping, got {type(spec).__name__}")

    gender = spec.get("gender")
    if gender not in GENDERS:
        raise TargetingError(
            f"gender must be one of {', '.join(GENDERS)}, got {gender!r}.\n"
            "rules/targeting.md forbids a mixed-gender ad set, so there is no 'ALL'."
        )

    lo_s, hi_s = _age(spec.get("min_age"), "min_age"), _age(spec.get("max_age"), "max_age")
    lo = int(lo_s)
    hi = int(hi_s.rstrip("+"))
    if lo < MIN_LEGAL_AGE:
        raise TargetingError(
            f"min_age is {lo}; rules/compliance.md is 18+ without exception.\n"
            "Snap's dating category enforces the same floor independently."
        )
    if hi < lo:
        raise TargetingError(f"max_age ({hi_s}) is below min_age ({lo_s})")

    countries = spec.get("countries")
    if not countries or not isinstance(countries, list):
        raise TargetingError("countries must be a non-empty list of 2-letter codes, e.g. [in]")
    bad = [c for c in countries if not (isinstance(c, str) and len(c) == 2 and c.isalpha())]
    if bad:
        raise TargetingError(f"not 2-letter country codes: {bad}")

    os_type = spec.get("os")
    if os_type is not None and os_type not in OS_TYPES:
        raise TargetingError(
            f"os must be one of {', '.join(OS_TYPES)} or omitted for all devices, got {os_type!r}"
        )


def check_matches_ad_set_name(spec: dict, ad_set_name: str) -> None:
    """Refuse a record that contradicts itself.

    The whole point of holding structured targeting is that the record cannot
    disagree with itself. `rules/naming.md` puts the gender in the ad-set name as
    a whole token, and the destination gate already reads it from there — so a
    spec saying FEMALE under a name saying MEN means one of the two is wrong, and
    which one it is cannot be guessed.
    """
    from_name = destinations.audience_of_ad_set_name(ad_set_name)
    if from_name is None:
        # Not this function's error to raise — the destination gate reports it
        # with the fuller explanation, and it runs on every path that calls here.
        return
    from_spec = "women" if spec.get("gender") == "FEMALE" else "men"
    if from_name != from_spec:
        raise TargetingError(
            f"ad set name {ad_set_name!r} reads as {from_name}, but targeting says "
            f"{spec.get('gender')} ({from_spec}).\n"
            "One of the two is wrong and it is not safe to guess which. Fix the name or "
            "the targeting so they agree."
        )


def to_snap(spec: dict) -> dict:
    """Translate the spec into a Snap ad-squad `targeting` payload."""
    validate(spec)
    payload: dict = {
        "regulated_content": bool(spec.get("regulated_content", True)),
        "demographics": [{
            "min_age": str(spec["min_age"]),
            "max_age": str(spec["max_age"]),
            "gender": spec["gender"],
            "operation": "INCLUDE",
        }],
        "geos": [{"country_code": c, "operation": "INCLUDE"} for c in spec["countries"]],
    }
    if spec.get("os"):
        payload["devices"] = [{"os_type": _SNAP_OS[spec["os"]], "operation": "INCLUDE"}]
    if spec.get("expansion", True):
        payload["enable_targeting_expansion"] = True
        payload["auto_expansion_options"] = {
            "interest_expansion_option": {"enabled": True},
            "custom_audience_expansion_option": {"enabled": True},
        }
    return payload


def describe(spec: dict) -> str:
    """One line for the plan print, so the operator sees the audience before creation."""
    bits = [
        {"FEMALE": "female", "MALE": "male"}.get(spec.get("gender"), str(spec.get("gender"))),
        f'{spec.get("min_age")}-{spec.get("max_age")}',
        ",".join(spec.get("countries") or []).upper(),
        spec["os"] if spec.get("os") else "all devices",
        "expansion on" if spec.get("expansion", True) else "expansion off",
    ]
    if spec.get("regulated_content", True):
        bits.append("regulated-content flagged")
    return ", ".join(bits)


def snap_readback_checks(spec: dict, squad_live: dict) -> list[tuple[str, object, object]]:
    """(label, got, want) rows comparing a live ad squad against this spec.

    Derived from the spec, never from a literal — that is the entire fix. A
    read-back diffed against a hardcoded dict validates the code against itself.
    """
    live = squad_live.get("targeting") or {}
    demo = (live.get("demographics") or [{}])[0]
    geos = live.get("geos") or []
    rows: list[tuple[str, object, object]] = [
        ("gender", demo.get("gender"), spec["gender"]),
        ("min age", str(demo.get("min_age")), str(spec["min_age"])),
        ("max age", str(demo.get("max_age")), str(spec["max_age"])),
        ("countries", ",".join(sorted(g.get("country_code", "") for g in geos)),
         ",".join(sorted(spec["countries"]))),
    ]
    if spec.get("os"):
        devices = live.get("devices") or [{}]
        rows.append(("os", devices[0].get("os_type"), _SNAP_OS[spec["os"]]))
    return rows


def _meta_age(value, field: str) -> int:
    """Meta's ages are ints, where Snap's are strings. `50+` maps onto Meta's 65 top."""
    s = _age(value, field)
    return META_MAX_AGE if s.endswith("+") else int(s)


def to_meta(spec: dict) -> dict:
    """Translate the spec into a Meta ad-set `targeting` payload.

    Two things here are not translations but decisions, and both are recorded rather
    than buried:

    `regulated_content` has no Meta equivalent. Snap has an explicit flag for
    regulated categories and dating is one; Meta handles dating as an account-level
    written permission instead, so there is no field to set. The spec's flag is
    therefore dropped here on purpose — not forgotten. If it were silently mapped to
    something plausible-looking, a reader would believe a declaration had been made
    that had not.

    `expansion` maps onto Advantage Audience, which is Meta's audience-broadening
    control and the closest analogue to Snap's targeting expansion. Note the polarity
    trap: Meta expresses it as `advantage_audience: 1` to expand and `0` to hold the
    audience as specified, so an omitted field is not a neutral default — recent Meta
    behaviour is to broaden unless told not to. It is written explicitly in both
    directions for that reason. This matters for the live women's records, whose whole
    premise is a specific age band: an ad set that quietly broadened would answer a
    different question than the one it was created to answer.
    """
    validate(spec)
    payload: dict = {
        "age_min": _meta_age(spec["min_age"], "min_age"),
        "age_max": _meta_age(spec["max_age"], "max_age"),
        "genders": [_META_GENDER[spec["gender"]]],
        "geo_locations": {
            "countries": [c.upper() for c in spec["countries"]],
            "location_types": ["home", "recent"],
        },
        "targeting_automation": {
            "advantage_audience": 1 if spec.get("expansion", True) else 0,
        },
    }
    if spec.get("os"):
        payload["user_os"] = [_META_OS[spec["os"]]]
    return payload


def meta_readback_checks(spec: dict, adset_live: dict) -> list[tuple[str, object, object]]:
    """(label, got, want) rows comparing a live Meta ad set against this spec.

    Derived from the spec, never from a literal — the same rule as
    `snap_readback_checks`, for the same reason: a read-back diffed against a
    hardcoded dict only ever validates the code against itself, which is how a wrong
    audience passes silently.

    Read-back matters more on Meta than on Snap, because Meta rewrites targeting it
    considers suboptimal rather than rejecting it. An ad set can be created with
    `advantage_audience: 0` and come back broadened, and the POST still returns 200.
    That is precisely the case a diff catches and a docstring does not.
    """
    live = adset_live.get("targeting") or {}
    geo = live.get("geo_locations") or {}
    rows: list[tuple[str, object, object]] = [
        ("gender", (live.get("genders") or [None])[0], _META_GENDER[spec["gender"]]),
        ("min age", live.get("age_min"), _meta_age(spec["min_age"], "min_age")),
        ("max age", live.get("age_max"), _meta_age(spec["max_age"], "max_age")),
        ("countries", ",".join(sorted(geo.get("countries") or [])),
         ",".join(sorted(c.upper() for c in spec["countries"]))),
        ("advantage audience",
         (live.get("targeting_automation") or {}).get("advantage_audience"),
         1 if spec.get("expansion", True) else 0),
    ]
    if spec.get("os"):
        rows.append(("os", ",".join(live.get("user_os") or []), _META_OS[spec["os"]]))
    return rows
