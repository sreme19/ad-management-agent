"""The network registry: rules/networks.yaml, loaded and enforced.

A network was a two-value enum hardcoded in four argparse calls, plus a
`utm_source: "snapchat"` string literal inside a Snap-only function. That works
for exactly two networks and stops working the moment a third is discussed,
because a network is four things at once — a UTM convention, a join key, an
analytics label, and a statement about whether this agent may create anything on
it — and two of those already differ between Snap and Meta in ways that have
caused real bugs.

**`creation` can only ever refuse.** `require_creation` is called *in addition
to* a command's own hardcoded network check, never instead of it, so editing the
yaml cannot grant a capability. Flipping meta to `paused-only` there would grant
nothing: there is no Meta client and no Meta credential (SPEC.md decision #10),
and snap.py's transport-layer refusal is what actually holds the paused-only
line. The registry states intent and tightens; the code holds.
"""
from __future__ import annotations

from pathlib import Path

import yaml

CREATION_MODES = ("none", "paused-only")


class NetworkError(ValueError):
    """Raised for an unknown network, or one this agent may not create on."""


def _load(rules_dir: str) -> dict:
    """Read and validate the registry. Deliberately uncached.

    It is read a handful of times per invocation at most, and caching it keyed on
    a path makes a file edited mid-process invisible — which is a real hazard in
    tests, and would be one for any long-running caller later.
    """
    path = Path(rules_dir) / "networks.yaml"
    if not path.exists():
        raise NetworkError(
            f"network registry missing: {path}\n"
            "Every command that names a network reads it. Restore the file from git."
        )
    data = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("networks") or {}
    if not data:
        raise NetworkError(f"{path} defines no networks")
    for name, entry in data.items():
        mode = entry.get("creation")
        if mode not in CREATION_MODES:
            raise NetworkError(
                f"{path}: network {name!r} has creation={mode!r}; "
                f"expected one of {', '.join(CREATION_MODES)}"
            )
        for field in ("utm_source", "ad_join_param", "ad_set_join_param"):
            if not entry.get(field):
                raise NetworkError(f"{path}: network {name!r} is missing {field}")
    return data


def all_networks(rules_dir: Path) -> dict:
    return _load(str(rules_dir))


def names(rules_dir: Path) -> list[str]:
    """Every registered network, for argparse choices."""
    return list(_load(str(rules_dir)))


def get(rules_dir: Path, network: str) -> dict:
    entry = _load(str(rules_dir)).get(network)
    if entry is None:
        raise NetworkError(
            f"unknown network {network!r}. Registered: {', '.join(names(rules_dir))}.\n"
            "Adding one is an entry in rules/networks.yaml plus a client module — read the "
            "budget warning at the top of that file first."
        )
    return entry


def require_creation(rules_dir: Path, network: str, *, mode: str = "paused-only") -> None:
    """Refuse if the registry does not permit creating on this network.

    Additive to the caller's own checks, never a substitute for them. See the
    module docstring for why that distinction is the whole safety argument.
    """
    entry = get(rules_dir, network)
    if entry.get("creation") != mode:
        raise NetworkError(
            f"rules/networks.yaml declares creation={entry.get('creation')!r} for "
            f"{network!r}; this command needs {mode!r}.\n"
            f"{str(entry.get('note') or '').strip()}"
        )


def utm_params(rules_dir: Path, network: str, *, campaign_name: str, ad_set_id: str,
               ad_id: str, ad_name: str) -> dict:
    """rules/tracking.md's five parameters, with this network's own conventions.

    What differs between the networks is which parameter the analytics joins the
    *ad* on: utm_id on Snap, utm_content on Meta, per traffic-quality.ts. So the
    ad id is written into this network's own `ad_join_param` **last**, after the
    human-readable ad name goes into utm_content — on Snap those are two different
    parameters and both survive, and on Meta they are the same one, where the id
    has to win because it is what the join reads.

    tracking.md's single URL template shows `utm_content={{ad.name}}` while its
    prose says utm_content is Meta's ad-level id. Both cannot hold on Meta. This
    follows the prose, since that is the half naming the code that reads it — and
    the contradiction is logged as q-2026-08-26-utm-content-on-meta rather than
    quietly resolved here.
    """
    entry = get(rules_dir, network)
    params = {
        "utm_source": entry["utm_source"],
        "utm_medium": "paid_social",
        "utm_campaign": campaign_name,
        entry["ad_set_join_param"]: ad_set_id,
        "utm_content": ad_name,
    }
    params[entry["ad_join_param"]] = ad_id
    return params
