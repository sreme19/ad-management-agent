"""The lifecycle rules SPEC.md states in prose, asserted as behaviour."""
from __future__ import annotations

import yaml
from conftest import propose_argv, run


def front_matter(root, slug="w2330"):
    text = (root / "campaigns" / slug / "record.md").read_text()
    return yaml.safe_load(text.split("---")[1])


class TestPropose:
    def test_writes_a_record_and_regenerates_the_index(self, ledger_root):
        assert run(propose_argv(ledger_root)) == 0
        assert (ledger_root / "campaigns" / "w2330" / "record.md").exists()
        assert "w2330" in (ledger_root / "INDEX.md").read_text()

    def test_carries_the_audience_twice_prose_and_spec(self, ledger_root):
        run(propose_argv(ledger_root))
        fm = front_matter(ledger_root)
        assert fm["targeting_summary"] == "prose reasoning for this audience"
        assert fm["targeting"] == {
            "gender": "FEMALE", "min_age": "23", "max_age": "30",
            "countries": ["in"], "os": "ANDROID",
            "expansion": True, "regulated_content": True,
        }

    def test_under_18_writes_nothing_at_all(self, ledger_root):
        assert run(propose_argv(ledger_root, min_age="16")) == 2
        assert not (ledger_root / "campaigns" / "w2330").exists()

    def test_a_spec_contradicting_its_own_ad_set_name_writes_nothing(self, ledger_root):
        assert run(propose_argv(ledger_root, gender="MALE")) == 2
        assert not (ledger_root / "campaigns" / "w2330").exists()

    def test_a_budget_below_the_floor_still_proposes(self, ledger_root):
        # budget.md's floor is guidance for the human, not a gate — the deviation
        # belongs in the brief. Only the *campaign cap* check refuses.
        assert run(propose_argv(ledger_root, budget_cap="300")) == 0


class TestDestinationGate:
    def test_a_womens_ad_set_cannot_point_at_the_mens_page(self, ledger_root):
        assert run(propose_argv(ledger_root,
                                destination_url="https://www.riteangle.dating/get")) == 2
        assert not (ledger_root / "campaigns" / "w2330").exists()

    def test_an_unregistered_page_fails_closed(self, ledger_root):
        assert run(propose_argv(ledger_root,
                                destination_url="https://www.riteangle.dating/nope")) == 2

    def test_a_page_that_cannot_take_paid_traffic_is_refused(self, ledger_root):
        # /beta matches on audience but is invite-token-gated.
        assert run(propose_argv(ledger_root,
                                destination_url="https://www.riteangle.dating/beta")) == 2

    def test_a_name_with_no_gender_token_is_refused(self, ledger_root):
        assert run(propose_argv(ledger_root, ad_set_name="EVERYONE_23-30_CASUAL_LPV")) == 2


class TestAmend:
    def test_targeting_is_patched_not_replaced(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        assert run(["amend", rec, "--reason", "widen the band", "--max-age", "35"]) == 0
        t = front_matter(ledger_root)["targeting"]
        assert t["max_age"] == "35"
        assert t["countries"] == ["in"] and t["os"] == "ANDROID" and t["gender"] == "FEMALE"

    def test_the_amendment_section_reports_per_sub_key(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        run(["amend", rec, "--reason", "widen", "--max-age", "35"])
        body = (ledger_root / "campaigns" / "w2330" / "record.md").read_text()
        assert "`targeting.max_age`" in body
        assert "'30' → '35'" in body

    def test_a_patch_cannot_leave_a_state_propose_would_refuse(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        assert run(["amend", rec, "--reason", "younger", "--min-age", "15"]) == 2
        assert front_matter(ledger_root)["targeting"]["min_age"] == "23"

    def test_renaming_across_genders_is_refused(self, ledger_root):
        # A rename can flip the gender token and leave the record self-contradictory.
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        assert run(["amend", rec, "--reason", "r", "--ad-set-name", "MEN_23-30_CASUAL_LPV"]) == 2

    def test_amend_cannot_launder_a_blocked_destination(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        assert run(["amend", rec, "--reason", "repoint",
                    "--destination-url", "https://www.riteangle.dating/get"]) == 2
        assert front_matter(ledger_root)["destination_url"].endswith("/get/w")

    def test_only_a_proposal_can_be_amended(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c",
             "--ad-set-id", "s", "--ad-id", "a"])
        assert front_matter(ledger_root)["status"] == "live"
        assert run(["amend", rec, "--reason", "too late", "--max-age", "35"]) == 2

    def test_nothing_to_amend_is_an_error_not_a_no_op(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        assert run(["amend", rec, "--reason", "nothing"]) == 2


class TestCloseTheLoop:
    def test_notes_accumulate_and_never_rewrite(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        run(["note", rec, "--kind", "budget", "--text", "raised on day three"])
        run(["note", rec, "--kind", "incident", "--text", "paused for a day"])
        body = (ledger_root / "campaigns" / "w2330" / "record.md").read_text()
        assert body.count("## Note — ") == 2
        assert "raised on day three" in body and "paused for a day" in body

    def test_log_setup_refuses_a_network_the_record_was_not_proposed_for(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        try:
            run(["log-setup", rec, "--network", "meta", "--campaign-id", "c",
                 "--ad-set-id", "s", "--ad-id", "a"])
            raised = False
        except ValueError:
            raised = True
        assert raised
        assert front_matter(ledger_root)["status"] == "proposed"

    def test_review_records_the_verdict_and_closes_the_record(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = front_matter(ledger_root)["rec_id"]
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c",
             "--ad-set-id", "s", "--ad-id", "a"])
        run(["log-review", rec, "--verdict", "inconclusive", "--summary", "capped below floor"])
        fm = front_matter(ledger_root)
        assert fm["status"] == "reviewed" and fm["verdict"] == "inconclusive"

    def test_a_second_proposal_with_the_same_slug_does_not_overwrite_the_first(self, ledger_root):
        run(propose_argv(ledger_root))
        run(propose_argv(ledger_root))
        assert (ledger_root / "campaigns" / "w2330" / "record.md").exists()
        assert (ledger_root / "campaigns" / "w2330-2" / "record.md").exists()
