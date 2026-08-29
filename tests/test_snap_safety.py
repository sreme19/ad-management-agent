"""The paused-only rule, tested as an invariant rather than trusted as a docstring.

SPEC.md decision #3 says this agent never enables anything and never changes the
budget of anything live, and is honest that the guarantee stopped being structural
the day the repo gained a Snap credential. These tests are what "the code is
careful" has to mean to be worth anything.
"""
from __future__ import annotations

import pytest

from ad_management_agent import snap as snapapi


def violations(method, payload):
    return snapapi._safety_violations(method, payload)


class TestNothingCanBeEnabled:
    def test_top_level_active_is_refused(self):
        assert violations("POST", {"status": "ACTIVE"})

    def test_active_nested_inside_snaps_list_wrapper_is_refused(self):
        # Snap wraps every object in a list under a plural key, so the dangerous
        # field is never at the top level in a real request.
        assert violations("POST", {"adsquads": [{"name": "x", "status": "ACTIVE"}]})

    @pytest.mark.parametrize("value", ["ACTIVE", "active", "Running", "ENABLED", "on", "LIVE"])
    def test_every_enabling_spelling_is_refused(self, value):
        assert violations("PUT", {"ads": [{"status": value}]})

    def test_paused_is_allowed(self):
        # Pausing stops spend. Stopping spend is always safe.
        assert violations("PUT", {"adsquads": [{"status": "PAUSED"}]}) == []


class TestBudgetsCannotBeChangedAfterCreation:
    def test_budget_on_a_put_is_refused(self):
        assert violations("PUT", {"adsquads": [{"daily_budget_micro": 5_000_000_000}]})

    def test_budget_on_a_post_is_allowed(self):
        # Creation is how an ad squad gets a budget at all.
        assert violations("POST", {"adsquads": [{"daily_budget_micro": 1_000_000_000}]}) == []

    @pytest.mark.parametrize("key", sorted(snapapi.BUDGET_KEYS))
    def test_every_budget_key_is_covered_on_put(self, key):
        assert violations("PUT", {key: 1})


class TestTheRealCallsStillPass:
    def test_creating_a_paused_campaign_is_allowed(self):
        assert violations("POST", {"campaigns": [{
            "name": "RA_TRAFFIC_GET_IN_PAN_TOF_202608", "status": "PAUSED",
            "buy_model": "AUCTION"}]}) == []

    def test_creating_a_paused_adsquad_with_a_budget_is_allowed(self):
        assert violations("POST", {"adsquads": [{
            "status": "PAUSED", "daily_budget_micro": 1_000_000_000,
            "bid_strategy": "AUTO_BID"}]}) == []

    def test_rewriting_a_creative_url_is_allowed(self):
        # set_creative_url is a PUT, and it must keep working — it is how utm_id
        # gets the real ad id instead of a macro that can silently not resolve.
        assert violations("PUT", {"creatives": [{
            "id": "abc", "name": "STORY_X", "type": "WEB_VIEW",
            "web_view_properties": {"url": "https://www.riteangle.dating/get/w?utm_id=1"}}]}) == []


class TestTheClientRefusesBeforeSending:
    def test_call_raises_and_never_reaches_the_network(self, monkeypatch):
        client = snapapi.SnapClient({"client_id": "x", "client_secret": "x",
                                     "refresh_token": "x", "ad_account_id": "x"})
        # If the guard let this through, urlopen would be reached — and a token
        # would be minted first. Both would fail this test loudly.
        monkeypatch.setattr(snapapi.urllib.request, "urlopen",
                            lambda *a, **k: pytest.fail("a refused request reached the network"))
        with pytest.raises(snapapi.SnapSafetyError) as exc:
            client.post("/adsquads/abc/ads", {"ads": [{"status": "ACTIVE"}]})
        assert "paused-only rule" in str(exc.value)

    def test_the_error_is_a_snaperror_so_nothing_swallows_it_by_type(self):
        assert issubclass(snapapi.SnapSafetyError, snapapi.SnapError)


class TestTheLeadPathIsGuardedToo:
    """The Snap lead path (2026-08-29) inherits the guard; assert it, don't assume it."""

    def test_creating_a_lead_form_is_allowed(self):
        from ad_management_agent.snap import _safety_violations
        assert not _safety_violations("POST", {"lead_generation_forms": [{
            "name": "RA_LEAD_WOMEN_18-30_CASUAL_MOVEON-LEAD_SNAP",
            "form_fields": [{"type": "FIRST_NAME"}, {"type": "PHONE_NUMBER"}, {"type": "EMAIL"}],
            "privacy_policy_url": "https://www.riteangle.dating/privacy-policy",
            "end_page_properties": {"call_to_action": "VIEW_WEBSITE",
                                    "url": "https://www.riteangle.dating/get/w-apply?ra_src=form"},
        }]})

    def test_a_lead_ad_created_active_is_refused(self):
        from ad_management_agent.snap import _safety_violations
        assert _safety_violations("POST", {"ads": [{
            "name": "x", "type": "LEAD_GENERATION", "status": "ACTIVE"}]})

    def test_a_paused_lead_adsquad_with_a_budget_is_allowed(self):
        from ad_management_agent.snap import _safety_violations
        assert not _safety_violations("POST", {"adsquads": [{
            "name": "WOMEN_18-30_CASUAL_MOVEON-LEAD", "status": "PAUSED",
            "optimization_goal": "LEAD_FORM_SUBMISSIONS",
            "daily_budget_micro": 300000000}]})
