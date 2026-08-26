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

    def test_expansion_off_omits_the_expansion_block(self):
        payload = targeting.to_snap(spec(expansion=False))
        assert "enable_targeting_expansion" not in payload
        assert "auto_expansion_options" not in payload


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
