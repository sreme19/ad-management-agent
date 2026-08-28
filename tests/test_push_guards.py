"""What `snap-push` refuses before it creates anything.

None of these reach the network: each guard fires while the client is still None,
or the payload is examined without a request. The one test that does construct a
client asserts that a refused request never gets as far as urlopen.
"""
from __future__ import annotations

import pytest
import yaml
from conftest import propose_argv, run

from ad_management_agent import cli


def rec_id_of(root, slug="w2330"):
    text = (root / "campaigns" / slug / "record.md").read_text()
    return yaml.safe_load(text.split("---")[1])["rec_id"]


def strip_field(root, field, slug="w2330"):
    path = root / "campaigns" / slug / "record.md"
    _, fm, body = path.read_text().split("---", 2)
    data = yaml.safe_load(fm)
    data.pop(field, None)
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body)


class TestPushRefusesBeforeCreating:
    def test_a_record_with_no_targeting_block(self, ledger_root):
        # The defect this replaced: a hardcoded audience meant the second record
        # ever pushed would carry the first one's targeting and still diff clean.
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        strip_field(ledger_root, "targeting")
        assert run(["snap-push", rec, "--dry-run"]) == 2

    def test_a_creative_with_no_recorded_qa_pass(self, ledger_root):
        run(propose_argv(ledger_root))
        (ledger_root / "creatives" / "test-asset" / "qa.md").write_text("Verdict: `regenerate`\n")
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 2

    def test_a_missing_creative_asset(self, ledger_root):
        run(propose_argv(ledger_root))
        (ledger_root / "creatives" / "test-asset" / "asset-a.jpg").unlink()
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 2

    def test_a_creative_folder_holding_neither_an_mp4_nor_a_jpg(self, ledger_root):
        # Video support (2026-08-28) made the asset lookup try two names. The guard
        # has to fire when BOTH are absent, not just when the jpg is.
        run(propose_argv(ledger_root))
        (ledger_root / "creatives" / "test-asset" / "asset-a.jpg").unlink()
        assert not (ledger_root / "creatives" / "test-asset" / "asset-a.mp4").exists()
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 2


class TestVideoCreatives:
    """A creative folder holding asset-a.mp4 is pushed as a Snap VIDEO media.

    Snap's WEB_VIEW creative takes either an image or a video as its top snap, so
    the only thing that changes is the media type registered at upload.
    """

    def test_an_mp4_is_accepted_and_still_needs_its_qa_pass(self, ledger_root):
        run(propose_argv(ledger_root))
        creative = ledger_root / "creatives" / "test-asset"
        creative.joinpath("asset-a.mp4").write_bytes(b"\x00\x00\x00 ftypisom")
        creative.joinpath("qa.md").write_text("Verdict: `regenerate`\n")
        # The video path must not become a way around the QA gate.
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 2

    def test_an_mp4_wins_over_a_jpg_in_the_same_folder(self, ledger_root):
        run(propose_argv(ledger_root))
        creative = ledger_root / "creatives" / "test-asset"
        creative.joinpath("asset-a.mp4").write_bytes(b"\x00\x00\x00 ftypisom")
        assert creative.joinpath("asset-a.jpg").exists()
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 0

    def test_a_record_that_is_already_live(self, ledger_root):
        # Pushing twice would create duplicates against a record holding real ids.
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c",
             "--ad-set-id", "s", "--ad-id", "a"])
        assert run(["snap-push", rec, "--dry-run"]) == 2

    def test_a_meta_record(self, ledger_root):
        run(propose_argv(ledger_root))
        path = ledger_root / "campaigns" / "w2330" / "record.md"
        path.write_text(path.read_text().replace("network: snap", "network: meta", 1))
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 2


