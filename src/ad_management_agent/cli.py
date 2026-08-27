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

from . import budget as budgetrules
from . import destinations
from . import meta as metaapi
from . import networks as networkreg
from . import research as researchmod
from . import snap as snapapi
from . import targeting as targetingspec
from .config import load_config
from .ledger import STATUSES, Ledger


def _today() -> str:
    """Today in the machine's local timezone, deliberately.

    Every date this repo writes is a business date read alongside
    pocket-dating-coach's analytics, which bucket by IST day (`fetch-analytics`
    takes `--start`/`--end` as IST days). A UTC date would disagree with those
    buckets for five and a half hours out of every twenty-four, which is exactly
    the window an evening review happens in. ruff's DTZ011 is right in general and
    wrong here.
    """
    return _dt.date.today().isoformat()  # noqa: DTZ011 — IST business date, see above


def _check_network(rules_dir: Path, network: str) -> None:
    """Validate --network against the registry, at run time.

    Not an argparse `choices=` list, because the parser is built before config is
    loaded and so cannot know where the registry lives — and because a hardcoded
    pair here is exactly what this registry exists to remove. The runtime error
    carries the registered names and points at the file.
    """
    try:
        networkreg.get(rules_dir, network)
    except networkreg.NetworkError as exc:
        _fail(exc)


NETWORK_HELP = "network key from rules/networks.yaml (currently: snap, meta)"


def _add_targeting_flags(sp: argparse.ArgumentParser, *, required: bool) -> None:
    """The structured audience, as flags on both `propose` and `amend`.

    Discrete flags rather than a JSON blob or a second file: a skill calls this
    programmatically and a human reads the invocation back in the shell history,
    and both are better served by `--gender FEMALE --min-age 18` than by quoting
    YAML through argv.
    """
    g = sp.add_argument_group(
        "targeting (structured — this is what snap-push and meta-push actually push)"
    )
    g.add_argument("--gender", required=required, default=None,
                   choices=list(targetingspec.GENDERS),
                   help="single-gender only; rules/targeting.md forbids a mixed ad set")
    g.add_argument("--min-age", required=required, default=None,
                   help="18 or above — rules/compliance.md is 18+ without exception")
    g.add_argument("--max-age", required=required, default=None,
                   help="a number, or 50+ for the open-ended top band")
    g.add_argument("--countries", required=required, default=None,
                   help="comma-separated 2-letter codes, e.g. in")
    g.add_argument("--os", default=None, choices=list(targetingspec.OS_TYPES),
                   help="omit to target all devices")
    g.add_argument("--expansion", default=None, choices=["on", "off"],
                   help="Snap targeting expansion; defaults to on for a new proposal")


def _targeting_patch(args: argparse.Namespace) -> dict:
    """Only the targeting fields the caller actually passed."""
    patch: dict = {}
    if args.gender is not None:
        patch["gender"] = args.gender.upper()
    if args.min_age is not None:
        patch["min_age"] = str(args.min_age)
    if args.max_age is not None:
        patch["max_age"] = str(args.max_age)
    if args.countries is not None:
        patch["countries"] = [c.strip().lower() for c in args.countries.split(",") if c.strip()]
    if args.os is not None:
        patch["os"] = args.os.upper()
    if args.expansion is not None:
        patch["expansion"] = args.expansion == "on"
    return patch


def _fail(exc: Exception) -> None:
    print(f"error: {exc}", file=sys.stderr)
    raise SystemExit(2) from exc


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
        _fail(exc)

    # The structured audience, validated before anything is written, and checked
    # against the ad-set name so the record cannot disagree with itself.
    try:
        spec = targetingspec.build(
            gender=args.gender,
            min_age=args.min_age,
            max_age=args.max_age,
            countries=[c.strip() for c in args.countries.split(",")],
            os=args.os,
            expansion=(args.expansion or "on") == "on",
        )
        targetingspec.check_matches_ad_set_name(spec, args.ad_set_name)
    except targetingspec.TargetingError as exc:
        _fail(exc)

    if budgetrules.below_floor(args.budget_cap):
        print(f"note: {budgetrules.floor_note(args.budget_cap)}\n"
              "      Proposing anyway — the cap is your call, but say why in the brief.",
              file=sys.stderr)

    _check_network(ledger.root / "rules", args.network)

    rec = ledger.propose(
        slug=args.slug,
        network=args.network,
        campaign_name=args.campaign_name,
        ad_set_name=args.ad_set_name,
        ad_name=args.ad_name,
        targeting_summary=args.targeting_summary,
        targeting=spec,
        creative_ref=args.creative_ref,
        destination_url=args.destination_url,
        budget_cap_inr_per_day=args.budget_cap,
        duration_days=args.duration_days,
        brief_path=args.brief,
        from_idea=args.from_idea,
        today=_today(),
    )
    ledger.write_index()

    # Close the idea, so an approved idea that became a real record stops being
    # reported as one nobody acted on.
    if args.from_idea:
        try:
            _research(ledger).mark_idea_proposed(args.from_idea, rec_id=rec.rec_id, today=_today())
        except (researchmod.ResearchError, KeyError) as exc:
            print(f"warning: proposal written, but {args.from_idea} was not closed: {exc}",
                  file=sys.stderr)
        else:
            print(f"closed idea {args.from_idea}")

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

    rec = ledger.find(args.rec_id)

    # Targeting is patched, not replaced: `--min-age 23` on its own should move one
    # field, not silently drop the geography. The merged result is validated as a
    # whole, so a patch cannot leave the record in a state propose would refuse.
    patch = _targeting_patch(args)
    if patch:
        merged = {**(rec.front_matter.get("targeting") or {}), **patch}
        try:
            targetingspec.validate(merged)
            targetingspec.check_matches_ad_set_name(
                merged, changes.get("ad_set_name") or rec.front_matter.get("ad_set_name", "")
            )
        except targetingspec.TargetingError as exc:
            _fail(exc)
        changes["targeting"] = merged

    if not changes:
        print("error: nothing to amend — pass at least one field to change", file=sys.stderr)
        raise SystemExit(2)

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
            _fail(exc)

        # Renaming an ad set can flip the gender token, which would leave a record
        # whose name and targeting disagree. Re-check even when the targeting itself
        # was not part of this amendment.
        if "ad_set_name" in changes and rec.front_matter.get("targeting"):
            try:
                targetingspec.check_matches_ad_set_name(
                    changes.get("targeting") or rec.front_matter["targeting"],
                    changes["ad_set_name"],
                )
            except targetingspec.TargetingError as exc:
                _fail(exc)

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


def _gate_campaign_caps(caps: dict, *, squad_daily_inr: float, duration_days: int,
                        rec_id: str, accept: bool) -> None:
    """Refuse to hang an ad squad off a campaign whose own cap would starve it.

    The lower figure binds. WOMEN_18-22_CASUAL_LPV was pushed on 2026-08-26 with an
    ad squad at Rs 1,000/day under a campaign capped at Rs 300/day; the effective
    spend was 30% of the plan and below rules/budget.md's floor, which made the
    result inconclusive before a rupee was spent. The push printed nothing about it
    because nothing read the parent.

    This is not the destination gate — there IS an escape hatch here, because a low
    cap is sometimes a deliberate choice rather than an error. But it is explicit,
    it names the deviation, and it tells you where to record it.
    """
    daily_cap = caps.get("daily_inr")
    lifetime_cap = caps.get("lifetime_inr")
    planned_total = squad_daily_inr * duration_days

    binding = []
    if daily_cap is not None and daily_cap < squad_daily_inr:
        binding.append(
            f"campaign daily cap is Rs {daily_cap:.0f}/day, below this ad squad's "
            f"Rs {squad_daily_inr:.0f}/day — the cap binds, so effective spend is "
            f"Rs {daily_cap:.0f}/day"
        )
    if lifetime_cap is not None and lifetime_cap < planned_total:
        binding.append(
            f"campaign lifetime cap is Rs {lifetime_cap:.0f}, below the planned "
            f"Rs {planned_total:.0f} ({squad_daily_inr:.0f} x {duration_days}d)"
        )

    if not binding:
        if daily_cap is None and lifetime_cap is None:
            print("campaign  no spend cap on the parent — the ad squad budget is the "
                  "effective one")
        else:
            print(f"campaign  cap checked: daily={daily_cap}, lifetime={lifetime_cap} — "
                  "neither binds")
        if budgetrules.below_floor(squad_daily_inr):
            print(f"WARNING   {budgetrules.floor_note(squad_daily_inr)}")
        return

    effective = min([v for v in (daily_cap, squad_daily_inr) if v is not None])
    lines = ["", "BLOCKED: the parent campaign's own cap would override this ad squad's budget."]
    lines += [f"  - {b}" for b in binding]
    if budgetrules.below_floor(effective):
        lines += ["", "  " + budgetrules.floor_note(effective)]
    lines += [
        "",
        "  Fix the cap in Ads Manager (Campaign > Daily spend cap) and push again — or, if the",
        "  cap is deliberate, re-run with --accept-campaign-cap to create it anyway. Doing that",
        "  records the deviation rather than hiding it:",
        f"    ad-agent note {rec_id} --kind budget --text \"...\"",
    ]
    if not accept:
        print("\n".join(lines), file=sys.stderr)
        raise SystemExit(2)
    print("\n".join(lines))
    print("\n--accept-campaign-cap: proceeding with the cap above as a stated deviation.")


