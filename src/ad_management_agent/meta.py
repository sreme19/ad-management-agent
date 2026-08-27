"""Meta Marketing API client.

The sibling of `snap.py`, built to the same terms. SPEC.md decisions #3 and #10 were
extended to Meta by the app owner on 2026-08-27, and that extension is explicit that
the permission is to build *this shape* — not to reach the API by any means:

  * Everything is created PAUSED. Nothing here can start spending money.
  * There is no enable/resume/activate call anywhere in this file, and none should be
    added without the app owner saying so explicitly.
  * The rule is enforced at the single choke point every request passes through
    (`_call`), so a method added later cannot skip a check it never knew about.
  * Every object is read back and diffed against what was asked for, because "the
    POST returned 200" is not evidence the ad set targets who you think it targets.

**Three things here deliberately do NOT mirror snap.py, because Meta differs.** Each
is a place where copying the Snap shape would have produced a hole or a wrong number:

1. **An update is a POST, not a PUT.** Meta has no PUT: creating is `POST
   /act_X/campaigns` and updating is `POST /{campaign_id}`. `snap.py` keys its budget
   guard off the method (`BUDGET_KEYS` + `method in ("PUT","PATCH")`), which on Meta
   would classify every budget change as a creation and wave it through. So the guard
   here keys off the **path shape** instead — a create posts to a known collection, an
   update posts to a bare object id. See `_is_create`.

2. **Meta's update is a partial patch, not a full replace.** Snap's is a replace, which
   is why `_safety_violations` there needs an `unchanged` echo exemption: omitting a
   budget field *deletes* it, so a pause had to send the budget back unchanged, and on
   2026-08-26 at 17:24 UTC an omission wiped a campaign's daily cap. Meta has no such
   trap — a field left out is a field left alone. That makes the guard here strictly
   *stronger*: any budget key on an update is refused outright, with no echo escape
   hatch, because there is never a legitimate reason to send one.

3. **Money is in minor units, not micro.** Snap is micro (1 INR = 1_000_000). Meta is
   the account currency's minor unit (1 INR = 100 paise). Getting this wrong is a
   10,000x budget error in the direction that spends money, so `MetaClient` refuses to
   create anything until it has read the ad account's own `currency` and found INR.
"""
from __future__ import annotations

import json
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# Pinned deliberately. Marketing API versions expire — v24.0 dies 2026-10-06 — and
# Meta began auto-upgrading unpinned callers on 2026-07-29. An auto-upgrade that
# silently changes a payload's meaning is not something to discover through a live
# ad account, so the version is a constant here and bumping it is a code change.
API_VERSION = "v26.0"
API = f"https://graph.facebook.com/{API_VERSION}"

# 1 INR = 100 paise. NOT snap.py's MICRO — see the module docstring, point 3.
MINOR = 100


class MetaError(RuntimeError):
    pass


class MetaSafetyError(MetaError):
    """An outbound request would have broken the paused-only rule. Never catch this."""


# Meta's own enabling value is ACTIVE; the rest are the near-synonyms a future method
# might reach for. PAUSED is deliberately absent: pausing stops spend, and stopping
# spend is always safe.
ENABLING_STATUSES = {"ACTIVE", "RUNNING", "ENABLED", "ON", "LIVE"}

# Meta deletes and archives through the same `status` field it enables through, so the
# one guard covers both hazards. These are refused for a different reason than
# ENABLING_STATUSES — not because they spend money, but because they destroy or hide
# the object a ledger record points at. `ad-audit` has to be able to read a pushed ad
# set months later to close its loop, and an ARCHIVED object drops out of Meta's
# default listings. Neither is this agent's call to make.
DESTRUCTIVE_STATUSES = {"DELETED", "ARCHIVED"}

# Changing any of these on an object that already exists is a budget change, which
# decision #3 forbids outright. Setting them at creation time is how an ad set gets a
# budget at all, so the check is scoped to updates rather than to the key alone.
BUDGET_KEYS = {
    "daily_budget",
    "lifetime_budget",
    "spend_cap",
    "bid_amount",
    "lifetime_spend_cap",
    "daily_spend_cap",
    "campaign_daily_budget",
    "campaign_lifetime_budget",
}

