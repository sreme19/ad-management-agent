"""Structured targeting: the checks that refuse, and the translation that pushes."""
from __future__ import annotations

import pytest

from ad_management_agent import targeting


def spec(**over):
    base = {"gender": "FEMALE", "min_age": "23", "max_age": "30",
            "countries": ["in"], "os": "ANDROID"}
    base.update(over)
    return targeting.build(**base)


class TestValidationRefuses:
    def test_under_18_is_refused(self):
        # rules/compliance.md: 18+ without exception.
        with pytest.raises(targeting.TargetingError, match="18"):
            spec(min_age="16")

    def test_18_exactly_is_allowed(self):
        assert spec(min_age="18")["min_age"] == "18"

    def test_a_mixed_gender_ad_set_has_no_spelling(self):
        with pytest.raises(targeting.TargetingError):
            spec(gender="ALL")

    def test_max_below_min_is_refused(self):
        with pytest.raises(targeting.TargetingError, match="below min_age"):
            spec(min_age="30", max_age="25")

    def test_open_ended_top_band_is_allowed(self):
        assert spec(max_age="50+")["max_age"] == "50+"

    def test_open_ended_min_age_is_refused(self):
        with pytest.raises(targeting.TargetingError):
            spec(min_age="18+")

    def test_countries_must_be_two_letter_codes(self):
        with pytest.raises(targeting.TargetingError):
            spec(countries=["india"])

    def test_countries_cannot_be_empty(self):
        with pytest.raises(targeting.TargetingError):
            spec(countries=[])


class TestTheRecordCannotDisagreeWithItself:
    def test_female_spec_under_a_mens_name_is_refused(self):
        with pytest.raises(targeting.TargetingError, match="(?i)one of the two is wrong"):
            targeting.check_matches_ad_set_name(spec(), "MEN_23-30_CASUAL_LPV")

    def test_agreement_passes(self):
        targeting.check_matches_ad_set_name(spec(), "WOMEN_23-30_CASUAL_LPV")

    def test_a_name_with_no_gender_token_is_left_to_the_destination_gate(self):
        # That gate reports it with the fuller explanation and runs on every path
        # that reaches here, so raising twice would only bury the better message.
        targeting.check_matches_ad_set_name(spec(), "SOMETHING_23-30_LPV")


class TestSnapTranslation:
    def test_demographics_geos_and_devices(self):
        payload = targeting.to_snap(spec())
        assert payload["demographics"] == [
            {"min_age": "23", "max_age": "30", "gender": "FEMALE", "operation": "INCLUDE"}]
        assert payload["geos"] == [{"country_code": "in", "operation": "INCLUDE"}]
        assert payload["devices"] == [{"os_type": "ANDROID", "operation": "INCLUDE"}]

    def test_dating_is_flagged_as_regulated_by_default(self):
        # An ad squad without this is a different, and rejectable, ad squad.
        assert targeting.to_snap(spec())["regulated_content"] is True

    def test_ios_keeps_snaps_own_spelling(self):
        assert targeting.to_snap(spec(os="IOS"))["devices"][0]["os_type"] == "iOS"

    def test_no_os_means_no_device_narrowing(self):
        assert "devices" not in targeting.to_snap(spec(os=None))

    def test_expansion_off_sends_the_flag_as_false_rather_than_omitting_it(self):
        # This test used to assert the opposite, and the opposite was a bug. Snap
        # defaults targeting expansion ON, so omitting the key silently broadens the
        # audience while the record claims it is narrow. Found on
        # rec-2026-08-28-moveon-swagger-w2530-snap: record said `expansion: off`,
        # live ad squad read back `enable_targeting_expansion: true`.
        payload = targeting.to_snap(spec(expansion=False))
        assert payload["enable_targeting_expansion"] is False
        assert payload["auto_expansion_options"] == {
            "interest_expansion_option": {"enabled": False},
            "custom_audience_expansion_option": {"enabled": False},
        }

    def test_the_readback_catches_snap_defaulting_expansion_on(self):
        # The live squad has no expansion key at all — which is how Snap reports an
        # ad squad it has broadened by default. A check that skipped the missing key
        # would pass exactly the case that broke.
        rows = targeting.snap_readback_checks(
            spec(expansion=False), {"targeting": {"demographics": [{}], "geos": []}}
        )
        got, want = next((g, w) for label, g, w in rows if label == "expansion")
        assert (got, want) == (True, False)


