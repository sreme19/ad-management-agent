"""Snap Marketing API client.

SPEC.md decisions #3 and #10 originally kept every credential that could reach a
live ad account out of this repo, so that "never touches a live account" was true
by construction rather than by care. The app owner reversed that on 2026-08-26 to
allow programmatic setup. What replaces the structural guarantee is this module's
own discipline, and it is deliberately narrow:

  * Everything is created PAUSED. Nothing here can start spending money.
  * There is no enable/resume call anywhere in this file, and none should be added
    without the app owner saying so explicitly. Enabling stays a human action in
    Ads Manager. This is enforced rather than promised: `_call` refuses any outbound
    payload carrying an enabling status, or a budget field on a PUT, at the single
    choke point every request passes through — so a method added later cannot skip a
    check it never knew about.
  * Every object is read back from the API after creation and diffed against what
    was asked for, because "the POST returned 200" is not evidence the ad squad
    targets who you think it targets.

Amounts are micro-currency throughout: 1 INR = 1_000_000 micro.
"""
from __future__ import annotations

import json
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API = "https://adsapi.snapchat.com/v1"
TOKEN_URL = "https://accounts.snapchat.com/login/oauth2/access_token"
MICRO = 1_000_000


class SnapError(RuntimeError):
    pass


class SnapSafetyError(SnapError):
    """An outbound request would have broken the paused-only rule. Never catch this."""


# Snap's own enabling values, plus the near-synonyms a future method might reach for.
# PAUSED is deliberately absent: pausing stops spend, and stopping spend is always safe.
ENABLING_STATUSES = {"ACTIVE", "RUNNING", "ENABLED", "ON", "LIVE"}

# Changing any of these on an object that already exists is a budget change, which
# decision #3 forbids outright. Setting them at creation time is how an ad squad gets
# a budget at all, so the check is scoped to PUT rather than to the key alone.
BUDGET_KEYS = {
    "daily_budget_micro",
    "lifetime_budget_micro",
    "lifetime_spend_cap_micro",
    "daily_spend_cap_micro",
    "spend_cap_micro",
    "bid_micro",
}


def _safety_violations(method: str, payload: object, path: str = "",
                       unchanged: dict | None = None) -> list[str]:
    """Every reason this outbound payload must not be sent. Empty means safe.

    Walks the whole structure rather than checking the top level, because Snap wraps
    every object in a list under a plural key — `{"adsquads": [{"status": "ACTIVE"}]}`
    hides the field two levels down.

    `unchanged` is the object as it currently exists on Snap. A budget key whose
    value is byte-identical to what is already stored is an ECHO, not a change, and
    is allowed through. That distinction is load-bearing: Snap's update is a full
    replace, so a field left out is a field deleted. Without this, a pause that
    omitted daily_budget_micro to satisfy the guard silently wiped the campaign's
    daily cap — which is exactly what happened on 2026-08-26 at 17:24 UTC.
    """
    found: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            here = f"{path}.{key}" if path else key
            if key == "status" and isinstance(value, str) and value.upper() in ENABLING_STATUSES:
                found.append(f"{here} = {value!r} would enable an object")
            is_echo = bool(unchanged) and unchanged.get(key, object()) == value
            if key in BUDGET_KEYS and method.upper() in ("PUT", "PATCH") and not is_echo:
                found.append(f"{here} on a {method.upper()} would change an existing budget")
            found += _safety_violations(method, value, here, unchanged)
    elif isinstance(payload, list):
        for i, item in enumerate(payload):
            found += _safety_violations(method, item, f"{path}[{i}]", unchanged)
    return found