class TestDryRun:
    def test_it_works_without_credentials_and_says_what_it_could_not_check(
        self, ledger_root, capsys
    ):
        run(propose_argv(ledger_root))
        assert run(["snap-push", rec_id_of(ledger_root), "--dry-run"]) == 0
        out = capsys.readouterr().out
        assert "nothing created" in out
        # The cap is the one thing that can silently invalidate the test, so a dry
        # run that cannot check it has to say so rather than look clean.
        assert "spend cap was NOT" in out

    def test_the_plan_describes_the_audience_from_the_record(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        run(["snap-push", rec_id_of(ledger_root), "--dry-run"])
        assert "female, 23-30, IN, ANDROID" in capsys.readouterr().out


class TestCampaignCapGate:
    """The 2026-08-26 failure: Rs 1,000/day ad squad under a Rs 300/day campaign."""

    def gate(self, caps, daily=1000.0, days=5, accept=False):
        return run_gate(caps, daily, days, accept)

    def test_a_binding_daily_cap_blocks(self):
        assert self.gate({"daily_inr": 300.0, "lifetime_inr": None}) == 2

    def test_accept_proceeds_but_states_the_deviation(self, capsys):
        assert self.gate({"daily_inr": 300.0, "lifetime_inr": None}, accept=True) == 0
        out = capsys.readouterr().out
        assert "BLOCKED" in out and "stated deviation" in out
        assert "ad-agent note" in out

    def test_a_binding_lifetime_cap_blocks(self):
        assert self.gate({"daily_inr": None, "lifetime_inr": 2000.0}) == 2

    def test_no_cap_proceeds(self):
        assert self.gate({"daily_inr": None, "lifetime_inr": None}) == 0

    def test_a_cap_above_the_squad_budget_proceeds(self):
        assert self.gate({"daily_inr": 5000.0, "lifetime_inr": None}) == 0

    def test_a_lifetime_cap_covering_the_run_proceeds(self):
        assert self.gate({"daily_inr": None, "lifetime_inr": 5000.0}) == 0

    def test_a_thin_budget_under_no_cap_warns_but_proceeds(self, capsys):
        assert self.gate({"daily_inr": None, "lifetime_inr": None}, daily=300.0) == 0
        assert "WARNING" in capsys.readouterr().out


def run_gate(caps, daily, days, accept):
    try:
        cli._gate_campaign_caps(caps, squad_daily_inr=daily, duration_days=days,
                                rec_id="rec-x", accept=accept)
    except SystemExit as exc:
        return exc.code or 0
    return 0


class TestMetaPushRefusesBeforeCreating:
    """The same guard set as snap-push, plus the ones only Meta needs.

    None of these reach the network: each fires while the client is still None.
    """

    def test_a_snap_record_is_refused_by_meta_push(self, ledger_root):
        # The mirror of snap-push's own network check. Each push knows one API, and
        # the registry cannot teach either of them a second one.
        run(propose_argv(ledger_root, network="snap"))
        assert run(["meta-push", rec_id_of(ledger_root), "--dry-run"]) == 2

    def test_a_record_with_no_targeting_block(self, ledger_root):
        run(propose_argv(ledger_root, network="meta"))
        strip_field(ledger_root, "targeting")
        assert run(["meta-push", rec_id_of(ledger_root), "--dry-run"]) == 2

    def test_a_creative_with_no_recorded_qa_pass(self, ledger_root):
        run(propose_argv(ledger_root, network="meta"))
        (ledger_root / "creatives" / "test-asset" / "qa.md").write_text("Verdict: `regenerate`\n")
        assert run(["meta-push", rec_id_of(ledger_root), "--dry-run"]) == 2


class TestMetaPushDryRunHappyPath:
    def test_it_prints_the_plan_and_creates_nothing(self, ledger_root, capsys):
        run(propose_argv(ledger_root, network="meta"))
        assert run(["meta-push", rec_id_of(ledger_root), "--dry-run"]) == 0
        out = capsys.readouterr().out

        # The plan the operator reads before anything is created.
        assert "everything created PAUSED" in out
        assert "LANDING_PAGE_VIEWS" in out
        assert "--dry-run: nothing created." in out

        # With no credentials configured, the missing parent-budget check has to be
        # stated rather than passed over in silence — it is the one thing that can
        # invalidate the test the record exists to run.
        assert "budget state was NOT" in out

        # The dropped spec field is said out loud. A silent drop is how a reader
        # comes to believe a declaration was made that was not.
        assert "regulated_content has no Meta equivalent" in out

    def test_the_dry_run_never_touches_the_network(self, ledger_root, monkeypatch):
        import urllib.request
        monkeypatch.setattr(urllib.request, "urlopen",
                            lambda *a, **k: pytest.fail("a dry run reached the network"))
        run(propose_argv(ledger_root, network="meta"))
        assert run(["meta-push", rec_id_of(ledger_root), "--dry-run"]) == 0