# A POST whose final path segment is one of these is creating a new object under a
# parent. A POST to anything else — i.e. to a bare object id — is an update. This is
# the load-bearing distinction on Meta; see the module docstring, point 1.
COLLECTIONS = {
    "campaigns",
    "adsets",
    "ads",
    "adcreatives",
    "adimages",
    "advideos",
}


def _is_create(method: str, path: str) -> bool:
    """True if this request creates a new object rather than modifying one.

    Conservative by construction: anything not recognisably a create is treated as an
    update, which is the stricter classification. A new collection endpoint added to
    Meta and not listed in COLLECTIONS therefore fails closed — its creates get
    refused for carrying a budget — rather than failing open and letting a budget
    change through as if it were a creation.
    """
    if method.upper() != "POST":
        return False
    segments = [s for s in path.split("?")[0].split("/") if s]
    return bool(segments) and segments[-1] in COLLECTIONS


def _safety_violations(method: str, path: str, payload: object,
                       field: str = "") -> list[str]:
    """Every reason this outbound payload must not be sent. Empty means safe.

    Walks the whole structure rather than checking the top level, because Meta nests
    the interesting fields — `object_story_spec.link_data`, `targeting.geo_locations`
    — and a `status` two levels down is still a status.

    Unlike snap.py's equivalent there is no `unchanged` echo exemption, and there
    should not be one: Meta's update is a patch, so a budget key on an update is
    always an attempt to change a budget, never the price of keeping one.
    """
    found: list[str] = []
    creating = _is_create(method, path)

    if isinstance(payload, dict):
        for key, value in payload.items():
            here = f"{field}.{key}" if field else key
            if key in ("status", "configured_status") and isinstance(value, str):
                upper = value.upper()
                if upper in ENABLING_STATUSES:
                    found.append(f"{here} = {value!r} would enable an object")
                elif upper in DESTRUCTIVE_STATUSES:
                    found.append(
                        f"{here} = {value!r} would destroy or hide an object the ledger "
                        f"may point at"
                    )
            if key in BUDGET_KEYS and not creating:
                found.append(
                    f"{here} on {method.upper()} {path} would change an existing budget"
                )
            found += _safety_violations(method, path, value, here)
    elif isinstance(payload, list):
        for i, item in enumerate(payload):
            found += _safety_violations(method, path, item, f"{field}[{i}]")
    return found