class TestReadBackIsDerivedNotHardcoded:
    """The bug this whole module exists to fix.

    A read-back compared against a literal only ever validates the code against
    itself. These assert the comparison follows the spec instead.
    """

    def test_a_wrong_audience_is_caught(self):
        live = {"targeting": {
            "demographics": [{"gender": "FEMALE", "min_age": "18", "max_age": "22"}],
            "geos": [{"country_code": "in"}], "devices": [{"os_type": "ANDROID"}]}}
        rows = targeting.snap_readback_checks(spec(min_age="23", max_age="30"), live)
        mismatched = [label for label, got, want in rows if str(got) != str(want)]
        assert mismatched == ["min age", "max age"]

    def test_a_matching_squad_produces_no_diff(self):
        live = {"targeting": {
            "demographics": [{"gender": "FEMALE", "min_age": "23", "max_age": "30"}],
            "geos": [{"country_code": "in"}], "devices": [{"os_type": "ANDROID"}]}}
        assert [r for r in targeting.snap_readback_checks(spec(), live)
                if str(r[1]) != str(r[2])] == []


class TestMetaTranslation:
    """One spec, two networks. Meta disagrees with Snap on nearly every field type."""

    def test_gender_becomes_an_integer_code(self):
        assert targeting.to_meta(spec(gender="FEMALE"))["genders"] == [2]
        assert targeting.to_meta(spec(gender="MALE"))["genders"] == [1]

    def test_ages_become_integers_not_strings(self):
        payload = targeting.to_meta(spec(min_age="25", max_age="30"))
        assert payload["age_min"] == 25 and payload["age_max"] == 30
        assert isinstance(payload["age_min"], int)

    def test_open_ended_max_age_maps_onto_metas_top_band(self):
        # Snap's `50+` has no Meta equivalent; Meta's maximum is 65, rendered "65+".
        assert targeting.to_meta(spec(max_age="50+"))["age_max"] == targeting.META_MAX_AGE

    def test_countries_are_uppercased(self):
        assert targeting.to_meta(spec())["geo_locations"]["countries"] == ["IN"]

    def test_expansion_polarity_is_written_explicitly_both_ways(self):
        # The trap: Meta broadens unless told not to, so an omitted field is not a
        # neutral default. Both directions must appear in the payload.
        on = targeting.to_meta(spec(expansion=True))["targeting_automation"]
        off = targeting.to_meta(spec(expansion=False))["targeting_automation"]
        assert on["advantage_audience"] == 1
        assert off["advantage_audience"] == 0

    def test_regulated_content_is_dropped_rather_than_invented(self):
        # Snap has a flag for it; Meta handles dating as an account-level written
        # permission and has no field. Mapping it to something plausible-looking
        # would make a reader believe a declaration was made that was not.
        payload = targeting.to_meta(spec())
        assert not any("regulated" in k for k in payload)

    def test_the_snap_payload_is_untouched_by_the_meta_one(self):
        # One stored spec, two translators — the point of keeping the spec neutral.
        s = spec()
        snap_payload = targeting.to_snap(s)
        targeting.to_meta(s)
        assert targeting.to_snap(s) == snap_payload


class TestMetaReadback:
    def test_a_broadened_adset_is_caught(self):
        # Meta rewrites targeting it considers suboptimal rather than rejecting it:
        # an ad set created with advantage_audience 0 can come back 1, with the POST
        # still returning 200. This is the case a diff catches.
        live = {"targeting": {
            "genders": [2], "age_min": 25, "age_max": 30,
            "geo_locations": {"countries": ["IN"]},
            "targeting_automation": {"advantage_audience": 1},
            "user_os": ["Android"]}}
        rows = targeting.meta_readback_checks(
            spec(min_age="25", max_age="30", expansion=False), live)
        assert [label for label, got, want in rows if str(got) != str(want)] \
            == ["advantage audience"]

    def test_a_matching_adset_produces_no_diff(self):
        live = {"targeting": {
            "genders": [2], "age_min": 23, "age_max": 30,
            "geo_locations": {"countries": ["IN"]},
            "targeting_automation": {"advantage_audience": 1},
            "user_os": ["Android"]}}
        assert [r for r in targeting.meta_readback_checks(spec(), live)
                if str(r[1]) != str(r[2])] == []

    def test_a_wrong_audience_is_caught(self):
        live = {"targeting": {
            "genders": [1], "age_min": 18, "age_max": 22,
            "geo_locations": {"countries": ["US"]},
            "targeting_automation": {"advantage_audience": 1},
            "user_os": ["Android"]}}
        rows = targeting.meta_readback_checks(spec(), live)
        assert [label for label, got, want in rows if str(got) != str(want)] \
            == ["gender", "min age", "max age", "countries"]