def _utm_query(rules_dir: Path, network: str, campaign_name: str,
               ad_squad_id: str, ad_id: str, ad_name: str) -> str:
    """rules/tracking.md's five parameters as a bare query string, no leading `?`.

    Split out from `_utm_url` because the two networks want it at different points
    in the URL. Snap takes a complete Website URL on the creative, so the params
    are appended there. Meta takes them in the ad's own `url_tags` field, which is
    query-string syntax WITHOUT a base URL or a `?` — passing a full URL there
    produces a link with the destination embedded in its own query string, which
    fails silently by still being a valid URL.

    The parameter names come from rules/networks.yaml rather than from literals
    here, because Snap and Meta genuinely disagree about which one carries the ad
    id and this function is one copy-paste away from being reused for the wrong
    one.
    """
    from urllib.parse import urlencode
    return urlencode(
        networkreg.utm_params(rules_dir, network, campaign_name=campaign_name,
                              ad_set_id=ad_squad_id, ad_id=ad_id, ad_name=ad_name)
    )


def _utm_url(rules_dir: Path, network: str, destination: str, campaign_name: str,
             ad_squad_id: str, ad_id: str, ad_name: str) -> str:
    """The destination with rules/tracking.md's scheme appended, every value literal.

    Ads Manager fills these from {{macros}}; the 2026-08-21 incident was a macro
    that silently never resolved. Pushed through the API the ids are known facts by
    the time the URL is written, so there is no macro left to fail.
    """
    return destination + "?" + _utm_query(
        rules_dir, network, campaign_name, ad_squad_id, ad_id, ad_name)


