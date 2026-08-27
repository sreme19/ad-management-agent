"""The paused-only rule on Meta, tested as an invariant rather than trusted as a docstring.

The sibling of test_snap_safety.py. SPEC.md decision #3 was extended to Meta on
2026-08-27 on the explicit condition that a Meta client carry its own equivalent of
`SnapClient._call`'s transport-layer refusal — so these tests are the condition, not
a nicety.

The classes marked WHERE META DIFFERS are the ones that would not exist if this file
had been a copy of the Snap one. Each covers a hole that mirroring Snap's shape would
have left open.
"""
from __future__ import annotations

import pytest

from ad_management_agent import meta as metaapi


def violations(method, path, payload):
    return metaapi._safety_violations(method, path, payload)


CREATE_ADSETS = "/23842/adsets"          # POST here creates
UPDATE_ADSET = "/23843"                  # POST here updates
CREATE_CAMPAIGNS = "/act_1561367575690055/campaigns"


class TestNothingCanBeEnabled:
    def test_top_level_active_is_refused(self):
        assert violations("POST", CREATE_ADSETS, {"status": "ACTIVE"})

    def test_active_nested_in_a_subdocument_is_refused(self):
        # Meta nests heavily — object_story_spec.link_data, targeting.geo_locations —
        # so a dangerous field is rarely at the top level of a real request.
        assert violations("POST", CREATE_ADSETS,
                          {"name": "x", "promoted_object": {"status": "ACTIVE"}})

    @pytest.mark.parametrize("value", ["ACTIVE", "active", "Running", "ENABLED", "on", "LIVE"])
    def test_every_enabling_spelling_is_refused(self, value):
        assert violations("POST", UPDATE_ADSET, {"status": value})

    def test_configured_status_is_covered_too(self):
        # Meta exposes both `status` and `configured_status`; guarding only the first
        # would leave a second spelling of the same action wide open.
        assert violations("POST", UPDATE_ADSET, {"configured_status": "ACTIVE"})

    def test_paused_is_allowed(self):
        # Pausing stops spend. Stopping spend is always safe.
        assert violations("POST", UPDATE_ADSET, {"status": "PAUSED"}) == []


class TestNothingCanBeDestroyed:
    """WHERE META DIFFERS: delete and archive travel through the `status` field.

    Snap has no equivalent — this guard has no counterpart in snap.py. `ad-audit` has
    to read a pushed ad set months later to close its loop, and an ARCHIVED object
    drops out of Meta's default listings, so both are refused.
    """

    @pytest.mark.parametrize("value", ["DELETED", "ARCHIVED", "deleted"])
    def test_destructive_statuses_are_refused(self, value):
        found = violations("POST", UPDATE_ADSET, {"status": value})
        assert found and "destroy or hide" in found[0]

    def test_destroying_is_refused_even_on_a_create_path(self):
        assert violations("POST", CREATE_ADSETS, {"status": "DELETED"})


class TestBudgetsCannotBeChangedAfterCreation:
    """WHERE META DIFFERS: create vs update is a PATH distinction, not a method one.

    Meta has no PUT. Creating is POST /act_X/campaigns and updating is POST
    /{campaign_id} — both POST. snap.py keys its budget guard off the method, which
    ported here verbatim would classify every budget change as a creation and wave it
    through. These tests are what holds that distinction in place.
    """

    def test_budget_on_an_update_is_refused(self):
        assert violations("POST", UPDATE_ADSET, {"daily_budget": 500_000})

    def test_budget_on_a_create_is_allowed(self):
        # Creation is how an ad set gets a budget at all.
        assert violations("POST", CREATE_ADSETS, {"daily_budget": 100_000}) == []

    @pytest.mark.parametrize("key", sorted(metaapi.BUDGET_KEYS))
    def test_every_budget_key_is_covered_on_an_update(self, key):
        assert violations("POST", UPDATE_ADSET, {key: 1})

    def test_an_unknown_collection_fails_closed_not_open(self):
        # If Meta adds a collection this module has not been taught, its creates get
        # refused for carrying a budget. That is the safe direction to be wrong in:
        # a false refusal is a code change, a false allow is a live budget change.
        assert violations("POST", "/23842/somethingnew", {"daily_budget": 1})

    def test_there_is_no_echo_exemption(self):
        # snap.py must allow a budget key whose value is unchanged, because Snap's
        # update is a full replace and omitting the field deletes the cap — the
        # 2026-08-26 17:24 UTC incident. Meta's update is a patch, so no such
        # exemption exists here, and none should be added.
        assert violations("POST", UPDATE_ADSET, {"daily_budget": 100_000})


