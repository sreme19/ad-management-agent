"""`log-review`'s two back-edges.

rules/creative-generation.md sec 9 requires a verdict to land on the prompt pack;
the research loop requires it to land on the belief that produced the
recommendation. Both were written down as things someone should remember, which
is how they stop happening around run four. These test that neither depends on
anyone remembering.
"""
from __future__ import annotations

import yaml
from conftest import propose_argv, run

from ad_management_agent import cli


def today():
    return cli._today()


def fm_of(root, path):
    return yaml.safe_load((root / path).read_text().split("---")[1])


def learn(slug, subject="audience"):
    return ["learn", "--slug", slug, "--claim", f"claim {slug}", "--subject", subject,
            "--source", "live-data", "--confidence", "high", "--sample-n", "110",
            "--evidence", "20.9% on n=110"]


def chain(root, *, learnings=("broad",), verdict="not-working", summary="4.1% on n=140"):
    """learning(s) -> idea -> propose -> live -> verdict."""
    for slug in learnings:
        run(learn(slug))
    argv = ["idea", "--slug", "widen", "--title", "Widen the band", "--verdict", "recommend",
            "--network", "snap", "--persona", "CASUAL-SELECTIVE", "--est-daily", "1000",
            "--est-days", "5", "--rationale", "untested"]
    for slug in learnings:
        argv += ["--learning", f"lrn-{today()}-{slug}"]
    run(argv)
    run(propose_argv(root, from_idea=f"idea-{today()}-widen"))
    rec = f"rec-{today()}-w2330"
    run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
         "--ad-id", "a"])
    run(["log-review", rec, "--verdict", verdict, "--summary", summary])
    return rec


class TestTheChainIsRecordedBothWays:
    def test_the_record_names_the_idea_it_came_from(self, ledger_root):
        run(["idea", "--slug", "widen", "--title", "W", "--verdict", "recommend",
             "--network", "snap", "--persona", "P", "--est-daily", "1000", "--est-days", "5",
             "--rationale", "r"])
        run(propose_argv(ledger_root, from_idea=f"idea-{today()}-widen"))
        assert fm_of(ledger_root, "campaigns/w2330/record.md")["from_idea"] == \
            f"idea-{today()}-widen"

    def test_a_record_written_before_from_idea_existed_is_still_reachable(self, ledger_root):
        # The idea has always carried rec_id, so the chain can be walked from that
        # end too — which is what makes this work for records already on disk.
        run(learn("broad"))
        run(["idea", "--slug", "widen", "--title", "W", "--verdict", "recommend",
             "--network", "snap", "--persona", "P", "--est-daily", "1000", "--est-days", "5",
             "--rationale", "r", "--learning", f"lrn-{today()}-broad"])
        run(propose_argv(ledger_root, from_idea=f"idea-{today()}-widen"))
        rec = f"rec-{today()}-w2330"
        path = ledger_root / "campaigns" / "w2330" / "record.md"
        path.write_text(path.read_text().replace(f"from_idea: idea-{today()}-widen",
                                                 "from_idea: null"))
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        run(["log-review", rec, "--verdict", "working", "--summary", "held"])
        assert fm_of(ledger_root,
                     f"research/learnings/lrn-{today()}-broad.md")["status"] == "supported"


class TestThePromptLibrary:
    def test_the_outcome_lands_on_the_prompt_pack(self, ledger_root):
        rec = chain(ledger_root)
        text = (ledger_root / "creatives" / "test-asset" / "prompts.md").read_text()
        assert f"## Outcome — {rec}" in text
        assert "**not-working**" in text and "4.1% on n=140" in text

    def test_it_carries_the_audience_so_the_library_is_rankable_by_persona(self, ledger_root):
        chain(ledger_root)
        text = (ledger_root / "creatives" / "test-asset" / "prompts.md").read_text()
        assert "WOMEN_23-30_CASUAL_LPV" in text
        assert "female, 23-30, IN, ANDROID" in text

    def test_it_reports_the_effective_spend_not_the_proposed_one(self, ledger_root):
        run(propose_argv(ledger_root))
        rec = f"rec-{today()}-w2330"
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        path = ledger_root / "campaigns" / "w2330" / "record.md"
        _, fm, body = path.read_text().split("---", 2)
        data = yaml.safe_load(fm)
        data.update({"campaign_daily_cap_inr": 300.0, "campaign_caps_verified": today()})
        path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body)
        run(["log-review", rec, "--verdict", "inconclusive", "--summary", "capped"])
        # Rs 1,000 was proposed; Rs 300 is what actually ran. The library has to
        # record the second, or a weak result reads as a weak creative.
        assert "Rs 300/day" in (
            ledger_root / "creatives" / "test-asset" / "prompts.md").read_text()

    def test_a_missing_prompt_pack_is_reported_not_fatal(self, ledger_root, capsys):
        (ledger_root / "creatives" / "test-asset" / "prompts.md").unlink()
        run(propose_argv(ledger_root))
        rec = f"rec-{today()}-w2330"
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        capsys.readouterr()
        assert run(["log-review", rec, "--verdict", "working", "--summary", "s"]) == 0
        out = capsys.readouterr().out
        assert "does not exist" in out
        assert fm_of(ledger_root, "campaigns/w2330/record.md")["verdict"] == "working"