def cmd_snap_push(args: argparse.Namespace, ledger: Ledger) -> None:
    config = load_config()
    rec = ledger.find(args.rec_id)
    fm = rec.front_matter

    # Two checks, deliberately. This command only knows how to talk to Snap, and
    # separately the registry has to declare that creating on it is permitted at
    # all. The registry can only tighten this — editing it cannot teach this
    # function a second API.
    if fm.get("network") != "snap":
        print(f"error: {args.rec_id} is network={fm.get('network')!r}, not snap", file=sys.stderr)
        raise SystemExit(2)
    try:
        networkreg.require_creation(ledger.root / "rules", "snap", mode="paused-only")
    except networkreg.NetworkError as exc:
        _fail(exc)
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
    def iso(d):
        return d.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    budget = float(fm["budget_cap_inr_per_day"])

    spec = fm.get("targeting")
    if not spec:
        print(f"error: {args.rec_id} has no structured `targeting` block, so there is nothing\n"
              "safe to push. Until 2026-08-26 this command used a hardcoded audience, which\n"
              "meant any record but the first would have been created with the first one's\n"
              "targeting and still diffed clean. Add it:\n"
              f"  ad-agent amend {args.rec_id} --reason 'add structured targeting' \\\n"
              "    --gender FEMALE --min-age 18 --max-age 22 --countries in --os ANDROID",
              file=sys.stderr)
        raise SystemExit(2)
    try:
        targetingspec.validate(spec)
        targetingspec.check_matches_ad_set_name(spec, fm["ad_set_name"])
    except targetingspec.TargetingError as exc:
        _fail(exc)
    targeting = targetingspec.to_snap(spec)

    plan = [
        ("campaign   ", fm["campaign_name"]),
        ("ad squad   ", (f'{fm["ad_set_name"]}  Rs {budget:.0f}/day x '
                         f'{fm["duration_days"]}d, LANDING_PAGE_VIEW, AUTO_BID')),
        ("ad         ", fm["ad_name"]),
        ("creative   ", f'{asset.name}  headline={args.headline!r}  CTA=MORE'),
        ("destination", fm["destination_url"]),
        ("targeting  ", targetingspec.describe(spec)),
    ]
    print(f"Plan for {args.rec_id} (everything created PAUSED):")
    for k, v in plan:
        print(f"  {k}  {v}")

    # A dry run still reads the parent campaign's spend cap. That check is the whole
    # reason to dry-run at all — it is the one thing that can silently invalidate the
    # test — so returning before it would leave the rehearsal unable to rehearse the
    # only failure it exists to catch. Both calls behind it are read-only GETs.
    client = None
    try:
        client = snapapi.SnapClient(config.get("snap") or {})
    except snapapi.SnapError as exc:
        if not args.dry_run:
            _fail(exc)
        print(f"\nnote: no Snap credentials, so the parent campaign's spend cap was NOT\n"
              f"      checked — the one thing most likely to make this ad set unreadable.\n"
              f"      ({exc})")

    campaign = None
    if client is not None:
        campaign = client.find_campaign(fm["campaign_name"])
        if campaign:
            print(f"\ncampaign  reusing {campaign['id']}")
        elif args.dry_run:
            print(f"\ncampaign  {fm['campaign_name']} does not exist yet; it would be created "
                  "new, with no cap to inherit")
        else:
            campaign = client.create_campaign(fm["campaign_name"], iso(start))
            print(f"\ncampaign  created {campaign['id']}")

    # Checked before the ad squad exists, not after: a cap that binds is cheaper to
    # fix while there is nothing hanging off the campaign yet.
    if campaign is not None:
        caps = client.campaign_caps(campaign["id"])
        _gate_campaign_caps(caps, squad_daily_inr=budget, duration_days=int(fm["duration_days"]),
                            rec_id=args.rec_id, accept=args.accept_campaign_cap)
        if not args.dry_run:
            ledger.record_campaign_caps(args.rec_id, daily_inr=caps.get("daily_inr"),
                                        lifetime_inr=caps.get("lifetime_inr"), today=_today())

    if args.dry_run:
        print("\n--dry-run: nothing created.")
        return

    squad = client.create_adsquad(name=fm["ad_set_name"], campaign_id=campaign["id"],
                                  targeting=targeting, daily_budget_inr=budget,
                                  start_time=iso(start), end_time=iso(end),
                                  pixel_id=(config.get("snap") or {}).get("pixel_id"))
    print(f"ad squad  created {squad['id']}")

    media = client.upload_media(f'{fm["ad_name"]}_MEDIA', asset)
    print(f"media     uploaded {media['id']}")

    # utm_id needs the ad id, which does not exist yet; the URL is rewritten below.
    provisional = _utm_url(ledger.root / "rules", "snap", fm["destination_url"],
                           fm["campaign_name"], squad["id"], "", fm["ad_name"])
    creative = client.create_creative(name=fm["ad_name"], media_id=media["id"],
                                      headline=args.headline, brand_name="Riteangle",
                                      url=provisional,
                                      profile_id=config["snap"]["profile_id"])
    print(f"creative  created {creative['id']}")

    ad = client.create_ad(name=fm["ad_name"], ad_squad_id=squad["id"], creative_id=creative["id"])
    print(f"ad        created {ad['id']}")

    final_url = _utm_url(ledger.root / "rules", "snap", fm["destination_url"],
                         fm["campaign_name"], squad["id"], ad["id"], fm["ad_name"])
    client.set_creative_url(creative, final_url)
    print("creative  landing URL rewritten with the real ad id")

    # ---- read back, and diff against what was asked for ----
    print("\nRead-back:")
    squad_live = client.get(f"/adsquads/{squad['id']}")["adsquads"][0]["adsquad"]
    ad_live = client.get(f"/ads/{ad['id']}")["ads"][0]["ad"]
    creative_live = client.get(f"/creatives/{creative['id']}")["creatives"][0]["creative"]

    checks = [
        ("ad squad status", squad_live.get("status"), "PAUSED"),
        ("ad status", ad_live.get("status"), "PAUSED"),
        ("daily budget", squad_live.get("daily_budget_micro"), int(budget * snapapi.MICRO)),
        ("optimisation goal", squad_live.get("optimization_goal"), "LANDING_PAGE_VIEW"),
        # Derived from the record's own spec, never from a literal — a read-back
        # compared against a hardcoded dict only ever validates the code against
        # itself, which is how a wrong audience would have passed silently.
        *targetingspec.snap_readback_checks(spec, squad_live),
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

    # Meta's per-feature creative enhancements, reported rather than assumed. The
    # single standard_enhancements opt-out was deprecated on 2026-08-28 and its
    # replacement names are documented only behind an internal URL, so the honest
    # thing is to print what Meta actually turned on and let a human decide. An
    # enhancement applied after rules/creative-generation.md's §10 QA gate voids the
    # sign-off that gate exists to give.
    dof = (creative_live.get("degrees_of_freedom_spec") or {}).get(
        "creative_features_spec") or {}
    opted_in = sorted(k for k, v in dof.items()
                      if str((v or {}).get("enroll_status", "")).upper() == "OPT_IN")
    if opted_in:
        print()
        print("CREATIVE ENHANCEMENTS Meta enabled by itself — the QA gate signed off on")
        print("the asset as built, and these change it after that sign-off:")
        for k in opted_in:
            print(f"  OPT_IN  {k}")
        print("  Turn them off per-ad in Ads Manager (Advantage+ creative) before enabling,")
        print("  or accept them deliberately. Names captured for a precise opt-out:")
        print(f"    {', '.join(opted_in)}")
    elif dof:
        print()
        print(f"creative enhancements: none opted in ({len(dof)} feature(s) reported)")

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


def _gate_campaign_budget_optimization(caps: dict, *, rec_id: str) -> None:
    """Refuse to hang an ad set off a Meta campaign that holds the budget itself.

    This has no Snap equivalent and it is strictly worse than the cap problem that
    `_gate_campaign_caps` exists for. A capped campaign *reduces* the ad set's spend,
    which is at least proportional and visible in the numbers. A campaign using
    campaign-budget optimisation **ignores the ad-set budget outright** and
    distributes its own across children as it sees fit — so the `budget_cap_inr_per_day`
    the ledger record states, and that `rules/budget.md`'s floor was checked against,
    becomes a number with no relationship to what gets spent.

    There is no escape hatch, unlike the cap gate. `--accept-campaign-cap` exists
    because a low cap is sometimes deliberate; a CBO parent is not a deviation to
    accept, it is a statement that this record cannot mean what it says. Move the ad
    set to a non-CBO campaign, or turn CBO off in Ads Manager.
    """
    if not caps.get("campaign_budget_optimization"):
        return
    print(
        f"error: the parent campaign uses campaign-budget optimisation, so it holds the\n"
        f"       budget and this ad set's Rs/day would be IGNORED rather than capped.\n"
        f"       (campaign daily={caps.get('daily_inr')}, lifetime={caps.get('lifetime_inr')})\n\n"
        f"       {rec_id} states a budget cap that would not describe what gets spent, and\n"
        f"       rules/budget.md's floor was checked against that same number. Turn CBO off\n"
        f"       in Ads Manager, or point this record at a non-CBO campaign.\n\n"
        f"       There is deliberately no --accept flag for this: a low cap can be a\n"
        f"       choice, but a CBO parent means the record cannot mean what it says.",
        file=sys.stderr)
    raise SystemExit(2)


def cmd_meta_push(args: argparse.Namespace, ledger: Ledger) -> None:
    """Create a proposed record on Meta, PAUSED, and diff it back.

    The sibling of `cmd_snap_push`, and deliberately the same shape: same record
    gates, same destination gate, same QA-pass requirement, same parent-cap check,
    same read-back-and-diff. Where it differs, it differs because Meta does.
    """
    config = load_config()
    rec = ledger.find(args.rec_id)
    fm = rec.front_matter

    # Two checks, deliberately — the same pair snap-push makes. This command only
    # knows how to talk to Meta, and separately the registry has to declare that
    # creating on it is permitted at all. The registry can only tighten this;
    # editing it cannot teach this function a second API.
    if fm.get("network") != "meta":
        print(f"error: {args.rec_id} is network={fm.get('network')!r}, not meta", file=sys.stderr)
        raise SystemExit(2)
    try:
        networkreg.require_creation(ledger.root / "rules", "meta", mode="paused-only")
    except networkreg.NetworkError as exc:
        _fail(exc)
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
    def iso(d):
        # Meta wants ISO 8601 with an offset, where Snap wants a milliseconds-and-Z
        # format. Same instant, different spelling; neither accepts the other's.
        return d.strftime("%Y-%m-%dT%H:%M:%S+0000")

    budget = float(fm["budget_cap_inr_per_day"])

    spec = fm.get("targeting")
    if not spec:
        print(f"error: {args.rec_id} has no structured `targeting` block, so there is nothing\n"
              "safe to push. Add it:\n"
              f"  ad-agent amend {args.rec_id} --reason 'add structured targeting' \\\n"
              "    --gender FEMALE --min-age 25 --max-age 30 --countries in",
              file=sys.stderr)
        raise SystemExit(2)
    try:
        targetingspec.validate(spec)
        targetingspec.check_matches_ad_set_name(spec, fm["ad_set_name"])
    except targetingspec.TargetingError as exc:
        _fail(exc)
    targeting = targetingspec.to_meta(spec)

    plan = [
        ("campaign   ", f'{fm["campaign_name"]}  OUTCOME_TRAFFIC'),
        ("ad set     ", (f'{fm["ad_set_name"]}  Rs {budget:.0f}/day x '
                         f'{fm["duration_days"]}d, LANDING_PAGE_VIEWS, lowest cost')),
        ("ad         ", fm["ad_name"]),
        ("creative   ", f'{asset.name}  headline={args.headline!r}  CTA={args.cta}'),
        ("destination", fm["destination_url"]),
        ("targeting  ", targetingspec.describe(spec)),
    ]
    print(f"Plan for {args.rec_id} (everything created PAUSED):")
    for k, v in plan:
        print(f"  {k}  {v}")
    # Said out loud in the plan, because it is the one field of the spec that does
    # not survive the crossing and a silent drop is how a reader comes to believe a
    # declaration was made that was not.
    if spec.get("regulated_content", True):
        print("  note         regulated_content has no Meta equivalent and is NOT sent; "
              "Meta gates dating at the account level instead")

    # A dry run still reads the parent campaign's budget state. That check is the
    # whole reason to dry-run — it is the one thing that can silently invalidate the
    # test — so returning before it would leave the rehearsal unable to rehearse the
    # only failure it exists to catch. Everything behind it is a read-only GET.
    client = None
    try:
        client = metaapi.MetaClient(config.get("meta") or {})
    except metaapi.MetaError as exc:
        if not args.dry_run:
            _fail(exc)
        print(f"\nnote: no Meta credentials, so the parent campaign's budget state was NOT\n"
              f"      checked — the one thing most likely to make this ad set unreadable.\n"
              f"      ({exc})")

    campaign = None
    if client is not None:
        # Before anything else: the currency, because every rupee figure below is
        # converted to paise on the way out and a non-INR account makes that wrong.
        client.require_inr()
        campaign = client.find_campaign(fm["campaign_name"])
        if campaign:
            print(f"\ncampaign  reusing {campaign['id']}")
        elif args.dry_run:
            print(f"\ncampaign  {fm['campaign_name']} does not exist yet; it would be created "
                  "new, with no budget of its own to inherit")
        else:
            campaign = client.create_campaign(fm["campaign_name"])
            print(f"\ncampaign  created {campaign['id']}")

    # Checked before the ad set exists, not after: a parent that would starve or
    # override this ad set is cheaper to fix while nothing hangs off it yet.
    if campaign is not None:
        caps = client.campaign_caps(campaign["id"])
        _gate_campaign_budget_optimization(caps, rec_id=args.rec_id)
        _gate_campaign_caps(caps, squad_daily_inr=budget, duration_days=int(fm["duration_days"]),
                            rec_id=args.rec_id, accept=args.accept_campaign_cap)
        if not args.dry_run:
            ledger.record_campaign_caps(args.rec_id, daily_inr=caps.get("daily_inr"),
                                        lifetime_inr=caps.get("lifetime_inr"), today=_today())

    if args.dry_run:
        print("\n--dry-run: nothing created.")
        return

    # Resume rather than duplicate. There is no rollback here and five objects to
    # create, so a run that dies partway is a normal state to recover from, not an
    # anomaly — see find_adset for the 2026-08-28 case this comes from. The read-back
    # below diffs a reused ad set against the record just as hard as a new one, so
    # reuse cannot smuggle in the wrong budget or audience.
    adset = client.find_adset(fm["ad_set_name"], campaign["id"])
    if adset:
        print(f"ad set    reusing {adset['id']} (already existed under this campaign)")
    else:
        adset = client.create_adset(name=fm["ad_set_name"], campaign_id=campaign["id"],
                                    targeting=targeting, daily_budget_inr=budget,
                                    start_time=iso(start), end_time=iso(end),
                                    pixel_id=(config.get("meta") or {}).get("pixel_id"))
        print(f"ad set    created {adset['id']}")

    image_hash = client.upload_image(asset)
    print(f"image     uploaded hash={image_hash}")

    # The creative's link carries the destination and the params that are known now.
    # utm_content has to carry the AD id on Meta (per traffic-quality.ts) and the ad
    # does not exist yet, so the id goes on afterwards via the ad's url_tags.
    creative = client.create_creative(
        name=f'{fm["ad_name"]}_CREATIVE', image_hash=image_hash,
        headline=args.headline, message=args.message,
        url=fm["destination_url"], call_to_action=args.cta)
    print(f"creative  created {creative['id']}")

    ad = client.find_ad(fm["ad_name"], adset["id"])
    if ad:
        print(f"ad        reusing {ad['id']} (already existed under this ad set)")
    else:
        ad = client.create_ad(name=fm["ad_name"], adset_id=adset["id"],
                              creative_id=creative["id"])
        print(f"ad        created {ad['id']}")

    # The ad id only exists now, and utm_content has to carry it on Meta. Neither the
    # ad nor an existing creative accepts url_tags after the fact — the ad-level POST
    # returns 200 and silently does nothing — so the tracking arrives as a new
    # creative built with url_tags at creation, which the ad is then repointed at.
    # See MetaClient.attach_tracked_creative for what was tried and what persists.
    url_tags = _utm_query(ledger.root / "rules", "meta", fm["campaign_name"],
                          adset["id"], ad["id"], fm["ad_name"])
    creative = client.attach_tracked_creative(
        ad_id=ad["id"], creative=client.get(
            f"/{creative['id']}", fields="id,object_story_spec"),
        url_tags=url_tags, name=f'{fm["ad_name"]}_CREATIVE_TRACKED')
    print(f"creative  {creative['id']} attached, url_tags carry the real ad id "
          f"(no {{{{macro}}}} to not resolve)")

    # ---- read back, and diff against what was asked for ----
    print("\nRead-back:")
    adset_live = client.get(
        f"/{adset['id']}",
        fields="id,name,status,daily_budget,optimization_goal,billing_event,targeting")
    # url_tags is NOT a readable field on an ad — asking for it 400s the whole
    # read-back ("Tried accessing nonexisting field"). It lives on the creative.
    ad_live = client.get(f"/{ad['id']}", fields="id,name,status,creative")
    creative_live = client.get(
        f"/{creative['id']}",
        fields="id,name,url_tags,object_story_spec,degrees_of_freedom_spec")
    link_data = ((creative_live.get("object_story_spec") or {}).get("link_data") or {})

    checks = [
        ("ad set status", adset_live.get("status"), "PAUSED"),
        ("ad status", ad_live.get("status"), "PAUSED"),
        # Compared in paise, in the unit Meta actually stores, so a minor-unit
        # mistake shows up here as a diff rather than as a plausible-looking number.
        ("daily budget (paise)", adset_live.get("daily_budget"),
         round(budget * metaapi.MINOR)),
        ("optimisation goal", adset_live.get("optimization_goal"), "LANDING_PAGE_VIEWS"),
        # Derived from the record's own spec, never from a literal — a read-back
        # compared against a hardcoded dict only ever validates the code against
        # itself, which is how a wrong audience would pass silently.
        *targetingspec.meta_readback_checks(spec, adset_live),
        ("headline", link_data.get("name"), args.headline),
        ("landing url", link_data.get("link"), fm["destination_url"]),
        ("url_tags", creative_live.get("url_tags"), url_tags),
        ("ad points at creative", (ad_live.get("creative") or {}).get("id"),
         creative["id"]),
    ]
    bad = 0
    for label, got, want in checks:
        ok = str(got) == str(want)
        bad += not ok
        print(f"  {'ok ' if ok else 'DIFF'}  {label:22} {got}")
        if not ok:
            print(f"        {'':22} expected: {want}")

    # Meta's per-feature creative enhancements, reported rather than assumed. The
    # single standard_enhancements opt-out was deprecated on 2026-08-28 and its
    # replacement names are documented only behind an internal URL, so the honest
    # thing is to print what Meta actually turned on and let a human decide. An
    # enhancement applied after rules/creative-generation.md's §10 QA gate voids the
    # sign-off that gate exists to give.
    dof = (creative_live.get("degrees_of_freedom_spec") or {}).get(
        "creative_features_spec") or {}
    opted_in = sorted(k for k, v in dof.items()
                      if str((v or {}).get("enroll_status", "")).upper() == "OPT_IN")
    if opted_in:
        print()
        print("CREATIVE ENHANCEMENTS Meta enabled by itself — the QA gate signed off on")
        print("the asset as built, and these change it after that sign-off:")
        for k in opted_in:
            print(f"  OPT_IN  {k}")
        print("  Turn them off per-ad in Ads Manager (Advantage+ creative) before enabling,")
        print("  or accept them deliberately. Names captured for a precise opt-out:")
        print(f"    {', '.join(opted_in)}")
    elif dof:
        print()
        print(f"creative enhancements: none opted in ({len(dof)} feature(s) reported)")

    print()
    if bad:
        print(f"{bad} field(s) differ from the plan. Fix in Ads Manager before enabling.")
        print("Meta rewrites targeting it considers suboptimal rather than rejecting it, so a\n"
              "diff on an audience field is a real change to what this test measures — not\n"
              "noise. Advantage Audience is the usual culprit.")
    else:
        print("Every field matches the plan.")
    print("Nothing is live: all objects are PAUSED. Enabling is a human action in Ads Manager.")
    print(f"\nWhen you have enabled it, close the loop:\n"
          f"  ad-agent log-setup {args.rec_id} --network meta \\\n"
          f"    --campaign-id {campaign['id']} \\\n"
          f"    --ad-set-id {adset['id']} \\\n"
          f"    --ad-id {ad['id']}")


def cmd_log_setup(args: argparse.Namespace, ledger: Ledger) -> None:
    _check_network(ledger.root / "rules", args.network)
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


def cmd_note(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = ledger.note(args.rec_id, text=args.text, kind=args.kind, today=_today())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    ledger.write_index()
    print(f"noted on {rec.rec_id} ({args.kind}) -> {rec.path}")


# A campaign verdict is evidence about a creative and evidence about a belief.
# rules/creative-generation.md sec 9 requires the first; the research loop needs
# the second. Both were written down as things someone should remember to do,
# which is how they stop happening around run four.
_VERDICT_TO_OUTCOME = {
    "working": "supported",
    "not-working": "contradicted",
    # A campaign can be unreadable for reasons that say nothing about the claim —
    # a campaign cap below the floor, broken tracking. That records the evidence
    # without moving the belief, which is the honest handling.
    "inconclusive": "inconclusive",
}


def _write_prompt_outcome(ledger: Ledger, rec, verdict: str, summary: str, today: str) -> str:
    """Append the verdict to the creative's prompt pack.

    rules/creative-generation.md sec 9: the reason the exact prompt text is kept is
    that a ranked prompt library accumulates across campaigns — which prompt
    patterns produce assets that earn taps, per persona. A prompt with no outcome
    attached taught nothing, so the audience goes in the entry too.
    """
    fm = rec.front_matter
    ref = str(fm.get("creative_ref") or "").strip("/")
    if not ref:
        return "no creative_ref on the record — prompt library not updated"
    prompts = ledger.root / ref / "prompts.md"
    if not prompts.exists():
        return f"{ref}/prompts.md does not exist — prompt library not updated"

    spec = fm.get("targeting")
    audience = targetingspec.describe(spec) if spec else str(fm.get("targeting_summary") or "")[:80]
    budget = fm.get("budget_cap_inr_per_day")
    cap = fm.get("campaign_daily_cap_inr")
    effective = min(budget, cap) if (budget is not None and cap is not None) else budget
    spend = f"Rs {float(effective):.0f}/day x {fm.get('duration_days')}d" if effective else "n/a"

    prompts.write_text(
        prompts.read_text(encoding="utf-8").rstrip()
        + f"\n\n## Outcome — {fm['rec_id']} ({today})\n\n"
        f"**{verdict}** — {summary.strip()}\n\n"
        f"- Ad set: `{fm.get('ad_set_name')}`\n"
        f"- Audience: {audience}\n"
        f"- Spend: {spend}\n",
        encoding="utf-8",
    )
    return f"{ref}/prompts.md"


def cmd_log_review(args: argparse.Namespace, ledger: Ledger) -> None:
    today = _today()
    try:
        rec = ledger.log_review(
            args.rec_id,
            verdict=args.verdict,
            summary=args.summary,
            review_log_path=args.review_log,
            today=today,
        )
    except ValueError as exc:
        _fail(exc)
    ledger.write_index()
    print(f"logged review for {rec.rec_id} -> verdict={args.verdict}")

    # --- back-edge 1: the prompt library ---
    print(f"  creative:  {_write_prompt_outcome(ledger, rec, args.verdict, args.summary, today)}")

    # --- back-edge 2: the beliefs this recommendation rested on ---
    r = _research(ledger)
    refs = list(args.learning or [])
    idea_id = rec.front_matter.get("from_idea")
    idea = r.idea_for_rec(rec.rec_id) if not idea_id else None
    if idea is not None:
        idea_id = idea.front_matter["id"]
    if idea_id:
        try:
            refs += [x for x in (r.find(idea_id).front_matter.get("learnings") or [])
                     if x not in refs]
        except KeyError:
            print(f"  warning:   {idea_id} is on the record but not in ideas/")

    if not refs:
        # Said out loud rather than passed over in silence: a verdict that updates
        # no belief means nothing in the library gets corrected by this result.
        print("  learnings: none — this record is not linked to any. Attach one with "
              f"`log-evidence <id> --from {rec.rec_id}` if it bears on a claim.")
        return

    outcome = _VERDICT_TO_OUTCOME[args.verdict]
    for ref in refs:
        try:
            updated = r.log_evidence(ref, outcome=outcome, text=args.summary,
                                     from_ref=rec.rec_id, today=today)
        except (researchmod.ResearchError, KeyError) as exc:
            print(f"  warning:   {ref} not updated: {exc}", file=sys.stderr)
        else:
            print(f"  learning:  {ref} -> {outcome} (now {updated.front_matter['status']})")


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


def _research(ledger: Ledger) -> researchmod.Research:
    return researchmod.Research(ledger.root)


def _research_fail(exc: Exception) -> None:
    print(f"error: {exc}", file=sys.stderr)
    raise SystemExit(2) from exc


def cmd_ingest(args: argparse.Namespace, ledger: Ledger) -> None:
    """Store a note exactly as it was brought in. Never edited afterwards."""
    text = Path(args.file).read_text(encoding="utf-8") if args.file else (args.text or "")
    try:
        rec = _research(ledger).ingest(title=args.title, text=text, source=args.source,
                                       slug=args.slug, today=_today())
    except (researchmod.ResearchError, OSError) as exc:
        _research_fail(exc)
    print(f"ingested {rec.front_matter['id']} -> {rec.path}")
    print("Nothing has been learned from it yet. Derive the claims with `ad-agent learn "
          f"--derived-from {rec.front_matter['id']} ...` — an ingested note with no learnings "
          "is an open loose end, and `ad-agent open` will keep saying so.")


def cmd_learn(args: argparse.Namespace, ledger: Ledger) -> None:
    r = _research(ledger)
    # Surface neighbours before writing. The CLI cannot judge whether two claims
    # are the same, but it can put them in front of whoever can.
    siblings = [x for x in r.learnings()
                if x.front_matter.get("subject") == args.subject
                and x.front_matter.get("status") not in ("retired",)]
    try:
        rec = r.learn(
            claim=args.claim, subject=args.subject, source=args.source,
            confidence=args.confidence, sample_n=args.sample_n, evidence=args.evidence,
            derived_from=args.derived_from, answers=args.answers, slug=args.slug,
            today=_today(),
        )
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    print(f"learned {rec.front_matter['id']} -> {rec.path}")
    if siblings:
        print(f"\n{len(siblings)} existing learning(s) on `{args.subject}` — if this restates one "
              "of them,\nthat is `log-evidence` on the original, not a second atom:")
        for x in siblings[:8]:
            fm = x.front_matter
            print(f"  {fm['id']}  [{fm.get('confidence')}/{fm.get('status')}] {fm.get('claim')}")


def cmd_log_evidence(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = _research(ledger).log_evidence(args.learning_id, outcome=args.outcome,
                                             text=args.text, from_ref=args.from_ref,
                                             today=_today())
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    print(f"{rec.front_matter['id']} -> status={rec.front_matter['status']}")


def cmd_reclassify(args: argparse.Namespace, ledger: Ledger) -> None:
    if not any((args.subject, args.source, args.confidence, args.sample_n)):
        print("error: nothing to reclassify — pass at least one of --subject, --source, "
              "--confidence, --sample-n", file=sys.stderr)
        raise SystemExit(2)
    try:
        rec, diff = _research(ledger).reclassify(
            args.learning_id, subject=args.subject, source=args.source,
            confidence=args.confidence, sample_n=args.sample_n, reason=args.reason,
            today=_today())
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    if not diff:
        print(f"{rec.front_matter['id']}: no change — every field already had that value")
        return
    print(f"reclassified {rec.front_matter['id']}")
    for field, (old, new) in sorted(diff.items()):
        print(f"  {field}: {old!r} -> {new!r}")


def cmd_promote(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = _research(ledger).promote(args.learning_id, rule_file=args.rule, today=_today())
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    print(f"promoted {rec.front_matter['id']} into {args.rule}")
    print("Remember the edit itself: this records that the rule now carries the claim, it does "
          "not write it. rules/ is what skills obey.")


def cmd_retire(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = _research(ledger).retire(args.learning_id, reason=args.reason, today=_today())
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    print(f"retired {rec.front_matter['id']}")


def cmd_question(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = _research(ledger).question(text=args.text, kind=args.kind, why=args.why,
                                         raised_by=args.raised_by, slug=args.slug,
                                         today=_today())
    except researchmod.ResearchError as exc:
        _research_fail(exc)
    print(f"asked {rec.front_matter['id']} -> {rec.path}")


def cmd_answer(args: argparse.Namespace, ledger: Ledger) -> None:
    try:
        rec = _research(ledger).answer(args.question_id, text=args.text, learning=args.learning,
                                       dropped=args.dropped, today=_today())
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    print(f"{rec.front_matter['id']} -> {rec.front_matter['status']}")


def cmd_idea(args: argparse.Namespace, ledger: Ledger) -> None:
    _check_network(ledger.root / "rules", args.network)
    if budgetrules.below_floor(args.est_daily):
        print(f"note: {budgetrules.floor_note(args.est_daily)}\n"
              "      An idea costed below the floor is proposing a system check, not a test.",
              file=sys.stderr)
    try:
        rec = _research(ledger).idea(
            title=args.title, verdict=args.verdict, network=args.network, persona=args.persona,
            est_daily_inr=args.est_daily, est_days=args.est_days, rationale=args.rationale,
            learnings=args.learning or [], blocked_on=args.blocked_on, slug=args.slug,
            today=_today(),
        )
    except (researchmod.ResearchError, KeyError) as exc:
        _research_fail(exc)
    fm = rec.front_matter
    print(f"{fm['verdict']} {fm['id']} -> {rec.path}  "
          f"(Rs {fm['est_daily_inr']:.0f}/day x {fm['est_days']}d = Rs {fm['est_total_inr']:.0f})")


def _age_days(today: _dt.date, when) -> int | None:
    try:
        return (today - _dt.date.fromisoformat(str(when))).days
    except (TypeError, ValueError):
        return None


def _effective_daily(fm: dict) -> tuple[float | None, str]:
    """The daily spend that actually binds, and how sure we are of it.

    `budget_cap_inr_per_day` is what was proposed. A campaign-level cap silently
    overrides it. Records pushed since 2026-08-26 carry the observed cap, so the
    effective figure is knowable; older ones do not, and this says so rather than
    quietly reporting the proposed number as though it were the real one.
    """
    proposed = fm.get("budget_cap_inr_per_day")
    if proposed is None:
        return None, "no budget on record"
    proposed = float(proposed)
    if not fm.get("campaign_caps_verified"):
        return proposed, "campaign cap never checked"
    cap = fm.get("campaign_daily_cap_inr")
    if cap is None:
        return proposed, "verified: no campaign cap"
    return min(proposed, float(cap)), f"campaign cap Rs {float(cap):.0f}/day binds"


def cmd_open(args: argparse.Namespace, ledger: Ledger) -> None:
    """Every loose end the ledger can see, in one place.

    The point is not a syntax reference — it is the answer to "where was I". A
    loop-engineered system's failure mode is not a wrong decision, it is a step
    that quietly never happened: a proposal never executed, a live ad set past its
    kill window with no verdict, a creative that cleared QA and was never used.
    None of that is visible in INDEX.md, which only lists records.

    Everything below is derived. This command holds no state of its own.
    """
    today = _dt.date.fromisoformat(_today())
    records = ledger.all()
    root = ledger.root
    sections: list[tuple[str, list[str]]] = []

    # --- proposals that never became anything ---
    rows = []
    for r in records:
        if r.status != "proposed":
            continue
        age = _age_days(today, r.front_matter.get("created"))
        stale = " STALE" if (age or 0) > 7 else ""
        rows.append(f"{r.rec_id}  proposed {age}d ago{stale}  "
                    f"-> snap-push, or abandon --reason")
    if rows:
        sections.append(("Proposed, never executed", rows))

    # --- live ad sets, against their own kill/double window ---
    due, running = [], []
    for r in records:
        if r.status != "live":
            continue
        fm = r.front_matter
        since = _age_days(today, fm.get("executed"))
        window = int(fm.get("duration_days") or budgetrules.KILL_WINDOW_DAYS_MAX)
        if since is None:
            running.append(f"{r.rec_id}  live, no execution date on record")
        elif since >= window:
            due.append(f"{r.rec_id}  live {since}d, window was {window}d  "
                       f"-> ad-audit, then log-review")
        else:
            running.append(f"{r.rec_id}  live {since}d of {window}d  "
                           f"-> review from {(_dt.date.fromisoformat(str(fm['executed'])) + _dt.timedelta(days=window)).isoformat()}")
    if due:
        sections.append(("Live and past the review window — no verdict yet", due))
    if running:
        sections.append(("Live, still inside the window", running))

    # --- funding, per rules/budget.md ---
    rows = []
    for r in records:
        if r.status not in ("proposed", "live"):
            continue
        eff, why = _effective_daily(r.front_matter)
        if eff is None:
            continue
        if budgetrules.below_floor(eff):
            rows.append(f"{r.rec_id}  Rs {eff:.0f}/day effective ({why})  "
                        f"-> below the Rs {budgetrules.MIN_VIABLE_DAILY_INR:.0f} floor; "
                        f"a weak read is inconclusive, not evidence")
        elif r.status == "live" and not r.front_matter.get("campaign_caps_verified"):
            # Only meaningful once something is live: a proposal has no parent
            # campaign to have been capped by yet.
            rows.append(f"{r.rec_id}  Rs {eff:.0f}/day proposed, but {why}  "
                        f"-> the real figure may be lower")
    if rows:
        sections.append(("Funding below the floor, or unverified", rows))

    # --- creative: cleared but unused, and used but unreviewed ---
    referenced = {str(r.front_matter.get("creative_ref") or "").strip("/") for r in records}
    uncleared, unused, no_backedge = [], [], []
    for r in records:
        ref = str(r.front_matter.get("creative_ref") or "").strip("/")
        if not ref or r.status in ("abandoned",):
            continue
        qa = root / ref / "qa.md"
        if not qa.exists() or "`pass`" not in qa.read_text(encoding="utf-8"):
            uncleared.append(f"{r.rec_id}  {ref}  -> no recorded QA pass "
                             f"(rules/creative-generation.md sec 10)")
    for d in sorted((root / "creatives").glob("*/")):
        ref = f"creatives/{d.name}"
        qa = d / "qa.md"
        if not qa.exists():
            continue
        if "`pass`" in qa.read_text(encoding="utf-8") and ref not in referenced:
            unused.append(f"{ref}  cleared QA, no record uses it  -> propose one, or say why not")
    for r in records:
        if r.status != "reviewed":
            continue
        ref = str(r.front_matter.get("creative_ref") or "").strip("/")
        prompts = root / ref / "prompts.md"
        if ref and prompts.exists():
            # Look for this record's own id, not for the word "verdict". A prompt
            # pack is shared across campaigns, so the question is whether *this*
            # result is recorded against it — and a keyword scan would be satisfied
            # by some other record's outcome, or by the word appearing in a QA note.
            text = prompts.read_text(encoding="utf-8")
            if r.front_matter["rec_id"] not in text:
                no_backedge.append(
                    f"{r.rec_id}  {ref}/prompts.md carries no verdict  "
                    f"-> creative-generation.md sec 9: a prompt with no outcome taught nothing")
    if uncleared:
        sections.append(("Creative not cleared by the QA gate", uncleared))
    if unused:
        sections.append(("Creative cleared but never used", unused))
    if no_backedge:
        sections.append(("Verdict never written back to the prompt library", no_backedge))

    # --- the research loop ---
    r = _research(ledger)

    rows = []
    for q in sorted(r.questions(), key=lambda x: str(x.front_matter.get("asked"))):
        fm = q.front_matter
        if fm.get("status") != "open":
            continue
        age = _age_days(today, fm.get("asked"))
        rows.append(f"{fm['id']}  [{fm.get('kind')}] asked {age}d ago  -> research it, "
                    f"then `answer` it")
    if rows:
        sections.append(("Open research questions", rows))

    rows = [f"{n.front_matter['id']}  ingested "
            f"{_age_days(today, n.front_matter.get('captured'))}d ago, nothing derived  "
            f"-> learn --derived-from {n.front_matter['id']}"
            for n in r.notes() if not n.front_matter.get("learnings")]
    if rows:
        # An ingested note nobody derived anything from is the research loop's own
        # version of a proposal never executed.
        sections.append(("Notes ingested, no learning derived", rows))

    stale, untested = [], []
    for lrn in r.learnings():
        fm = lrn.front_matter
        if fm.get("status") in ("retired", "promoted"):
            continue
        due = _age_days(today, fm.get("review_after"))
        if due is not None and due >= 0:
            last = _age_days(today, fm.get("last_confirmed"))
            stale.append(f"{fm['id']}  [{fm.get('source')}] last confirmed {last}d ago  "
                         f"-> reconfirm or retire")
        elif fm.get("status") == "open" and (_age_days(today, fm.get("created")) or 0) >= 14:
            # A grace period, so a claim recorded this week is not nagged about as
            # though it had been sitting untested for months. After two weeks, a
            # hypothesis nobody has designed a test for is a real loose end.
            untested.append(f"{fm['id']}  [{fm.get('confidence')}/{fm.get('source')}] "
                            f"{str(fm.get('claim'))[:70]}  -> never tested")
    if stale:
        sections.append(("Learnings past their review date", stale))
    if untested:
        sections.append(("Learnings never tested against a real outcome", untested))

    rows = []
    for idea in r.ideas():
        fm = idea.front_matter
        if fm.get("status") != "open":
            continue
        age = _age_days(today, fm.get("created"))
        if fm.get("verdict") == "recommend":
            rows.append(f"{fm['id']}  recommended {age}d ago, Rs {fm.get('est_total_inr'):.0f}  "
                        f"-> propose --from-idea {fm['id']}, or drop it")
    if rows:
        sections.append(("Ideas recommended but never proposed", rows))

    # A claim that turned out wrong is only half the problem; what still leans on it
    # is the other half. Anything citing it needs revisiting, and a contradicted claim
    # sitting in a rules file is the worst state in the system, because rules/ wins.
    cited: dict[str, list[str]] = {}
    for idea in r.ideas():
        for ref in idea.front_matter.get("learnings") or []:
            cited.setdefault(ref, []).append(idea.front_matter["id"])
    promoted, plain = [], []
    for lrn in r.learnings():
        fm = lrn.front_matter
        if fm.get("status") not in ("contradicted", "mixed"):
            continue
        leans = (fm.get("recs") or []) + cited.get(fm["id"], [])
        tail = f"  still cited by {', '.join(leans)}" if leans else ""
        if fm.get("promoted_to"):
            promoted.append(f"{fm['id']}  {fm['status']}, but still normative in "
                            f"{fm['promoted_to']}{tail}  -> fix the rule or retire the claim")
        else:
            plain.append(f"{fm['id']}  {fm['status']}{tail}  -> revise, retire, or narrow it")
    if promoted:
        sections.append(("Promoted rules whose evidence has since been contradicted", promoted))
    if plain:
        sections.append(("Learnings contradicted by a real outcome", plain))

    # --- report ---
    if sections:
        for title, rows in sections:
            print(f"{title} ({len(rows)})")
            for row in rows:
                print(f"  {row}")
            print()
    else:
        print("Nothing open in the ledger.\n")

    # Absence of a section is not evidence of nothing to do — say what this command
    # cannot yet see, so a quiet report is not mistaken for a finished loop.
    empty = [label for label, store in (("questions", r.questions_dir),
                                        ("notes", r.notes_dir),
                                        ("learnings", r.learnings_dir),
                                        ("ideas", r.ideas_dir)) if not store.exists()]
    if empty:
        print("No store yet for: " + ", ".join(empty) + ".")
        print("Nothing has been written to them, so an empty report above is not evidence")
        print("that there is nothing outstanding — only that nobody has recorded it here.")


COMMANDS_BEGIN = "<!-- BEGIN GENERATED: ad-agent commands -->"
COMMANDS_END = "<!-- END GENERATED: ad-agent commands -->"
COMMANDS_DOCS = ("README.md", "wiki-export/Command-Cheatsheet.md")


def _subcommands(parser: argparse.ArgumentParser) -> list[tuple[str, str, argparse.ArgumentParser]]:
    """(name, help, parser) for every subcommand, in the order they were declared.

    Reaches into argparse's private `_actions` / `_choices_actions`, deliberately:
    the alternative is a hand-maintained list of commands, which is the exact thing
    this function exists to stop anyone from keeping.
    """
    out = []
    for action in parser._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        helps = {ca.dest: (ca.help or "") for ca in action._choices_actions}
        for name, sub in action.choices.items():
            out.append((name, helps.get(name, ""), sub))
    return out


def _commands_markdown(parser: argparse.ArgumentParser) -> str:
    cmds = _subcommands(parser)
    lines = [
        "<!-- Generated by `ad-agent commands --write`. Do not hand-edit this block. -->",
        "",
        "| command | what it does |",
        "|---|---|",
    ]
    for name, help_text, _ in cmds:
        lines.append(f"| `{name}` | {help_text} |")
    lines.append("")
    for name, _, sub in cmds:
        usage = " ".join(sub.format_usage().replace("usage:", "", 1).split())
        lines += [f"#### `{name}`", "", "```", usage, "```", ""]
    return "\n".join(lines).rstrip()


def cmd_commands(args: argparse.Namespace, ledger: Ledger) -> None:
    """Print — or write — the command list, so no hand-maintained copy can drift.

    On 2026-08-26 both README.md and the wiki cheatsheet still said this agent
    never calls a Snap API, hours after it had created a live ad set through one,
    and neither listed `snap-push` at all. Three hand-kept copies of one list is
    why. The prose around each command stays hand-written — that is where the
    reasoning lives — but the list itself is generated from the parser.
    """
    parser = build_parser()
    block = _commands_markdown(parser)
    names = [n for n, _, _ in _subcommands(parser)]

    if args.check:
        # Drift runs both ways. The docs can fall behind the CLI (a command with no
        # written section), and a skill can run ahead of it (telling a session to
        # run something that does not exist, or that got renamed). The second is
        # worse: a wrong doc is confusing, a wrong instruction fails mid-task.
        import re as _re
        phantom = []
        for skill in sorted((ledger.root / ".claude" / "skills").glob("*/SKILL.md")):
            for token in _re.findall(r"ad-agent\s+([a-z][a-z-]*)",
                                     skill.read_text(encoding="utf-8")):
                if token not in names:
                    phantom.append(f"{skill.parent.name}: `ad-agent {token}` is not a command")

        missing_docs, undocumented = [], []
        for rel in COMMANDS_DOCS:
            path = ledger.root / rel
            if not path.exists():
                missing_docs.append(rel)
                continue
            text = path.read_text(encoding="utf-8")
            outside = text.split(COMMANDS_BEGIN)[0] + text.split(COMMANDS_END)[-1]
            for name in names:
                if f"ad-agent {name}" not in outside and rel.endswith("Command-Cheatsheet.md"):
                    undocumented.append(f"{rel}: `{name}` has no hand-written section")
        for row in missing_docs:
            print(f"missing: {row}", file=sys.stderr)
        for row in undocumented + sorted(set(phantom)):
            print(row, file=sys.stderr)
        if missing_docs or undocumented or phantom:
            raise SystemExit(1)
        skills = len(list((ledger.root / ".claude" / "skills").glob("*/SKILL.md")))
        print(f"ok — {len(names)} commands, all documented; "
              f"{skills} skills reference only real ones")
        return

    if not args.write:
        print(block)
        return

    for rel in COMMANDS_DOCS:
        path = ledger.root / rel
        text = path.read_text(encoding="utf-8")
        if COMMANDS_BEGIN not in text or COMMANDS_END not in text:
            print(f"error: {rel} has no generated block. Add these two markers where the\n"
                  f"command list should go:\n  {COMMANDS_BEGIN}\n  {COMMANDS_END}",
                  file=sys.stderr)
            raise SystemExit(2)
        head = text.split(COMMANDS_BEGIN)[0]
        tail = text.split(COMMANDS_END, 1)[1]
        path.write_text(f"{head}{COMMANDS_BEGIN}\n{block}\n{COMMANDS_END}{tail}",
                        encoding="utf-8")
        print(f"wrote {rel}")


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

    if args.network not in ("all", "other"):
        _check_network(Path(config["ledger"]["root"]) / "rules", args.network)

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
    sp.add_argument("--network", required=True, help=NETWORK_HELP)
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
    sp.add_argument(
        "--budget-cap", type=float, default=budgetrules.DEFAULT_DAILY_INR,
        help="INR per day (default: rules/budget.md's operating default, Rs 300 as of "
             "2026-08-28). Reads below the Rs 800-1,200 full-experiment threshold are "
             "directional — propose says so on the record; raise the cap for a test "
             "whose answer must be trusted")
    sp.add_argument("--duration-days", required=True, type=int)
    sp.add_argument("--brief", required=True, help="path to a markdown brief file")
    sp.add_argument("--from-idea", default=None,
                    help="idea id this came from; marks that idea proposed so it stops "
                         "showing as an open loose end")
    _add_targeting_flags(sp, required=True)
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
    sp.add_argument("--accept-campaign-cap", action="store_true",
                    help="create anyway when the parent campaign's cap would bind, as a "
                         "stated deviation rather than a surprise")
    sp.set_defaults(func=cmd_snap_push)

    sp = sub.add_parser(
        "meta-push",
        help="Create a proposed recommendation in Meta Ads Manager, PAUSED, then diff it back",
    )
    sp.add_argument("rec_id")
    sp.add_argument("--headline", default="A shortlist that means something.",
                    help="the link headline (Meta's `name` field), ~40 chars before truncation")
    sp.add_argument("--message", default="",
                    help="primary text above the image; required by Meta for a link ad")
    sp.add_argument("--cta", default="LEARN_MORE",
                    help="call-to-action button type, e.g. LEARN_MORE, SIGN_UP, DOWNLOAD")
    sp.add_argument("--dry-run", action="store_true",
                    help="print the plan and create nothing")
    sp.add_argument("--accept-campaign-cap", action="store_true",
                    help="create anyway when the parent campaign's cap would bind, as a "
                         "stated deviation rather than a surprise. Does NOT apply to a "
                         "campaign-budget-optimisation parent, which is refused outright")
    sp.set_defaults(func=cmd_meta_push)

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
    _add_targeting_flags(sp, required=False)
    sp.set_defaults(func=cmd_amend)

    sp = sub.add_parser("log-setup", help="Record the real IDs after setting the ad up by hand")
    sp.add_argument("rec_id")
    sp.add_argument("--network", required=True, help=NETWORK_HELP)
    sp.add_argument("--campaign-id", required=True)
    sp.add_argument("--ad-set-id", required=True)
    sp.add_argument("--ad-id", required=True)
    sp.add_argument("--deviated", default=None, help="what changed from the brief, if anything")
    sp.set_defaults(func=cmd_log_setup)

    sp = sub.add_parser(
        "note",
        help="Append a dated note to a record — for things that change mid-run",
    )
    sp.add_argument("rec_id")
    sp.add_argument("--text", required=True, help="what happened, and why it matters to the verdict")
    sp.add_argument("--kind", default="observation",
                    choices=list(Ledger.NOTE_KINDS),
                    help="budget/targeting/creative changes, an incident, or a plain observation")
    sp.set_defaults(func=cmd_note)

    sp = sub.add_parser("log-review", help="Record mode-6's verdict on a live recommendation")
    sp.add_argument("rec_id")
    sp.add_argument("--verdict", required=True, choices=["working", "not-working", "inconclusive"])
    sp.add_argument("--summary", required=True)
    sp.add_argument("--review-log", default=None, help="path to a markdown review-detail file")
    sp.add_argument("--learning", action="append", default=None,
                    help="learning id this verdict bears on, beyond any reached via the record's "
                         "idea; repeatable")
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

    # ---- the research loop -------------------------------------------------
    sp = sub.add_parser(
        "ingest",
        help="Store a note you brought in, verbatim and immutable, as provenance for learnings",
    )
    sp.add_argument("--title", required=True, help="what this note is about")
    sp.add_argument("--source", required=True, choices=list(researchmod.SOURCES))
    g = sp.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", default=None, help="path to the note")
    g.add_argument("--text", default=None, help="the note itself")
    sp.add_argument("--slug", default=None,
                    help="short id suffix; defaults to the first few words")
    sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser(
        "learn",
        help="Record one derived claim, with the source kind and confidence that make it citable",
    )
    sp.add_argument("--claim", required=True, help="one claim, stated plainly")
    sp.add_argument("--subject", required=True, choices=list(researchmod.SUBJECTS))
    sp.add_argument("--source", required=True, choices=list(researchmod.SOURCES),
                    help="only live-data and platform-doc may be `high` confidence")
    sp.add_argument("--confidence", required=True, choices=list(researchmod.CONFIDENCES))
    sp.add_argument("--sample-n", default=None, type=int,
                    help=f"required for live-data; below MIN_SAMPLE={researchmod.MIN_SAMPLE} "
                         "the claim can only be `low`")
    sp.add_argument("--evidence", required=True, help="what actually supports this, today")
    sp.add_argument("--derived-from", default=None, help="the note id this was derived from")
    sp.add_argument("--answers", default=None, help="question id this claim closes")
    sp.add_argument("--slug", default=None,
                    help="short id suffix; defaults to the first few words")
    sp.set_defaults(func=cmd_learn)

    sp = sub.add_parser(
        "log-evidence",
        help="Attach a dated outcome to a learning — the back-edge that lets it be corrected",
    )
    sp.add_argument("learning_id")
    sp.add_argument("--outcome", required=True, choices=list(researchmod.OUTCOMES))
    sp.add_argument("--text", required=True)
    sp.add_argument("--from", dest="from_ref", default=None,
                    help="rec_id whose verdict produced this, if any")
    sp.set_defaults(func=cmd_log_evidence)

    sp = sub.add_parser(
        "reclassify",
        help="Correct how a learning is filed — subject, source, confidence — not what it claims",
    )
    sp.add_argument("learning_id")
    sp.add_argument("--reason", required=True, help="why the original filing was wrong")
    sp.add_argument("--subject", default=None, choices=list(researchmod.SUBJECTS))
    sp.add_argument("--source", default=None, choices=list(researchmod.SOURCES))
    sp.add_argument("--confidence", default=None, choices=list(researchmod.CONFIDENCES))
    sp.add_argument("--sample-n", default=None, type=int)
    sp.set_defaults(func=cmd_reclassify)

    sp = sub.add_parser(
        "promote",
        help="Record that a learning has graduated into a rules file and is now normative",
    )
    sp.add_argument("learning_id")
    sp.add_argument("--rule", required=True, help="e.g. rules/targeting.md")
    sp.set_defaults(func=cmd_promote)

    sp = sub.add_parser("retire", help="Close out a learning that is no longer worth carrying")
    sp.add_argument("learning_id")
    sp.add_argument("--reason", required=True)
    sp.set_defaults(func=cmd_retire)

    sp = sub.add_parser(
        "question",
        help="Add an open research question to the queue that drives the next research pass",
    )
    sp.add_argument("--text", required=True)
    sp.add_argument("--kind", required=True, choices=list(researchmod.SUBJECTS))
    sp.add_argument("--why", required=True, help="why it matters — what decision it unblocks")
    sp.add_argument("--raised-by", default=None, help="rec_id, learning id or idea id, if any")
    sp.add_argument("--slug", default=None,
                    help="short id suffix; defaults to the first few words")
    sp.set_defaults(func=cmd_question)

    sp = sub.add_parser("answer", help="Close an open question, optionally naming what it taught")
    sp.add_argument("question_id")
    sp.add_argument("--text", required=True)
    sp.add_argument("--learning", default=None, help="the learning id this produced")
    sp.add_argument("--dropped", action="store_true",
                    help="close it as no longer worth answering, rather than as answered")
    sp.set_defaults(func=cmd_answer)

    sp = sub.add_parser(
        "idea",
        help="Record a recommend/hold idea with the spend it would take to test it",
    )
    sp.add_argument("--title", required=True)
    sp.add_argument("--verdict", required=True, choices=list(researchmod.IDEA_VERDICTS))
    sp.add_argument("--network", required=True, help=NETWORK_HELP)
    sp.add_argument("--persona", required=True, help="from rules/targeting.md")
    sp.add_argument("--est-daily", required=True, type=float, help="INR per day to test it")
    sp.add_argument("--est-days", required=True, type=int)
    sp.add_argument("--rationale", required=True)
    sp.add_argument("--learning", action="append", default=None,
                    help="learning id this rests on; repeatable")
    sp.add_argument("--blocked-on", default=None,
                    help="required for a hold: what would make it recommendable")
    sp.add_argument("--slug", default=None,
                    help="short id suffix; defaults to the first few words")
    sp.set_defaults(func=cmd_idea)

    sp = sub.add_parser(
        "open",
        help="Every loose end the ledger can see — start here when you come back to this repo",
    )
    sp.set_defaults(func=cmd_open)

    sp = sub.add_parser(
        "commands",
        help="Print the command list, or regenerate it in README and the wiki cheatsheet",
    )
    sp.add_argument("--write", action="store_true",
                    help="splice the list into README.md and wiki-export/Command-Cheatsheet.md")
    sp.add_argument("--check", action="store_true",
                    help="fail if a command has no hand-written section in the cheatsheet")
    sp.set_defaults(func=cmd_commands)

    sp = sub.add_parser(
        "fetch-analytics",
        help="Pull pocket-dating-coach's ad analytics via the authenticated internal endpoint",
    )
    sp.add_argument("--start", required=True, help="YYYY-MM-DD, IST day, inclusive")
    sp.add_argument("--end", required=True, help="YYYY-MM-DD, IST day, inclusive")
    sp.add_argument("--currency", default="INR", choices=["INR", "USD"])
    sp.add_argument("--network", default="all",
                    help="all, other, or a key from rules/networks.yaml")
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
