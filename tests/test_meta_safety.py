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


class TestTheAccountsOwnConventionNotSnaps:
    """Corrections made 2026-08-27 after reading the live account, not the docs.

    The first cut of meta.py mirrored snap.py's pixel requirement and asserted "Meta
    has no fallback, no pixel means no signal at all". The account says otherwise: its
    live LANDING_PAGE_VIEWS ad set FB_W_20-25_ID_Romantic binds no dataset at ad-set
    level, has Website events unchecked, and its ad reported 36 landing-page views.
    Meta binds the dataset at the ACCOUNT level. These tests keep the correction from
    being quietly re-broken by someone tidying it back into symmetry with Snap.
    """

    def sig(self):
        import inspect
        return inspect.signature(metaapi.MetaClient.create_adset)

    def test_pixel_id_is_optional(self):
        assert self.sig().parameters["pixel_id"].default is None, (
            "pixel_id must stay optional: the account's own live LPV ad set has none"
        )

    def test_the_adset_payload_does_not_send_promoted_object(self):
        # promoted_object carrying a pixel belongs to OFFSITE_CONVERSIONS, a different
        # optimisation goal. Sending it on an OUTCOME_TRAFFIC/LANDING_PAGE_VIEWS ad set
        # sets a field the account's own working ad set does not set.
        import inspect
        src = inspect.getsource(metaapi.MetaClient.create_adset)
        assert "promoted_object" not in src.split('"""')[-1], (
            "promoted_object is back in the ad-set payload; a conversions objective "
            "would need it, but that is a new code path, not this one"
        )

    def test_landing_page_views_is_still_the_goal(self):
        # The correction was about the pixel, not about the KPI. The account's live ad
        # set reads "Maximise number of landing page views", so this must not drift.
        import inspect
        assert "LANDING_PAGE_VIEWS" in inspect.getsource(metaapi.MetaClient.create_adset)

    def test_a_non_inr_account_is_still_refused(self, monkeypatch):
        # Confirmed INR on 2026-08-27 (the ad set's cost goal reads "in Indian Rupee"),
        # so this check should pass in practice — but it is the guard against a 10,000x
        # error, so it must still fire for anything else.
        client = metaapi.MetaClient({"access_token": "x", "ad_account_id": "act_1",
                                     "page_id": "2"})
        monkeypatch.setattr(type(client), "currency",
                            property(lambda self: "USD"))
        with pytest.raises(metaapi.MetaError, match="not INR"):
            client.require_inr()


class TestBudgetSharingIsAlwaysOff:
    """Meta requires is_adset_budget_sharing_enabled on a no-campaign-budget campaign.

    Discovered on 2026-08-28 when the first real push failed at create_campaign. The
    value is not a preference: True hands Meta 20% of every child ad set's budget to
    redistribute, which is a softer form of the campaign-budget-optimisation parent
    that meta-push refuses outright. On a Rs 1,000/day ad set that is Rs 200/day of
    drift — the difference between clearing rules/budget.md's Rs 800 floor and not.
    """

    def test_campaign_creation_sets_it_false(self):
        import inspect
        src = inspect.getsource(metaapi.MetaClient.create_campaign)
        body = src.split('"""')[-1]
        assert '"is_adset_budget_sharing_enabled": False' in body, (
            "budget sharing must be explicitly False on every campaign this creates"
        )
        assert "True" not in body.split("is_adset_budget_sharing_enabled")[1][:40]

    def test_flipping_it_on_an_existing_campaign_is_refused(self):
        # Settable at creation (Meta requires it); a change afterwards is a budget
        # change, because it alters what the child ad sets actually spend.
        assert violations("POST", UPDATE_ADSET, {"is_adset_budget_sharing_enabled": True})
        assert violations("POST", "/23841", {"is_adset_budget_sharing_enabled": False})
        assert violations("POST", CREATE_CAMPAIGNS,
                          {"is_adset_budget_sharing_enabled": False}) == []


class TestTheAuthHintDoesNotMisfire:
    def test_a_validation_error_labelled_oauthexception_gets_no_auth_hint(self):
        # Meta returns type OAuthException for plain validation failures. Keying the
        # hint off that type printed "check your asset assignments" under an error
        # about a missing field, which sends the reader to the wrong place entirely.
        import inspect
        src = inspect.getsource(metaapi.MetaClient._call)
        assert '"OAuth" in detail' not in src
        assert "access token" in src