class TestTheBeliefsBehindIt:
    def test_a_working_verdict_supports_every_learning_the_idea_cited(self, ledger_root):
        chain(ledger_root, learnings=("broad", "android"), verdict="working", summary="held")
        for slug in ("broad", "android"):
            assert fm_of(ledger_root,
                         f"research/learnings/lrn-{today()}-{slug}.md")["status"] == "supported"

    def test_a_failing_verdict_contradicts_them(self, ledger_root):
        chain(ledger_root)
        assert fm_of(ledger_root,
                     f"research/learnings/lrn-{today()}-broad.md")["status"] == "contradicted"

    def test_an_inconclusive_verdict_records_evidence_without_moving_the_belief(
        self, ledger_root
    ):
        # A campaign can be unreadable for reasons that say nothing about the claim —
        # a campaign cap below the floor, broken tracking.
        rec = chain(ledger_root, verdict="inconclusive", summary="capped below the floor")
        fm = fm_of(ledger_root, f"research/learnings/lrn-{today()}-broad.md")
        assert fm["status"] == "open"
        body = (ledger_root / "research" / "learnings" / f"lrn-{today()}-broad.md").read_text()
        assert "capped below the floor" in body and rec in body

    def test_the_record_is_linked_on_the_learning(self, ledger_root):
        rec = chain(ledger_root)
        assert fm_of(ledger_root, f"research/learnings/lrn-{today()}-broad.md")["recs"] == [rec]

    def test_an_extra_learning_can_be_attached_by_hand(self, ledger_root):
        # For a record that predates ideas entirely, like the first live women's set.
        run(learn("sideways"))
        run(propose_argv(ledger_root))
        rec = f"rec-{today()}-w2330"
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        run(["log-review", rec, "--verdict", "working", "--summary", "held",
             "--learning", f"lrn-{today()}-sideways"])
        assert fm_of(ledger_root,
                     f"research/learnings/lrn-{today()}-sideways.md")["status"] == "supported"

    def test_a_verdict_that_updates_no_belief_says_so(self, ledger_root, capsys):
        run(propose_argv(ledger_root))
        rec = f"rec-{today()}-w2330"
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        capsys.readouterr()
        run(["log-review", rec, "--verdict", "working", "--summary", "s"])
        # Silence here would read as "the loop closed". It didn't.
        assert "not linked to any" in capsys.readouterr().out

    def test_a_dangling_learning_reference_warns_without_losing_the_verdict(
        self, ledger_root, capsys
    ):
        run(propose_argv(ledger_root))
        rec = f"rec-{today()}-w2330"
        run(["log-setup", rec, "--network", "snap", "--campaign-id", "c", "--ad-set-id", "s",
             "--ad-id", "a"])
        assert run(["log-review", rec, "--verdict", "working", "--summary", "s",
                    "--learning", "lrn-2020-01-01-nope"]) == 0
        assert "not updated" in capsys.readouterr().err
        assert fm_of(ledger_root, "campaigns/w2330/record.md")["status"] == "reviewed"


class TestOnlySomethingThatRanGetsAVerdict:
    def test_a_proposal_cannot_be_reviewed(self, ledger_root):
        run(propose_argv(ledger_root))
        assert run(["log-review", f"rec-{today()}-w2330", "--verdict", "working",
                    "--summary", "s"]) == 2

    def test_a_record_cannot_be_reviewed_twice(self, ledger_root):
        rec = chain(ledger_root)
        assert run(["log-review", rec, "--verdict", "working", "--summary", "s"]) == 2

    def test_the_second_attempt_points_somewhere_useful(self, ledger_root, capsys):
        rec = chain(ledger_root)
        capsys.readouterr()
        run(["log-review", rec, "--verdict", "working", "--summary", "s"])
        err = capsys.readouterr().err
        assert "`note`" in err and "learning" in err