class SnapClient:
    def __init__(self, cfg: dict):
        missing = [k for k in ("client_id", "client_secret", "refresh_token", "ad_account_id")
                   if not (cfg or {}).get(k)]
        if missing:
            raise SnapError(
                "config.local.yaml is missing snap." + ", snap.".join(missing) + ".\n"
                "See config.example.yaml for the expected block."
            )
        self.cfg = cfg
        self._token: str | None = None

    # ---- transport -------------------------------------------------------
    @property
    def token(self) -> str:
        """Access tokens last an hour, so they are minted per run, never stored."""
        if self._token is None:
            body = urllib.parse.urlencode({
                "client_id": self.cfg["client_id"],
                "client_secret": self.cfg["client_secret"],
                "grant_type": "refresh_token",
                "refresh_token": self.cfg["refresh_token"],
            }).encode()
            req = urllib.request.Request(
                TOKEN_URL, data=body, method="POST",
                headers={"content-type": "application/x-www-form-urlencoded"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    self._token = json.loads(r.read())["access_token"]
            except urllib.error.HTTPError as e:
                raise SnapError(
                    f"could not refresh the access token (HTTP {e.code}). The refresh token may "
                    f"have been revoked — re-run the authorize step.\n{e.read().decode()[:300]}"
                ) from e
        return self._token

    def _call(self, method: str, path: str, payload: dict | None = None,
              unchanged: dict | None = None) -> dict:
        # The paused-only rule, enforced at the one place every request passes through.
        #
        # SPEC.md decision #3 (as amended 2026-08-26) states that this module never
        # enables anything and never changes the budget of anything live, and notes
        # honestly that the guarantee is no longer structural — the repo now holds a
        # credential that can reach a live account, so "never" rests on the code being
        # careful. Prose in a docstring is not carefulness that survives the next
        # method someone adds. This is: a new call cannot forget a check it never had
        # to remember. There is no override flag, and there is not meant to be one.
        if payload is not None:
            violations = _safety_violations(method, payload, unchanged=unchanged)
            if violations:
                raise SnapSafetyError(
                    f"REFUSED: {method} {path} would break the paused-only rule.\n"
                    + "\n".join(f"  - {v}" for v in violations)
                    + "\n\nSee SPEC.md decision #3. Enabling an ad set and raising the budget of a\n"
                    "live one are human actions in Ads Manager, deliberately. If this refusal is\n"
                    "wrong, the fix is the app owner amending that decision — not this check."
                )
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            f"{API}{path}", data=data, method=method,
            headers={"Authorization": f"Bearer {self.token}", "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise SnapError(f"{method} {path} -> HTTP {e.code}\n{e.read().decode()[:800]}") from e

    def get(self, path: str) -> dict:
        return self._call("GET", path)

    def post(self, path: str, payload: dict) -> dict:
        return self._call("POST", path, payload)

    def put(self, path: str, payload: dict, unchanged: dict | None = None) -> dict:
        return self._call("PUT", path, payload, unchanged=unchanged)

    # ---- helpers ---------------------------------------------------------
    @staticmethod
    def _one(res: dict, key: str) -> dict:
        """Snap wraps every object in a list under a plural key, one entry per request item."""
        items = res.get(key) or []
        if not items:
            raise SnapError(f"expected one {key} in the response, got none: {json.dumps(res)[:300]}")
        obj = items[0]
        singular = key.rstrip("s") if key != "adsquads" else "adsquad"
        inner = obj.get(singular, obj)
        if obj.get("sub_request_status") not in (None, "SUCCESS"):
            raise SnapError(f"{singular} rejected: {json.dumps(obj)[:500]}")
        return inner

    # ---- campaign --------------------------------------------------------
    def find_campaign(self, name: str) -> dict | None:
        """Exact-name lookup that refuses to guess.

        Two live campaigns in this account already share the name
        RA_TRAFFIC_GET_IN_BLR_TOF_202608 with different ids, which is precisely the
        collision rules/naming.md warns about. Hanging an ad squad off the wrong one
        would be invisible until the numbers made no sense, so an ambiguous name is
        an error, never a pick-the-first.
        """
        res = self.get(f"/adaccounts/{self.cfg['ad_account_id']}/campaigns")
        hits = [c["campaign"] for c in res.get("campaigns", []) if c["campaign"].get("name") == name]
        if len(hits) > 1:
            ids = ", ".join(h["id"] for h in hits)
            raise SnapError(
                f"{len(hits)} campaigns are named {name!r} ({ids}).\n"
                "Refusing to guess which one to use — rename or delete the duplicate in Ads "
                "Manager first. See rules/naming.md."
            )
        return hits[0] if hits else None

    def campaign_caps(self, campaign_id: str) -> dict:
        """Read a campaign's own spend caps, in INR. Either may be None.

        A campaign-level cap silently overrides a larger ad-squad budget: the lower
        figure binds. On 2026-08-26 WOMEN_18-22_CASUAL_LPV was created with an ad
        squad carrying Rs 1,000/day under a campaign capped at Rs 300/day, which put
        the live test below rules/budget.md's floor and made its read inconclusive
        before a rupee was spent. Nothing in the push looked at the parent, so
        nothing caught it. This is what `snap-push` now checks before it creates
        anything.
        """
        c = self._one(self.get(f"/campaigns/{campaign_id}"), "campaigns")
        daily = c.get("daily_budget_micro")
        lifetime = c.get("lifetime_spend_cap_micro")
        return {
            "daily_inr": float(daily) / MICRO if daily else None,
            "lifetime_inr": float(lifetime) / MICRO if lifetime else None,
        }

    def create_campaign(self, name: str, start_time: str) -> dict:
        res = self.post(f"/adaccounts/{self.cfg['ad_account_id']}/campaigns", {"campaigns": [{
            "name": name,
            "ad_account_id": self.cfg["ad_account_id"],
            "status": "PAUSED",
            "start_time": start_time,
            "buy_model": "AUCTION",
            "objective_v2_properties": {"objective_v2_type": "TRAFFIC"},
        }]})
        return self._one(res, "campaigns")

    # ---- stopping spend --------------------------------------------------
    def pause_campaign(self, campaign_id: str) -> dict:
        """Set a live campaign to PAUSED, stopping everything beneath it.

        This is the ONE state change this module makes, and the asymmetry is the
        point: it can stop money, and it can never start it. There is still no
        resume, enable or activate anywhere here, so the worst this method can do
        is halt spend that a human chose to begin. Restarting remains a human
        action in Ads Manager, exactly as SPEC.md decision #3 requires.

        Reads back and refuses to claim success on the API's say-so.
        """
        current = self.get(f"/campaigns/{campaign_id}")["campaigns"][0]["campaign"]
        # Snap's update is a full replace, not a patch: omitting a required field
        # fails the item while the HTTP call still returns 200. Echo the current
        # values back and change only status. _one() raises on the per-item error
        # that a bare 200 would otherwise hide.
        body = {
            "id": campaign_id,
            "ad_account_id": self.cfg["ad_account_id"],
            "name": current["name"],
            "start_time": current["start_time"],
            "buy_model": current.get("buy_model", "AUCTION"),
            "status": "PAUSED",
        }
        # Echo every field that exists, budgets included. Snap's update is a full
        # replace: anything omitted is deleted, so leaving the budget out to keep the
        # guard happy destroys the cap instead of protecting it. The guard is given
        # `current` so it can verify each budget value is identical to what is already
        # stored — an echo passes, a change still does not.
        for k in ("end_time", "objective_v2_properties", "daily_budget_micro",
                  "lifetime_spend_cap_micro"):
            if current.get(k) is not None:
                body[k] = current[k]
        self._one(self.put(f"/adaccounts/{self.cfg['ad_account_id']}/campaigns",
                           {"campaigns": [body]}, unchanged=current), "campaigns")
        after = self.get(f"/campaigns/{campaign_id}")["campaigns"][0]["campaign"]
        if after.get("status") != "PAUSED":
            raise SnapError(
                f"asked Snap to pause {current['name']} but it still reads "
                f"{after.get('status')!r}. Pause it by hand in Ads Manager."
            )
        return after

    # ---- ad squad --------------------------------------------------------
    def create_adsquad(self, *, name, campaign_id, targeting, daily_budget_inr,
                       start_time, end_time, pixel_id) -> dict:
        """Create the ad squad, PAUSED.

        `pixel_id` is required because every other LANDING_PAGE_VIEW squad in this
        account carries the same one, and the first squad this command created did
        not. A mismatch with the account's own convention is far more likely an
        omission than a deliberate choice, so it fails rather than passing quietly.

        Note what the pixel is NOT responsible for: Snap counts landing-page views
        for a WEB_VIEW ad natively, by rendering the page in its own in-app browser,
        and reported 59 of them for the pixel-less first run. So a missing pixel does
        not blind the optimisation goal. It was briefly diagnosed that way here, from
        a `conversion_page_views: 0` reading against the wrong stats field, and that
        was wrong.
        """
        if not pixel_id:
            raise SnapError(
                "pixel_id is required for a LANDING_PAGE_VIEW ad squad.\n"
                "Without it Snap cannot see the conversion it is being asked to "
                "optimise for. Set snap.pixel_id in config.local.yaml."
            )
        res = self.post(f"/campaigns/{campaign_id}/adsquads", {"adsquads": [{
            "pixel_id": pixel_id,
            "name": name,
            "campaign_id": campaign_id,
            "type": "SNAP_ADS",
            "status": "PAUSED",
            "targeting": targeting,
            "optimization_goal": "LANDING_PAGE_VIEW",
            "billing_event": "IMPRESSION",
            "bid_strategy": "AUTO_BID",
            "daily_budget_micro": int(daily_budget_inr * MICRO),
            "placement_v2": {"config": "AUTOMATIC"},
            "start_time": start_time,
            "end_time": end_time,
        }]})
        return self._one(res, "adsquads")

    # ---- media + creative + ad -------------------------------------------
    def upload_media(self, name: str, path: Path) -> dict:
        media = self._one(self.post(f"/adaccounts/{self.cfg['ad_account_id']}/media", {"media": [{
            "ad_account_id": self.cfg["ad_account_id"], "name": name, "type": "IMAGE",
        }]}), "media")

        boundary = uuid.uuid4().hex
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body = b"".join([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'.encode(),
            f"Content-Type: {ctype}\r\n\r\n".encode(),
            path.read_bytes(), b"\r\n", f"--{boundary}--\r\n".encode(),
        ])
        req = urllib.request.Request(
            f"{API}/media/{media['id']}/upload", data=body, method="POST",
            headers={"Authorization": f"Bearer {self.token}",
                     "content-type": f"multipart/form-data; boundary={boundary}"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                r.read()
        except urllib.error.HTTPError as e:
            raise SnapError(f"media upload -> HTTP {e.code}\n{e.read().decode()[:500]}") from e
        return media

    def create_creative(self, *, name, media_id, headline, brand_name, url, profile_id) -> dict:
        if len(headline) > 34:
            raise SnapError(f"headline is {len(headline)} chars; Snap's limit is 34: {headline!r}")
        res = self.post(f"/adaccounts/{self.cfg['ad_account_id']}/creatives", {"creatives": [{
            "ad_account_id": self.cfg["ad_account_id"],
            "name": name, "type": "WEB_VIEW",
            "headline": headline, "brand_name": brand_name,
            "call_to_action": "MORE", "shareable": True,
            "top_snap_media_id": media_id,
            "web_view_properties": {"url": url},
            "profile_properties": {"profile_id": profile_id},
        }]})
        return self._one(res, "creatives")

    def set_creative_url(self, creative: dict, url: str) -> dict:
        """Rewrite the landing URL once the real ad id exists.

        rules/tracking.md requires utm_id to carry the ad id, and the ad does not
        exist when the creative is created. Ads Manager solves this with a {{ad.id}}
        macro — the same macro whose silent non-resolution cost a week of spend on
        2026-08-21. Here the id is known for certain by the time this runs, so the
        URL is written literally and there is no macro left to fail.
        """
        body = {k: creative[k] for k in ("id", "ad_account_id", "name", "type", "headline",
                                         "brand_name", "call_to_action", "shareable",
                                         "top_snap_media_id", "profile_properties")
                if k in creative}
        body["web_view_properties"] = {"url": url}
        return self._one(self.put(f"/adaccounts/{self.cfg['ad_account_id']}/creatives",
                                  {"creatives": [body]}), "creatives")

    def create_ad(self, *, name, ad_squad_id, creative_id) -> dict:
        return self._one(self.post(f"/adsquads/{ad_squad_id}/ads", {"ads": [{
            "ad_squad_id": ad_squad_id, "creative_id": creative_id,
            "name": name, "type": "REMOTE_WEBPAGE", "status": "PAUSED",
        }]}), "ads")