class TestObjectsAreCreatedOnTheRightEndpoint:
    """Meta's parent/child creation endpoints are not Snap's, and the difference bites.

    snap.py creates an ad squad at /campaigns/{id}/adsquads. Meta's campaign node
    exposes `adsets` as a read-only edge, so the same shape 400s with a message that
    blames permissions — which sent the first real push (2026-08-28) looking at asset
    assignments for a campaign its own token had just created.
    """

    def test_adsets_are_created_on_the_ad_account_not_the_campaign(self):
        import inspect
        src = inspect.getsource(metaapi.MetaClient.create_adset)
        body = src.split('"""')[-1]
        assert "/adsets" in body
        assert "{campaign_id}/adsets" not in body, (
            "ad sets must be created on the ad account with campaign_id in the body"
        )
        assert "account_path" in body

    def test_every_create_still_classifies_as_a_create(self):
        # The guard keys off the last path segment, so moving a create between
        # parents must not accidentally reclassify it as an update and start
        # refusing its budget.
        for path in ("/act_1/adsets", "/act_1/campaigns", "/act_1/ads",
                     "/act_1/adcreatives", "/act_1/adimages"):
            assert metaapi._is_create("POST", path), path
            assert violations("POST", path, {"daily_budget": 100_000}) == []


class TestTrackingSurvivesMetasImmutability:
    """The url_tags saga of 2026-08-28, encoded so it cannot silently regress.

    Three shapes were tried against the live account. Only the third persists:
      1. POST url_tags to /{ad_id}          -> 200, and read back as None. A SILENT
                                               no-op, which is why decision #3 requires
                                               reading every object back.
      2. POST url_tags to /{creative_id}    -> 400, "specify the name, status or
                                               associated advert labels". Creatives are
                                               effectively immutable.
      3. Create a NEW creative WITH url_tags, then repoint the ad at it -> works.
    """

    def test_the_ad_level_url_tags_writer_is_gone(self):
        assert not hasattr(metaapi.MetaClient, "set_ad_url_tags"), (
            "set_ad_url_tags returned 200 and never persisted — it must not come back"
        )

    def test_the_tracked_creative_path_exists_and_verifies_itself(self):
        import inspect
        assert hasattr(metaapi.MetaClient, "attach_tracked_creative")
        src = inspect.getsource(metaapi.MetaClient.attach_tracked_creative)
        body = src.split('"""')[-1]
        # url_tags must be set at CREATION, on the adcreatives collection.
        assert '"url_tags": url_tags' in body
        assert "adcreatives" in body
        # And it must read back and refuse rather than trust the 200 that fooled it.
        assert "if got != url_tags" in body
        assert "url_tags" in body and "raise MetaError" in body

    def test_attaching_a_creative_is_not_blocked_by_the_safety_guard(self):
        # Repointing an ad is an update carrying no status and no budget key.
        assert violations("POST", "/23844", {"creative": {"creative_id": "99"}}) == []

    def test_creating_a_creative_with_tracking_is_allowed(self):
        assert violations("POST", "/act_1/adcreatives", {
            "name": "X_CREATIVE_TRACKED",
            "url_tags": "utm_source=fb&utm_content=23844"}) == []


class TestEveryLevelIsResumable:
    """No rollback and five objects means a partial run is a normal state.

    The first real push failed three times, twice with objects already created. Each
    level needs an exact-name finder or a retry mints duplicates — which is the
    collision find_campaign already refuses to guess through, and which would break
    pocket-dating-coach's ad-set rollup.
    """

    @pytest.mark.parametrize("finder", ["find_campaign", "find_adset", "find_ad"])
    def test_a_finder_exists_at_each_level(self, finder):
        assert callable(getattr(metaapi.MetaClient, finder, None))

    @pytest.mark.parametrize("finder", ["find_campaign", "find_adset", "find_ad"])
    def test_each_finder_refuses_rather_than_guessing(self, finder):
        import inspect
        src = inspect.getsource(getattr(metaapi.MetaClient, finder))
        assert "len(hits) > 1" in src and "raise MetaError" in src