class TestTheRealCallsStillPass:
    def test_creating_a_paused_campaign_is_allowed(self):
        assert violations("POST", CREATE_CAMPAIGNS, {
            "name": "FB_TRAFFIC_GETW_IN_BLR_TOF_202608", "status": "PAUSED",
            "objective": "OUTCOME_TRAFFIC", "special_ad_categories": []}) == []

    def test_creating_a_paused_adset_with_a_budget_is_allowed(self):
        assert violations("POST", CREATE_ADSETS, {
            "status": "PAUSED", "daily_budget": 100_000,
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "targeting": {"age_min": 25, "age_max": 30, "genders": [2]}}) == []

    def test_writing_url_tags_onto_an_ad_is_allowed(self):
        # set_ad_url_tags is an update, and it must keep working — it is how
        # utm_content gets the real ad id instead of a {{ad.id}} macro that can
        # silently not resolve, as one did on 2026-08-21.
        assert violations("POST", "/23844", {
            "url_tags": "utm_source=meta&utm_content=23844"}) == []

    def test_pausing_a_campaign_is_allowed(self):
        assert violations("POST", "/23841", {"status": "PAUSED"}) == []


class TestTheClientRefusesBeforeSending:
    def client(self):
        return metaapi.MetaClient({"access_token": "x", "ad_account_id": "act_1", "page_id": "2"})

    def test_call_raises_and_never_reaches_the_network(self, monkeypatch):
        monkeypatch.setattr(metaapi.urllib.request, "urlopen",
                            lambda *a, **k: pytest.fail("a refused request reached the network"))
        with pytest.raises(metaapi.MetaSafetyError) as exc:
            self.client().post("/23843", {"status": "ACTIVE"})
        assert "paused-only rule" in str(exc.value)

    def test_a_budget_change_never_reaches_the_network(self, monkeypatch):
        monkeypatch.setattr(metaapi.urllib.request, "urlopen",
                            lambda *a, **k: pytest.fail("a refused request reached the network"))
        with pytest.raises(metaapi.MetaSafetyError):
            self.client().post("/23843", {"daily_budget": 999_999})

    def test_the_error_is_a_metaerror_so_nothing_swallows_it_by_type(self):
        assert issubclass(metaapi.MetaSafetyError, metaapi.MetaError)

    def test_no_enable_or_resume_method_exists_on_the_client(self):
        # Decision #3 says there is no enable/resume/activate call and none is to be
        # added without the app owner saying so. This asserts the absence, so adding
        # one is a deliberate act that fails a test rather than a quiet commit.
        banned = [n for n in dir(metaapi.MetaClient)
                  if any(w in n.lower() for w in ("enable", "resume", "activate", "unpause"))]
        assert banned == [], f"MetaClient grew an enabling method: {banned}"

    def test_the_token_is_never_put_in_a_url(self, monkeypatch):
        seen = {}

        class FakeResponse:
            def read(self):
                return b"{}"
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False

        def fake_urlopen(req, *a, **k):
            seen["url"] = req.full_url
            seen["auth"] = req.get_header("Authorization")
            return FakeResponse()

        monkeypatch.setattr(metaapi.urllib.request, "urlopen", fake_urlopen)
        self.client().get("/act_1/campaigns", fields="id,name")
        assert "SECRETTOKEN" not in seen["url"]
        assert "access_token" not in seen["url"], (
            "a non-expiring system-user token in a query string is a leak with no "
            "rotation story, because there is no refresh step"
        )
        assert seen["auth"] == "Bearer x"


class TestMoneyIsInTheRightUnit:
    """WHERE META DIFFERS: minor units, not micro. Getting this wrong is 10,000x."""

    def test_minor_is_paise_not_micro(self):
        from ad_management_agent import snap as snapapi
        assert metaapi.MINOR == 100
        assert snapapi.MICRO == 1_000_000
        # Stated as a relationship rather than two constants, because the hazard is
        # someone "harmonising" them later.
        assert snapapi.MICRO // metaapi.MINOR == 10_000

    def test_a_thousand_rupees_is_a_hundred_thousand_paise(self):
        assert round(1000 * metaapi.MINOR) == 100_000

    def test_the_api_version_is_pinned(self):
        # Meta auto-upgrades unpinned callers since 2026-07-29, and versions expire.
        assert metaapi.API_VERSION.startswith("v")
        assert metaapi.API.endswith(metaapi.API_VERSION)
