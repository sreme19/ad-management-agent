"""`ad-agent open` — the entry point, and the one command meant to be remembered.

Its job is to be trustworthy when read cold, so these test what it says as much as
what it counts: a quiet report must not read as a finished loop.
"""
from __future__ import annotations

import datetime as dt

import yaml
from conftest import propose_argv, run

from ad_management_agent import cli


def rec_id_of(root, slug="w2330"):
    return yaml.safe_load(
        (root / "campaigns" / slug / "record.md").read_text().split("---")[1])["rec_id"]


def backdate(root, field, days, slug="w2330"):
    path = root / "campaigns" / slug / "record.md"
    _, fm, body = path.read_text().split("---", 2)
    data = yaml.safe_load(fm)
    today = dt.date.fromisoformat(cli._today())
    data[field] = (today - dt.timedelta(days=days)).isoformat()
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body)


def go_live(root, rec):
    run(["log-setup", rec, "--network", "snap", "--campaign-id", "c",
         "--ad-set-id", "s", "--ad-id", "a"])


class TestItNamesWhatItCannotSee:
    def test_an_empty_ledger_still_warns_about_unwired_loops(self, ledger_root, capsys):
        # The fixture ships a QA-passed creative, which is itself a loose end
        # (correctly). Remove it so this test sees a genuinely empty ledger.
        (ledger_root / "creatives" / "test-asset" / "qa.md").unlink()
        capsys.readouterr()
        assert run(["open"]) == 0
        out = capsys.readouterr().out
        assert "Nothing open in the ledger" in out
        # The important half: absence of a section is not evidence of nothing to do.
        assert "No store yet for: questions, notes, learnings, ideas" in out
        assert "not evidence" in out and "nothing outstanding" in out


class TestLooseEnds:
    def test_a_proposal_that_was_never_executed_shows_up(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        capsys.readouterr()
        run(["open"])
        assert "Proposed, never executed" in capsys.readouterr().out

    def test_an_old_proposal_is_marked_stale(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        backdate(ledger_root, "created", 30)
        capsys.readouterr()
        run(["open"])
        assert "STALE" in capsys.readouterr().out

    def test_a_live_ad_set_past_its_window_is_flagged_for_review(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        go_live(ledger_root, rec_id_of(ledger_root))
        backdate(ledger_root, "executed", 9)
        capsys.readouterr()
        run(["open"])
        out = capsys.readouterr().out
        assert "past the review window" in out
        assert "live 9d, window was 5d" in out

    def test_a_live_ad_set_inside_its_window_gets_a_review_date(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        go_live(ledger_root, rec_id_of(ledger_root))
        backdate(ledger_root, "executed", 1)
        capsys.readouterr()
        run(["open"])
        out = capsys.readouterr().out
        assert "still inside the window" in out and "review from" in out

    def test_a_reviewed_record_is_not_a_loose_end(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        go_live(ledger_root, rec)
        run(["log-review", rec, "--verdict", "working", "--summary", "done"])
        # Close the back-edge too, or the missing prompt verdict is itself an open
        # loose end — which is the point of that check.
        prompts = ledger_root / "creatives" / "test-asset" / "prompts.md"
        prompts.write_text(prompts.read_text() + "\n## Verdict: working\n")
        capsys.readouterr()
        capsys.readouterr()
        run(["open"])
        assert "Nothing open in the ledger" in capsys.readouterr().out


class TestFunding:
    def test_an_unverified_cap_is_only_reported_once_something_is_live(
        self, ledger_root, capsys
    ):
        # A proposal has no parent campaign to have been capped by yet.
        run(propose_argv(ledger_root))
        capsys.readouterr()
        run(["open"])
        assert "campaign cap never checked" not in capsys.readouterr().out
        go_live(ledger_root, rec_id_of(ledger_root))
        capsys.readouterr()
        run(["open"])
        assert "campaign cap never checked" in capsys.readouterr().out

    def test_a_verified_binding_cap_reports_the_real_effective_spend(
        self, ledger_root, capsys
    ):
        # The 2026-08-26 case: proposed Rs 1,000/day, actually Rs 300/day.
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        go_live(ledger_root, rec)
        path = ledger_root / "campaigns" / "w2330" / "record.md"
        _, fm, body = path.read_text().split("---", 2)
        data = yaml.safe_load(fm)
        data.update({"campaign_daily_cap_inr": 300.0, "campaign_caps_verified": "2026-08-26"})
        path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body)
        capsys.readouterr()
        run(["open"])
        out = capsys.readouterr().out
        assert "Rs 300/day effective" in out and "below the Rs 800 floor" in out
        assert "inconclusive, not evidence" in out

    def test_a_verified_absent_cap_is_not_flagged(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        go_live(ledger_root, rec)
        path = ledger_root / "campaigns" / "w2330" / "record.md"
        _, fm, body = path.read_text().split("---", 2)
        data = yaml.safe_load(fm)
        data.update({"campaign_daily_cap_inr": None, "campaign_caps_verified": "2026-08-26"})
        path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body)
        capsys.readouterr()
        run(["open"])
        assert "Funding below the floor" not in capsys.readouterr().out


class TestCreative:
    def test_a_creative_with_no_qa_pass_is_flagged(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        (ledger_root / "creatives" / "test-asset" / "qa.md").write_text("Verdict: `regenerate`\n")
        capsys.readouterr()
        run(["open"])
        assert "not cleared by the QA gate" in capsys.readouterr().out

    def test_a_cleared_creative_nobody_uses_is_flagged(self, ledger_root, capsys):
        spare = ledger_root / "creatives" / "spare-asset"
        spare.mkdir()
        spare.joinpath("qa.md").write_text("Verdict: `pass`\n")
        capsys.readouterr()
        run(["open"])
        out = capsys.readouterr().out
        assert "cleared but never used" in out and "spare-asset" in out

    def test_a_reviewed_record_whose_prompts_carry_no_verdict_is_flagged(
        self, ledger_root, capsys
    ):
        # creative-generation.md sec 9: a prompt with no outcome attached taught nothing.
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        go_live(ledger_root, rec)
        run(["log-review", rec, "--verdict", "not-working", "--summary", "no taps"])
        capsys.readouterr()
        run(["open"])
        assert "never written back to the prompt library" in capsys.readouterr().out

    def test_the_back_edge_clears_once_the_verdict_is_written(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        rec = rec_id_of(ledger_root)
        go_live(ledger_root, rec)
        run(["log-review", rec, "--verdict", "not-working", "--summary", "no taps"])
        prompts = ledger_root / "creatives" / "test-asset" / "prompts.md"
        prompts.write_text(prompts.read_text() + "\n## Verdict: not-working\n")
        capsys.readouterr()
        run(["open"])
        assert "never written back" not in capsys.readouterr().out