class MetaClient:
    def __init__(self, cfg: dict):
        missing = [k for k in ("access_token", "ad_account_id", "page_id")
                   if not (cfg or {}).get(k)]
        if missing:
            raise MetaError(
                "config.local.yaml is missing meta." + ", meta.".join(missing) + ".\n"
                "See config.example.yaml for the expected block. The token is the "
                "system-user token for riteangle-api (SPEC.md decision #10, as amended "
                "2026-08-27) — it does not expire, and Meta shows it only once."
            )
        self.cfg = cfg
        self._currency: str | None = None

    @property
    def account_path(self) -> str:
        """Meta's ad account ids are prefixed `act_`; the config may hold either form."""
        raw = str(self.cfg["ad_account_id"])
        return raw if raw.startswith("act_") else f"act_{raw}"

    # ---- transport -------------------------------------------------------
    def _call(self, method: str, path: str, payload: dict | None = None) -> dict:
        # The paused-only rule, enforced at the one place every request passes through.
        #
        # There is no override flag, and there is not meant to be one. Prose in a
        # docstring is not carefulness that survives the next method someone adds;
        # this is, because a new call cannot forget a check it never had to remember.
        if payload is not None:
            violations = _safety_violations(method, path, payload)
            if violations:
                raise MetaSafetyError(
                    f"REFUSED: {method} {path} would break the paused-only rule.\n"
                    + "\n".join(f"  - {v}" for v in violations)
                    + "\n\nSee SPEC.md decision #3 (extended to Meta 2026-08-27). Enabling an ad\n"
                    "set, raising the budget of a live one, and deleting anything are human\n"
                    "actions in Ads Manager, deliberately. If this refusal is wrong, the fix is\n"
                    "the app owner amending that decision — not this check."
                )

        data = urllib.parse.urlencode(
            {k: (json.dumps(v) if isinstance(v, (dict, list)) else v)
             for k, v in (payload or {}).items()}
        ).encode() if payload is not None else None

        # The token goes in a header, never in the query string. Meta's own access
        # logs, any proxy, and the browser history of anyone who pastes a URL all
        # capture query parameters; a non-expiring system-user token in one of those
        # is a credential leak with no rotation story, because there is no refresh.
        req = urllib.request.Request(
            f"{API}{path}", data=data, method=method.upper(),
            headers={"Authorization": f"Bearer {self.cfg['access_token']}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:800]
            hint = ""
            if e.code in (400, 401, 403) and "OAuth" in detail:
                hint = (
                    "\n\nA system-user token does not expire, so an auth failure here is more "
                    "likely a missing asset assignment than a stale token: check that "
                    "riteangle-api is assigned this ad account with Manage campaigns, and that "
                    "the riteangle app is installed on it."
                )
            raise MetaError(f"{method} {path} -> HTTP {e.code}\n{detail}{hint}") from e

    def get(self, path: str, fields: str | None = None) -> dict:
        return self._call("GET", path + (f"?fields={fields}" if fields else ""))

    def post(self, path: str, payload: dict) -> dict:
        return self._call("POST", path, payload)

    # ---- account ---------------------------------------------------------
    @property
    def currency(self) -> str:
        if self._currency is None:
            self._currency = self.get(f"/{self.account_path}", fields="currency").get("currency")
        return self._currency or ""

    def require_inr(self) -> None:
        """Refuse to convert a rupee figure into minor units for a non-INR account.

        Every budget in this repo is INR: rules/budget.md's floor is Rs 800-1,200/day
        against a Rs 50,000/month envelope, and the ledger's field is literally
        `budget_cap_inr_per_day`. If this account settles in anything else, the minor
        unit is not paise and the number sent would be wrong by whatever the FX rate
        is — in the direction that spends money. Cheaper to refuse than to discover.
        """
        cur = self.currency
        if cur != "INR":
            raise MetaError(
                f"ad account {self.account_path} settles in {cur or 'an unknown currency'}, "
                "not INR.\nEvery budget in this repo is rupees (rules/budget.md, and the "
                "ledger's own\nbudget_cap_inr_per_day), so the minor-unit conversion here would "
                "be wrong.\nRefusing rather than guessing an FX rate."
            )

    # ---- campaign --------------------------------------------------------
    def find_campaign(self, name: str) -> dict | None:
        """Exact-name lookup that refuses to guess.

        The same rule as snap.py's, for the same reason and with more evidence behind
        it on this network: this account already holds two Pages both named
        `Riteangle` (one deactivated), and six campaigns whose names collide on
        prefix. Hanging an ad set off the wrong parent is invisible until the numbers
        make no sense, so an ambiguous name is an error, never a pick-the-first.
        """
        res = self.get(f"/{self.account_path}/campaigns", fields="id,name,status")
        hits = [c for c in res.get("data", []) if c.get("name") == name]
        if len(hits) > 1:
            ids = ", ".join(h["id"] for h in hits)
            raise MetaError(
                f"{len(hits)} campaigns are named {name!r} ({ids}).\n"
                "Refusing to guess which one to use — rename or delete the duplicate in Ads "
                "Manager first. See rules/naming.md."
            )
        return hits[0] if hits else None

    def campaign_caps(self, campaign_id: str) -> dict:
        """Read a campaign's own budget caps, in INR. Either may be None.

        Mirrors snap.py.campaign_caps, and exists for the same incident: on
        2026-08-26 WOMEN_18-22_CASUAL_LPV was created with an ad squad at Rs
        1,000/day under a campaign capped at Rs 300/day, which put the live test
        below rules/budget.md's floor and made its read inconclusive before a rupee
        was spent. Nothing in the push looked at the parent, so nothing caught it.

        Meta has the same trap with an extra wrinkle: a campaign using
        campaign-budget optimisation holds the budget itself, and an ad-set budget
        under it is ignored outright rather than merely capped. That is reported too.
        """
        c = self.get(
            f"/{campaign_id}",
            fields="id,name,daily_budget,lifetime_budget,spend_cap,budget_remaining",
        )
        def inr(key):
            raw = c.get(key)
            return float(raw) / MINOR if raw not in (None, "", "0") else None
        return {
            "daily_inr": inr("daily_budget"),
            "lifetime_inr": inr("lifetime_budget"),
            "spend_cap_inr": inr("spend_cap"),
            # A campaign-level daily or lifetime budget on Meta means CBO is on.
            "campaign_budget_optimization": bool(
                c.get("daily_budget") or c.get("lifetime_budget")
            ),
        }

    def create_campaign(self, name: str, objective: str = "OUTCOME_TRAFFIC") -> dict:
        """Create the campaign, PAUSED.

        `special_ad_categories` is required by Meta and is deliberately sent empty.
        Dating is not one of Meta's special ad categories — those are credit,
        employment, housing, elections/politics and gambling — so claiming one would
        be a false declaration. Note separately that Meta requires written permission
        to advertise dating at all; that is an account-level approval, not a field.
        """
        return self.post(f"/{self.account_path}/campaigns", {
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": [],
            "buying_type": "AUCTION",
        })

    # ---- stopping spend --------------------------------------------------
    def pause_campaign(self, campaign_id: str) -> dict:
        """Set a live campaign to PAUSED, stopping everything beneath it.

        This is the ONE state change this module makes, and the asymmetry is the
        point: it can stop money, and it can never start it. There is no resume,
        enable or activate anywhere here, so the worst this method can do is halt
        spend a human chose to begin.

        Simpler than the Snap equivalent, and the difference is instructive: Snap's
        update is a full replace, so pausing there has to echo every existing field
        back or it deletes them. Meta's update is a patch, so this sends `status`
        alone — which is also why the guard above can refuse budget keys on updates
        with no exemption. Reads back and refuses to claim success on the API's word.
        """
        self.post(f"/{campaign_id}", {"status": "PAUSED"})
        after = self.get(f"/{campaign_id}", fields="id,name,status,effective_status")
        if after.get("status") != "PAUSED":
            raise MetaError(
                f"asked Meta to pause {after.get('name', campaign_id)} but it still reads "
                f"{after.get('status')!r}. Pause it by hand in Ads Manager."
            )
        return after

    # ---- ad set ----------------------------------------------------------
    def create_adset(self, *, name, campaign_id, targeting, daily_budget_inr,
                     start_time, end_time, pixel_id=None) -> dict:
        """Create the ad set, PAUSED, optimising for landing-page views.

        **`pixel_id` is deliberately optional here, unlike snap.py's equivalent, and
        `promoted_object` is deliberately not sent.** This was wrong in the first cut of
        this module: it mirrored Snap's hard requirement and asserted that "Meta has no
        fallback, no pixel means no signal at all". Checking the account on 2026-08-27
        showed the opposite. Its own live LANDING_PAGE_VIEWS ad set,
        `FB_W_20-25_ID_Romantic`, binds no dataset at the ad-set level and has Website
        events unchecked, and the ad under it reported 36 landing-page views anyway.
        Meta's Tracking panel says the ad account's *default* conversion dataset is used
        unless told otherwise, so the binding is at the account level, not here.

        `promoted_object` carrying a pixel is required for OFFSITE_CONVERSIONS, which is
        a different optimisation goal than this one. Sending it on an OUTCOME_TRAFFIC ad
        set optimising for LANDING_PAGE_VIEWS risks a rejection for a field the account's
        own working ad set does not set — so this follows the account's observed
        convention, which is the same rule snap.py's pixel requirement came from, applied
        honestly to a network whose convention turned out to be the other way.

        A conversions-objective ad set WOULD need `promoted_object`. That is a new code
        path when someone builds it, not a flag on this one.
        """
        self.require_inr()
        return self.post(f"/{campaign_id}/adsets", {
            "name": name,
            "campaign_id": campaign_id,
            "status": "PAUSED",
            "targeting": targeting,
            "optimization_goal": "LANDING_PAGE_VIEWS",
            "billing_event": "IMPRESSIONS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            # round() before sending, not truncation: Rs 999.999/day is a rounding
            # artefact of a rupee figure, and int() would floor it to 99999 paise and
            # put the ad set a paisa under rules/budget.md's floor.
            "daily_budget": round(daily_budget_inr * MINOR),
            "destination_type": "WEBSITE",
            "start_time": start_time,
            "end_time": end_time,
        })

    # ---- media + creative + ad -------------------------------------------
    def upload_image(self, path: Path) -> str:
        """Upload an image and return its `image_hash`.

        Meta identifies ad images by a content hash rather than by an id, and the
        response keys the result under the *filename* — so the hash has to be dug out
        of a dict whose only key is whatever the file happened to be called. Pulling
        the single value rather than looking up `path.name` avoids depending on Meta
        echoing the filename back byte-for-byte.
        """
        boundary = uuid.uuid4().hex
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body = b"".join([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="filename"; filename="{path.name}"\r\n'.encode(),
            f"Content-Type: {ctype}\r\n\r\n".encode(),
            path.read_bytes(), b"\r\n", f"--{boundary}--\r\n".encode(),
        ])
        req = urllib.request.Request(
            f"{API}/{self.account_path}/adimages", data=body, method="POST",
            headers={"Authorization": f"Bearer {self.cfg['access_token']}",
                     "content-type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                res = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise MetaError(f"image upload -> HTTP {e.code}\n{e.read().decode()[:500]}") from e
        images = res.get("images") or {}
        if not images:
            raise MetaError(f"image upload returned no hash: {json.dumps(res)[:300]}")
        entry = next(iter(images.values()))
        if not entry.get("hash"):
            raise MetaError(f"image upload returned no hash: {json.dumps(res)[:300]}")
        return entry["hash"]

    def create_creative(self, *, name, image_hash, headline, message, url,
                        call_to_action: str = "LEARN_MORE") -> dict:
        """Create the ad creative, bound to the Page identity.

        The Page is not optional on Meta and has no Snap equivalent: a Snap ad renders
        under a `profile_id`, while a Meta ad IS a post by a Page. That makes the
        active `Riteangle` Page (1309735922215645) load-bearing, and makes the
        deactivated duplicate of the same name a live hazard — which is why the page id
        comes from config rather than from a name lookup.
        """
        return self.post(f"/{self.account_path}/adcreatives", {
            "name": name,
            "object_story_spec": {
                "page_id": str(self.cfg["page_id"]),
                "link_data": {
                    "image_hash": image_hash,
                    "link": url,
                    "name": headline,
                    "message": message,
                    "call_to_action": {"type": call_to_action},
                },
            },
            "degrees_of_freedom_spec": {
                # Meta will otherwise "improve" the creative on its own — recropping,
                # restyling, generating variants. rules/creative-generation.md's QA gate
                # signs off on a specific 1080x1920 asset with specific type on it; an
                # enhancement applied after that gate makes the sign-off meaningless.
                "creative_features_spec": {
                    "standard_enhancements": {"enroll_status": "OPT_OUT"}
                }
            },
        })

    def create_ad(self, *, name, adset_id, creative_id) -> dict:
        return self.post(f"/{self.account_path}/ads", {
            "name": name,
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status": "PAUSED",
        })

    def set_ad_url_tags(self, ad_id: str, url_tags: str) -> dict:
        """Write the tracking parameters onto the ad once its real id exists.

        rules/tracking.md requires the ad id to reach the analytics, and on Meta the
        joining parameter is `utm_content` where Snap uses `utm_id` (per
        traffic-quality.ts). The ad does not exist when the creative is created, so
        the creative's link cannot carry it.

        Ads Manager solves this with a {{ad.id}} macro — the same class of macro whose
        silent non-resolution cost a week of unattributable spend on 2026-08-21. Here
        the id is a known fact by the time this runs, so the value is written literally
        and there is no macro left to fail. This is an update (POST to a bare id), and
        it passes the guard because it carries no budget key and no status.
        """
        return self.post(f"/{ad_id}", {"url_tags": url_tags})
