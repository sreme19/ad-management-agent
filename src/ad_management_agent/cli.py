"""ad-agent CLI — the zero-API persistence layer for the ad-management-agent loop.

Every command here is either a deterministic file read/write or a single
plain HTTP call to pocket-dating-coach's authenticated internal analytics
endpoint. Nothing in this file calls the Anthropic API, or any LLM — the
reasoning happens live in the Claude Code session running the skill; this
CLI only persists or fetches data on that session's behalf.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
import urllib.error
import urllib.request
from pathlib import Path

from . import destinations, snap as snapapi
from .config import load_config
from .ledger import STATUSES, Ledger


def _today() -> str:
    return _dt.date.today().isoformat()


def cmd_propose(args: argparse.Namespace, ledger: Ledger) -> None:
    # Hard gate, before anything is written: an ad set may not point at a page
    # framed for a different audience. See rules/destinations.yaml — no override.
    try:
        destinations.check(
            ad_set_name=args.ad_set_name,
            destination_url=args.destination_url,
            rules_dir=ledger.root / "rules",
        )
    except destinations.DestinationGateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    rec = ledger.propose(
        slug=args.slug,
        network=args.network,
        campaign_name=args.campaign_name,
        ad_set_name=args.ad_set_name,
        ad_name=args.ad_name,
        targeting_summary=args.targeting_summary,
        creative_ref=args.creative_ref,
        destination_url=args.destination_url,
        budget_cap_inr_per_day=args.budget_cap,
        duration_days=args.duration_days,
        brief_path=args.brief,
        today=_today(),
    )
    ledger.write_index()
    print(f"proposed {rec.rec_id} -> {rec.path}")


def cmd_amend(args: argparse.Namespace, ledger: Ledger) -> None:
    fields = {
        "campaign_name": args.campaign_name,
        "ad_set_name": args.ad_set_name,
        "ad_name": args.ad_name,
        "targeting_summary": args.targeting_summary,
        "creative_ref": args.creative_ref,
        "destination_url": args.destination_url,
        "budget_cap_inr_per_day": args.budget_cap,
        "duration_days": args.duration_days,
    }
    changes = {k: v for k, v in fields.items() if v is not None}
    if not changes:
        print("error: nothing to amend — pass at least one field to change", file=sys.stderr)
        raise SystemExit(2)

    rec = ledger.find(args.rec_id)

    # Close the loophole: amend must not be a way around the destination gate.
    # Re-run it whenever this amendment touches the audience or the destination,
    # against the *resulting* pair rather than only the changed half. Amendments
    # that touch neither are left alone deliberately, so a record already blocked
    # by the gate can still have unrelated fields repaired.
    if "ad_set_name" in changes or "destination_url" in changes:
        effective_ad_set = changes.get("ad_set_name", rec.front_matter.get("ad_set_name", ""))
        effective_dest = changes.get("destination_url", rec.front_matter.get("destination_url", ""))
        try:
            destinations.check(
                ad_set_name=effective_ad_set,
                destination_url=effective_dest,
                rules_dir=ledger.root / "rules",
            )
        except destinations.DestinationGateError as exc:
            print(f"error: {exc}", file=sys.stderr)
            raise SystemExit(2) from exc

    try:
        rec, diff = ledger.amend(
            args.rec_id, changes=changes, reason=args.reason, today=_today()
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    if not diff:
        print(f"{rec.rec_id}: no change — every field already had that value")
        return
    ledger.write_index()
    print(f"amended {rec.rec_id} -> {rec.path}")
    for field, (old, new) in sorted(diff.items()):
        print(f"  {field}: {old!r} -> {new!r}")


# Mirrors the account's best-performing women's ad squad, `Female 18-22-LPV`
# (20.9% tap rate, n=110): broad, no interest narrowing, expansion on. That set
# was starved at ~Rs 50/day; this changes the budget and the name, not the
# audience, which is the whole point of the recommendation.
def _women_1822_targeting() -> dict:
    return {
        # Dating is a regulated category on Snap. The predecessor carries this and
        # an ad squad without it is a different, and rejectable, ad squad.
        "regulated_content": True,
        "demographics": [
            {"min_age": "18", "max_age": "22", "gender": "FEMALE", "operation": "INCLUDE"}
        ],
        "geos": [{"country_code": "in", "operation": "INCLUDE"}],
        "devices": [{"os_type": "ANDROID", "operation": "INCLUDE"}],
        "enable_targeting_expansion": True,
        "auto_expansion_options": {
            "interest_expansion_option": {"enabled": True},
            "custom_audience_expansion_option": {"enabled": True},
        },
    }


def _utm_url(destination: str, campaign_name: str, ad_squad_id: str,
             ad_id: str, ad_name: str) -> str:
    """rules/tracking.md's scheme, with every value literal.

    Ads Manager fills these from {{macros}}; the 2026-08-21 incident was a macro
    that silently never resolved. Pushed through the API the ids are known facts by
    the time the URL is written, so there is no macro left to fail.
    """
    from urllib.parse import urlencode
    return destination + "?" + urlencode({
        "utm_source": "snapchat",
        "utm_medium": "paid_social",
        "utm_campaign": campaign_name,
        "utm_term": ad_squad_id,
        "utm_id": ad_id,
        "utm_content": ad_name,
    })


def cmd_snap_push(args: argparse.Namespace, ledger: Ledger) -> None:
    config = load_config()
    rec = ledger.find(args.rec_id)
    fm = rec.front_matter

    if fm.get("network") != "snap":
        print(f"error: {args.rec_id} is network={fm.get('network')!r}, not snap", file=sys.stderr)
        raise SystemExit(2)
    if fm.get("status") != "proposed":
        print(f"error: {args.rec_id} is {fm.get('status')!r}; push expects 'proposed'.\n"
              "A record that is already live has real ids — pushing again would create "
              "duplicates.", file=sys.stderr)
        raise SystemExit(2)

    # The destination gate applies here too: this is the moment the ad set is
    # actually pointed at a page, so it is the last useful place to catch a mismatch.
    try:
        destinations.check(ad_set_name=fm["ad_set_name"],
                           destination_url=fm["destination_url"],
                           rules_dir=ledger.root / "rules")
    except destinations.DestinationGateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    asset = ledger.root / fm["creative_ref"] / "asset-a.jpg"
    qa = ledger.root / fm["creative_ref"] / "qa.md"
    if not asset.exists():
        print(f"error: creative not found at {asset}", file=sys.stderr)
        raise SystemExit(2)
    if not qa.exists() or "`pass`" not in qa.read_text(encoding="utf-8"):
        print(f"error: no recorded QA pass in {qa} — see rules/creative-generation.md sec 10",
              file=sys.stderr)
        raise SystemExit(2)

    start = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
    end = start + _dt.timedelta(days=int(fm["duration_days"]))
    iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%S.000Z")  # noqa: E731
    budget = float(fm["budget_cap_inr_per_day"])
    targeting = _women_1822_targeting()

    plan = [
        ("campaign   ", fm["campaign_name"]),
        ("ad squad   ", f'{fm["ad_set_name"]}  Rs {budget:.0f}/day x {fm["duration_days"]}d, '
                        f'LANDING_PAGE_VIEW, AUTO_BID'),
        ("ad         ", fm["ad_name"]),
        ("creative   ", f'{asset.name}  headline={args.headline!r}  CTA=MORE'),
        ("destination", fm["destination_url"]),
        ("targeting  ", "female 18-22, IN, Android, expansion on, no interest narrowing"),
    ]
    print(f"Plan for {args.rec_id} (everything created PAUSED):")
    for k, v in plan:
        print(f"  {k}  {v}")
    if args.dry_run:
        print("\n--dry-run: nothing created.")
        return

    client = snapapi.SnapClient(config.get("snap") or {})

    campaign = client.find_campaign(fm["campaign_name"])
    if campaign:
        print(f"\ncampaign  reusing {campaign['id']}")
    else:
        campaign = client.create_campaign(fm["campaign_name"], iso(start))
        print(f"\ncampaign  created {campaign['id']}")

    squad = client.create_adsquad(name=fm["ad_set_name"], campaign_id=campaign["id"],
                                  targeting=targeting, daily_budget_inr=budget,
                                  start_time=iso(start), end_time=iso(end))
    print(f"ad squad  created {squad['id']}")

    media = client.upload_media(f'{fm["ad_name"]}_MEDIA', asset)
    print(f"media     uploaded {media['id']}")

    # utm_id needs the ad id, which does not exist yet; the URL is rewritten below.
    provisional = _utm_url(fm["destination_url"], fm["campaign_name"], squad["id"], "", fm["ad_name"])
    creative = client.create_creative(name=fm["ad_name"], media_id=media["id"],
                                      headline=args.headline, brand_name="Riteangle",
                                      url=provisional,
                                      profile_id=config["snap"]["profile_id"])
    print(f"creative  created {creative['id']}")

    ad = client.create_ad(name=fm["ad_name"], ad_squad_id=squad["id"], creative_id=creative["id"])
    print(f"ad        created {ad['id']}")

    final_url = _utm_url(fm["destination_url"], fm["campaign_name"], squad["id"],
                         ad["id"], fm["ad_name"])
    client.set_creative_url(creative, final_url)
    print("creative  landing URL rewritten with the real ad id")

    # ---- read back, and diff against what was asked for ----
    print("\nRead-back:")
    squad_live = client.get(f"/adsquads/{squad['id']}")["adsquads"][0]["adsquad"]
    ad_live = client.get(f"/ads/{ad['id']}")["ads"][0]["ad"]
    creative_live = client.get(f"/creatives/{creative['id']}")["creatives"][0]["creative"]
    demo = (squad_live.get("targeting", {}).get("demographics") or [{}])[0]

    checks = [
        ("ad squad status", squad_live.get("status"), "PAUSED"),
        ("ad status", ad_live.get("status"), "PAUSED"),
        ("daily budget", squad_live.get("daily_budget_micro"), int(budget * snapapi.MICRO)),
        ("optimisation goal", squad_live.get("optimization_goal"), "LANDING_PAGE_VIEW"),
        ("gender", demo.get("gender"), "FEMALE"),
        ("min age", str(demo.get("min_age")), "18"),
        ("max age", str(demo.get("max_age")), "22"),
        ("country", (squad_live.get("targeting", {}).get("geos") or [{}])[0].get("country_code"), "in"),
        ("os", (squad_live.get("targeting", {}).get("devices") or [{}])[0].get("os_type"), "ANDROID"),
        ("headline", creative_live.get("headline"), args.headline),
        ("landing url", creative_live.get("web_view_properties", {}).get("url"), final_url),
    ]
    bad = 0
    for label, got, want in checks:
        ok = str(got) == str(want)
        bad += not ok
        print(f"  {'ok ' if ok else 'DIFF'}  {label:18} {got}")
        if not ok:
            print(f"        {'':18} expected: {want}")

    print()
    if bad:
        print(f"{bad} field(s) differ from the plan. Fix in Ads Manager before enabling.")
    else:
        print("Every field matches the plan.")
    print("Nothing is live: all objects are PAUSED. Enabling is a human action in Ads Manager.")
    print(f"\nWhen you have enabled it, close the loop:\n"
          f"  ad-agent log-setup {args.rec_id} --network snap \\\n"
          f"    --campaign-id {campaign['id']} \\\n"
          f"    --ad-set-id {squad['id']} \\\n"
          f"    --ad-id {ad['id']}")


def cmd_log_setup(args: argparse.Namespace, ledger: Ledger) -> None:
    rec = ledger.log_setup(
        args.rec_id,
        network=args.network,
        campaign_id=args.campaign_id,
        ad_set_id=args.ad_set_id,
        ad_id=args.ad_id,
        deviated=args.deviated,
        today=_today(),
    )
    ledger.write_index()
    print(f"logged setup for {rec.rec_id} -> status=live")


def cmd_log_review(args: argparse.Namespace, ledger: Ledger) -> None:
    rec = ledger.log_review(
        args.rec_id,
        verdict=args.verdict,
        summary=args.summary,
        review_log_path=args.review_log,
        today=_today(),
    )
    ledger.write_index()
    print(f"logged review for {rec.rec_id} -> verdict={args.verdict}")


def cmd_abandon(args: argparse.Namespace, ledger: Ledger) -> None:
    rec = ledger.abandon(args.rec_id, reason=args.reason, today=_today())
    ledger.write_index()
    print(f"abandoned {rec.rec_id}")


def cmd_stats(args: argparse.Namespace, ledger: Ledger) -> None:
    records = ledger.all()
    by_status: dict[str, int] = {}
    by_verdict: dict[str, int] = {}
    for r in records:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        v = r.front_matter.get("verdict")
        if v:
            by_verdict[v] = by_verdict.get(v, 0) + 1

    print(f"total: {len(records)}")
    for s in STATUSES:
        if by_status.get(s):
            print(f"  {s}: {by_status[s]}")
    if by_verdict:
        print("verdicts (of reviewed):")
        for v, n in sorted(by_verdict.items()):
            print(f"  {v}: {n}")


def cmd_dump_ledger(args: argparse.Namespace, ledger: Ledger) -> None:
    path = ledger.write_index()
    text = path.read_text(encoding="utf-8")
    if args.status:
        lines = text.splitlines()
        header, rows = lines[:6], lines[6:]
        rows = [r for r in rows if f"| {args.status} |" in r]
        text = "\n".join(header + rows)
    print(text)


def cmd_fetch_analytics(args: argparse.Namespace, config: dict) -> None:
    url = config.get("pdc", {}).get("analytics_url")
    api_key = config.get("pdc", {}).get("api_key")
    if not url or not api_key:
        print(
            "pdc.analytics_url / pdc.api_key are not set in config.local.yaml "
            "(see config.example.yaml). This also does nothing useful until the "
            "pocket-dating-coach PR adding /api/internal/ad-analytics has shipped "
            "— see SPEC.md, 'Data access'.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    qs = (
        f"?start={args.start}&end={args.end}&currency={args.currency}"
        f"&network={args.network}&audience={args.audience}"
    )
    req = urllib.request.Request(url + qs, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"fetch failed: {e}", file=sys.stderr)
        raise SystemExit(1)

    if args.out:
        Path(args.out).write_text(body, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(body)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ad-agent")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("propose", help="Record a mode-5 recommendation before you execute it")
    sp.add_argument("slug", help="short campaign slug, used as the ledger folder name")
    sp.add_argument("--network", required=True, choices=["snap", "meta"])
    sp.add_argument("--campaign-name", required=True)
    sp.add_argument("--ad-set-name", required=True)
    sp.add_argument("--ad-name", required=True)
    sp.add_argument("--targeting-summary", required=True)
    sp.add_argument("--creative-ref", required=True, help="path or id under creatives/")
    sp.add_argument(
        "--destination-url",
        required=True,
        help="the landing URL this ad set sends traffic to; checked against rules/destinations.yaml",
    )
    sp.add_argument("--budget-cap", required=True, type=float, help="INR per day")
    sp.add_argument("--duration-days", required=True, type=int)
    sp.add_argument("--brief", required=True, help="path to a markdown brief file")
    sp.set_defaults(func=cmd_propose)

    sp = sub.add_parser(
        "snap-push",
        help="Create a proposed recommendation in Snap Ads Manager, PAUSED, then diff it back",
    )
    sp.add_argument("rec_id")
    sp.add_argument("--headline", default="A shortlist that means something.",
                    help="Snap headline, 34 chars max")
    sp.add_argument("--dry-run", action="store_true",
                    help="print the plan and create nothing")
    sp.set_defaults(func=cmd_snap_push)

    sp = sub.add_parser(
        "amend",
        help="Revise a still-proposed recommendation, with an audit trail of what changed",
    )
    sp.add_argument("rec_id")
    sp.add_argument("--reason", required=True, help="why this proposal is being revised")
    sp.add_argument("--campaign-name", default=None)
    sp.add_argument("--ad-set-name", default=None)
    sp.add_argument("--ad-name", default=None)
    sp.add_argument("--targeting-summary", default=None)
    sp.add_argument("--creative-ref", default=None)
    sp.add_argument(
        "--destination-url",
        default=None,
        help="re-runs the rules/destinations.yaml gate against the resulting pair",
    )
    sp.add_argument("--budget-cap", default=None, type=float, help="INR per day")
    sp.add_argument("--duration-days", default=None, type=int)
    sp.set_defaults(func=cmd_amend)

    sp = sub.add_parser("log-setup", help="Record the real IDs after setting the ad up by hand")
    sp.add_argument("rec_id")
    sp.add_argument("--network", required=True, choices=["snap", "meta"])
    sp.add_argument("--campaign-id", required=True)
    sp.add_argument("--ad-set-id", required=True)
    sp.add_argument("--ad-id", required=True)
    sp.add_argument("--deviated", default=None, help="what changed from the brief, if anything")
    sp.set_defaults(func=cmd_log_setup)

    sp = sub.add_parser("log-review", help="Record mode-6's verdict on a live recommendation")
    sp.add_argument("rec_id")
    sp.add_argument("--verdict", required=True, choices=["working", "not-working", "inconclusive"])
    sp.add_argument("--summary", required=True)
    sp.add_argument("--review-log", default=None, help="path to a markdown review-detail file")
    sp.set_defaults(func=cmd_log_review)

    sp = sub.add_parser("abandon", help="Close out a recommendation that was never executed")
    sp.add_argument("rec_id")
    sp.add_argument("--reason", required=True)
    sp.set_defaults(func=cmd_abandon)

    sp = sub.add_parser("stats", help="Deterministic counts over the ledger")
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("dump-ledger", help="Print the ledger index")
    sp.add_argument("--status", default=None, choices=list(STATUSES))
    sp.set_defaults(func=cmd_dump_ledger)

    sp = sub.add_parser(
        "fetch-analytics",
        help="Pull pocket-dating-coach's ad analytics via the authenticated internal endpoint",
    )
    sp.add_argument("--start", required=True, help="YYYY-MM-DD, IST day, inclusive")
    sp.add_argument("--end", required=True, help="YYYY-MM-DD, IST day, inclusive")
    sp.add_argument("--currency", default="INR", choices=["INR", "USD"])
    sp.add_argument("--network", default="all", choices=["all", "snap", "meta", "other"])
    sp.add_argument("--audience", default="all", choices=["all", "men", "women", "unknown"])
    sp.add_argument("--out", default=None, help="write JSON here instead of stdout")
    sp.set_defaults(func=cmd_fetch_analytics)

    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config = load_config()

    if args.command == "fetch-analytics":
        cmd_fetch_analytics(args, config)
        return

    ledger = Ledger(Path(config["ledger"]["root"]))
    args.func(args, ledger)


if __name__ == "__main__":
    main()
