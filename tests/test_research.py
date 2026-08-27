"""The research loop: the gates that keep the library honest, and the back-edge.

The store exists because `rules/targeting.md` already carries dated observations
with no source attached, and the live women's record cites one of them to justify
a Rs 5,000 spend. These tests are mostly about the checks that stop that
recurring — a hunch and a measurement must not be citable at the same weight.
"""
from __future__ import annotations

import pytest
import yaml
from conftest import propose_argv, run

from ad_management_agent import cli
from ad_management_agent import research as researchmod


def fm_of(root, kind, item_id):
    sub = {"note": "research/notes", "lrn": "research/learnings",
           "q": "research/questions", "idea": "ideas"}[kind]
    return yaml.safe_load((root / sub / f"{item_id}.md").read_text().split("---")[1])


def today():
    return cli._today()


def ingest(slug="note-a", source="own-research", text="raw material"):
    return ["ingest", "--title", "A note", "--slug", slug, "--source", source, "--text", text]


def learn(slug="claim-a", **over):
    a = {"claim": "Broad targeting beats narrow for LPV", "subject": "audience",
         "source": "live-data", "confidence": "high", "sample-n": "110",
         "evidence": "20.9% tap rate on n=110"}
    a.update({k.replace("_", "-"): v for k, v in over.items()})
    argv = ["learn", "--slug", slug]
    for k, v in a.items():
        if v is not None:
            argv += [f"--{k}", v]
    return argv


def idea(slug="idea-a", **over):
    a = {"title": "Widen the band", "verdict": "recommend", "network": "snap",
         "persona": "CASUAL-SELECTIVE", "est-daily": "1000", "est-days": "5",
         "rationale": "the adjacent band is untested"}
    a.update({k.replace("_", "-"): v for k, v in over.items()})
    argv = ["idea", "--slug", slug]
    for k, v in a.items():
        if v is not None:
            argv += [f"--{k}", v]
    return argv


class TestNotesAreProvenance:
    def test_a_note_is_stored_verbatim(self, ledger_root):
        run(ingest(text="line one\nline two"))
        body = (ledger_root / "research" / "notes" / f"note-{today()}-note-a.md").read_text()
        assert "line one\nline two" in body

    def test_a_note_cannot_be_overwritten(self, ledger_root):
        # The content is the provenance. If it could be rewritten, a claim
        # pointing back at it would prove nothing.
        assert run(ingest()) == 0
        assert run(ingest(text="different material now")) == 2
        body = (ledger_root / "research" / "notes" / f"note-{today()}-note-a.md").read_text()
        assert "raw material" in body

    def test_an_empty_note_is_refused(self, ledger_root):
        assert run(ingest(text="   ")) == 2

    def test_deriving_a_learning_back_links_the_note(self, ledger_root):
        run(ingest())
        run(learn(derived_from=f"note-{today()}-note-a"))
        assert fm_of(ledger_root, "note", f"note-{today()}-note-a")["learnings"] == [
            f"lrn-{today()}-claim-a"]

    def test_derived_from_must_name_a_note(self, ledger_root):
        run(ingest())
        run(learn("first"))
        assert run(learn("second", derived_from=f"lrn-{today()}-first")) == 2


class TestConfidenceIsGatedNotSelfDeclared:
    @pytest.mark.parametrize("source", ["own-research", "competitor-observation", "intuition"])
    def test_a_hypothesis_cannot_be_high_confidence(self, ledger_root, source):
        assert run(learn(source=source, confidence="high", sample_n=None)) == 2

    @pytest.mark.parametrize("source", ["live-data", "platform-doc"])
    def test_a_measurement_or_a_doc_can_be(self, ledger_root, source):
        n = "110" if source == "live-data" else None
        assert run(learn(f"c-{source}", source=source, confidence="high", sample_n=n)) == 0

    def test_a_hypothesis_at_medium_is_fine(self, ledger_root):
        assert run(learn(source="intuition", confidence="medium", sample_n=None)) == 0

    def test_live_data_must_state_its_sample_size(self, ledger_root):
        # SPEC.md decision #6: a sample that is not written down cannot be checked
        # against MIN_SAMPLE.
        assert run(learn(sample_n=None)) == 2

    def test_below_min_sample_it_can_only_be_low(self, ledger_root):
        assert run(learn(sample_n="12", confidence="high")) == 2
        assert run(learn(sample_n="12", confidence="medium")) == 2
        assert run(learn(sample_n="12", confidence="low")) == 0

    def test_the_floor_matches_pocket_dating_coachs(self):
        assert researchmod.MIN_SAMPLE == 30


class TestSourceCode:
    """Added 2026-08-26: reading a function is as certain as reading a doc."""

    def test_a_code_claim_can_be_high_confidence(self, ledger_root):
        assert run(learn(source="source-code", confidence="high", sample_n=None)) == 0

    def test_it_goes_stale_faster_than_a_platform_doc(self, ledger_root):
        # Certain when read, but it describes something someone is actively changing.
        run(learn("code", source="source-code", confidence="high", sample_n=None))
        run(learn("doc", source="platform-doc", confidence="high", sample_n=None))
        code = fm_of(ledger_root, "lrn", f"lrn-{today()}-code")
        doc = fm_of(ledger_root, "lrn", f"lrn-{today()}-doc")
        assert code["review_after"] < doc["review_after"]

    def test_it_needs_no_sample_size(self, ledger_root):
        assert run(learn(source="source-code", confidence="high", sample_n=None)) == 0


class TestReclassify:
    """Correcting how a claim is filed, without touching what it claims."""

    def test_it_moves_source_and_confidence_together(self, ledger_root):
        run(learn(source="own-research", confidence="medium", sample_n=None))
        lrn = f"lrn-{today()}-claim-a"
        assert run(["reclassify", lrn, "--reason", "no source-code kind existed then",
                    "--source", "source-code", "--confidence", "high"]) == 0
        fm = fm_of(ledger_root, "lrn", lrn)
        assert fm["source"] == "source-code" and fm["confidence"] == "high"

    def test_the_correction_is_recorded_in_the_body(self, ledger_root):
        run(learn(source="own-research", confidence="medium", sample_n=None))
        lrn = f"lrn-{today()}-claim-a"
        run(["reclassify", lrn, "--reason", "wrongly filed", "--source", "source-code"])
        body = (ledger_root / "research" / "learnings" / f"{lrn}.md").read_text()
        assert "## Reclassified" in body and "wrongly filed" in body
        assert "'own-research' -> 'source-code'" in body

    def test_it_runs_the_same_confidence_gate(self, ledger_root):
        # Reclassifying must not be a way around the gate that `learn` enforces.
        run(learn(source="source-code", confidence="high", sample_n=None))
        lrn = f"lrn-{today()}-claim-a"
        assert run(["reclassify", lrn, "--reason", "r", "--source", "intuition"]) == 2
        assert fm_of(ledger_root, "lrn", lrn)["source"] == "source-code"

    def test_moving_to_live_data_demands_a_sample_size(self, ledger_root):
        run(learn(source="own-research", confidence="medium", sample_n=None))
        lrn = f"lrn-{today()}-claim-a"
        assert run(["reclassify", lrn, "--reason", "r", "--source", "live-data"]) == 2
        assert run(["reclassify", lrn, "--reason", "r", "--source", "live-data",
                    "--sample-n", "110", "--confidence", "high"]) == 0

    def test_the_review_clock_follows_the_new_source(self, ledger_root):
        run(learn(source="platform-doc", confidence="high", sample_n=None))
        lrn = f"lrn-{today()}-claim-a"
        before = fm_of(ledger_root, "lrn", lrn)["review_after"]
        run(["reclassify", lrn, "--reason", "r", "--source", "competitor-observation",
             "--confidence", "medium"])
        # Recomputed from last_confirmed, not today — re-filing is not reconfirming.
        assert fm_of(ledger_root, "lrn", lrn)["review_after"] < before

    def test_the_claim_itself_cannot_be_changed(self):
        # Evidence already attached was gathered against the claim as written.
        import inspect

        from ad_management_agent import research
        assert "claim" not in inspect.signature(research.Research.reclassify).parameters

    def test_passing_nothing_is_an_error(self, ledger_root):
        run(learn())
        assert run(["reclassify", f"lrn-{today()}-claim-a", "--reason", "r"]) == 2

    def test_it_refuses_anything_that_is_not_a_learning(self, ledger_root):
        run(ingest())
        assert run(["reclassify", f"note-{today()}-note-a", "--reason", "r",
                    "--source", "source-code"]) == 2


class TestOneClaimPerFile:
    def test_a_duplicate_id_is_refused_and_points_at_log_evidence(self, ledger_root, capsys):
        run(learn())
        assert run(learn()) == 2
        assert "log-evidence" in capsys.readouterr().err

    def test_siblings_on_the_same_subject_are_surfaced(self, ledger_root, capsys):
        run(learn("first", claim="Broad beats narrow"))
        capsys.readouterr()
        run(learn("second", claim="Android outperforms iOS"))
        out = capsys.readouterr().out
        assert "existing learning(s) on `audience`" in out
        assert f"lrn-{today()}-first" in out

    def test_staleness_is_set_from_the_source(self, ledger_root):
        run(learn("fast", source="competitor-observation", confidence="medium", sample_n=None))
        run(learn("slow", source="platform-doc", confidence="high", sample_n=None))
        fast = fm_of(ledger_root, "lrn", f"lrn-{today()}-fast")
        slow = fm_of(ledger_root, "lrn", f"lrn-{today()}-slow")
        # Competitor creative rots faster than a documented platform behaviour.
        assert fast["review_after"] < slow["review_after"]


class TestTheBackEdge:
    """Without this the library only ever grows and never corrects itself."""

    def setup_learning(self):
        run(learn())
        return f"lrn-{today()}-claim-a"

    def test_supported_moves_an_open_claim(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "held on a second set"])
        assert fm_of(ledger_root, "lrn", lrn)["status"] == "supported"

    def test_contradicted_moves_an_open_claim(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "contradicted", "--text", "4% tap rate"])
        assert fm_of(ledger_root, "lrn", lrn)["status"] == "contradicted"

    def test_disagreeing_outcomes_make_it_mixed_not_the_latest_one(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "a"])
        run(["log-evidence", lrn, "--outcome", "contradicted", "--text", "b"])
        assert fm_of(ledger_root, "lrn", lrn)["status"] == "mixed"

    def test_inconclusive_leaves_the_status_alone_but_is_recorded(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "a"])
        run(["log-evidence", lrn, "--outcome", "inconclusive", "--text", "n too small"])
        assert fm_of(ledger_root, "lrn", lrn)["status"] == "supported"
        assert "n too small" in (
            ledger_root / "research" / "learnings" / f"{lrn}.md").read_text()

    def test_support_resets_the_review_clock(self, ledger_root):
        lrn = self.setup_learning()
        before = fm_of(ledger_root, "lrn", lrn)["review_after"]
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "still true"])
        assert fm_of(ledger_root, "lrn", lrn)["last_confirmed"] == today()
        assert fm_of(ledger_root, "lrn", lrn)["review_after"] >= before

    def test_the_originating_record_is_linked_back(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "contradicted", "--text", "x",
             "--from", "rec-2026-08-21-women-1822-casual-lpv"])
        assert fm_of(ledger_root, "lrn", lrn)["recs"] == [
            "rec-2026-08-21-women-1822-casual-lpv"]

    def test_evidence_accumulates_and_never_rewrites(self, ledger_root):
        lrn = self.setup_learning()
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "first outcome"])
        run(["log-evidence", lrn, "--outcome", "supported", "--text", "second outcome"])
        body = (ledger_root / "research" / "learnings" / f"{lrn}.md").read_text()
        assert "first outcome" in body and "second outcome" in body

    def test_a_retired_claim_takes_no_more_evidence(self, ledger_root):
        lrn = self.setup_learning()
        run(["retire", lrn, "--reason", "superseded"])
        assert run(["log-evidence", lrn, "--outcome", "supported", "--text", "x"]) == 2


class TestPromotion:
    def test_promoting_records_which_rule_now_carries_it(self, ledger_root):
        run(learn())
        lrn = f"lrn-{today()}-claim-a"
        assert run(["promote", lrn, "--rule", "rules/targeting.md"]) == 0
        fm = fm_of(ledger_root, "lrn", lrn)
        assert fm["status"] == "promoted" and fm["promoted_to"] == "rules/targeting.md"

    def test_it_must_be_a_rules_file_that_exists(self, ledger_root):
        run(learn())
        assert run(["promote", f"lrn-{today()}-claim-a", "--rule", "rules/invented.md"]) == 2


class TestQuestions:
    def ask(self, slug="q-a"):
        return ["question", "--slug", slug, "--kind", "channel",
                "--text", "Does Truecaller skew male?", "--why", "it decides a channel"]

    def test_asking_and_answering(self, ledger_root):
        run(self.ask())
        qid = f"q-{today()}-q-a"
        assert fm_of(ledger_root, "q", qid)["status"] == "open"
        run(["answer", qid, "--text", "No published split found"])
        assert fm_of(ledger_root, "q", qid)["status"] == "answered"

    def test_the_same_question_cannot_be_asked_twice(self, ledger_root):
        run(self.ask())
        assert run(self.ask()) == 2

    def test_a_closed_question_cannot_be_answered_again(self, ledger_root):
        run(self.ask())
        qid = f"q-{today()}-q-a"
        run(["answer", qid, "--text", "first"])
        assert run(["answer", qid, "--text", "second"]) == 2

    def test_dropping_is_a_distinct_close(self, ledger_root):
        run(self.ask())
        qid = f"q-{today()}-q-a"
        run(["answer", qid, "--text", "no longer relevant", "--dropped"])
        assert fm_of(ledger_root, "q", qid)["status"] == "dropped"

    def test_a_bad_learning_reference_leaves_the_question_untouched(self, ledger_root):
        # It used to close the question, then raise — leaving it `answered` with no
        # learning while the caller saw an error and assumed nothing had happened.
        run(self.ask())
        qid = f"q-{today()}-q-a"
        assert run(["answer", qid, "--text", "x", "--learning", "lrn-2020-01-01-nope"]) == 2
        assert fm_of(ledger_root, "q", qid)["status"] == "open"

    def test_a_learning_can_close_the_question_it_answers(self, ledger_root):
        run(self.ask())
        qid = f"q-{today()}-q-a"
        run(learn(source="own-research", confidence="medium", sample_n=None, answers=qid))
        assert fm_of(ledger_root, "q", qid)["status"] == "answered"
        assert fm_of(ledger_root, "q", qid)["learning"] == f"lrn-{today()}-claim-a"
        assert fm_of(ledger_root, "lrn", f"lrn-{today()}-claim-a")["questions"] == [qid]


class TestIdeas:
    def test_a_hold_must_say_what_would_change_it(self, ledger_root):
        # Otherwise it is indistinguishable from a no, and sits in the queue forever.
        assert run(idea(verdict="hold")) == 2
        assert run(idea(verdict="hold", blocked_on="a measured gender split")) == 0

    def test_the_total_spend_is_computed_not_asserted(self, ledger_root):
        run(idea(est_daily="1200", est_days="4"))
        assert fm_of(ledger_root, "idea", f"idea-{today()}-idea-a")["est_total_inr"] == 4800

    def test_an_unknown_learning_reference_is_refused(self, ledger_root):
        assert run(idea(learning="lrn-2020-01-01-nope")) == 2

    def test_a_thin_budget_still_records_but_warns(self, ledger_root, capsys):
        # Rs 300 became the accepted DEFAULT on 2026-08-28, but the warning stays:
        # rules/budget.md keeps Rs 800-1,200 as the full-experiment threshold, and a
        # read under it is directional. Recording at 300 is fine; recording it
        # silently is not.
        assert run(idea(est_daily="300")) == 0
        err = capsys.readouterr().err
        assert "full-experiment threshold" in err and "directional" in err


class TestIdeaToProposal:
    def test_proposing_from_an_idea_closes_it(self, ledger_root):
        run(idea())
        iid = f"idea-{today()}-idea-a"
        assert run(propose_argv(ledger_root, from_idea=iid)) == 0
        fm = fm_of(ledger_root, "idea", iid)
        assert fm["status"] == "proposed"
        assert fm["rec_id"] == f"rec-{today()}-w2330"

    def test_the_same_idea_cannot_be_proposed_twice(self, ledger_root, capsys):
        run(idea())
        iid = f"idea-{today()}-idea-a"
        run(propose_argv(ledger_root, from_idea=iid))
        # The second proposal is still written — the ledger is the source of truth
        # and refusing it would lose real work — but the failure is reported.
        assert run(propose_argv(ledger_root, from_idea=iid)) == 0
        assert "was not closed" in capsys.readouterr().err

    def test_an_unknown_idea_warns_without_losing_the_proposal(self, ledger_root, capsys):
        assert run(propose_argv(ledger_root, from_idea="idea-2020-01-01-nope")) == 0
        assert (ledger_root / "campaigns" / "w2330" / "record.md").exists()
        assert "was not closed" in capsys.readouterr().err


class TestOpenSurfacesTheResearchLoop:
    def test_an_unanswered_question(self, ledger_root, capsys):
        run(["question", "--slug", "q-a", "--kind", "channel", "--text", "t", "--why", "w"])
        capsys.readouterr()
        run(["open"])
        assert "Open research questions" in capsys.readouterr().out

    def test_a_note_nobody_derived_anything_from(self, ledger_root, capsys):
        run(ingest())
        capsys.readouterr()
        run(["open"])
        assert "no learning derived" in capsys.readouterr().out

    def test_that_clears_once_a_learning_is_derived(self, ledger_root, capsys):
        run(ingest())
        run(learn(derived_from=f"note-{today()}-note-a"))
        capsys.readouterr()
        run(["open"])
        assert "no learning derived" not in capsys.readouterr().out

    def test_a_recommended_idea_nobody_proposed(self, ledger_root, capsys):
        run(idea())
        capsys.readouterr()
        run(["open"])
        assert "recommended but never proposed" in capsys.readouterr().out

    def test_a_hold_is_not_reported_as_unproposed(self, ledger_root, capsys):
        run(idea(verdict="hold", blocked_on="a measured gender split"))
        capsys.readouterr()
        run(["open"])
        assert "recommended but never proposed" not in capsys.readouterr().out

    def test_a_stale_learning(self, ledger_root, capsys):
        run(learn("old", source="competitor-observation", confidence="medium", sample_n=None))
        path = ledger_root / "research" / "learnings" / f"lrn-{today()}-old.md"
        path.write_text(path.read_text().replace(
            f"review_after: '{yaml.safe_load(path.read_text().split('---')[1])['review_after']}'",
            "review_after: '2020-01-01'"))
        capsys.readouterr()
        run(["open"])
        assert "past their review date" in capsys.readouterr().out

    def test_a_fresh_learning_is_not_nagged_about(self, ledger_root, capsys):
        run(learn())
        capsys.readouterr()
        run(["open"])
        assert "never tested" not in capsys.readouterr().out

    def test_an_untested_learning_surfaces_after_the_grace_period(self, ledger_root, capsys):
        run(learn())
        path = ledger_root / "research" / "learnings" / f"lrn-{today()}-claim-a.md"
        path.write_text(path.read_text().replace(f"created: '{today()}'", "created: '2026-01-01'"))
        capsys.readouterr()
        run(["open"])
        assert "never tested" in capsys.readouterr().out

    def test_a_contradicted_claim_names_what_still_leans_on_it(self, ledger_root, capsys):
        run(learn())
        lrn = f"lrn-{today()}-claim-a"
        run(idea(learning=lrn))
        run(["log-evidence", lrn, "--outcome", "contradicted", "--text", "x",
             "--from", "rec-2026-08-21-women-1822-casual-lpv"])
        capsys.readouterr()
        run(["open"])
        out = capsys.readouterr().out
        assert "contradicted by a real outcome" in out
        assert "still cited by" in out and f"idea-{today()}-idea-a" in out

    def test_a_contradicted_claim_still_in_a_rules_file_is_the_loudest(self, ledger_root, capsys):
        run(learn())
        lrn = f"lrn-{today()}-claim-a"
        run(["promote", lrn, "--rule", "rules/targeting.md"])
        run(["log-evidence", lrn, "--outcome", "contradicted", "--text", "x"])
        capsys.readouterr()
        run(["open"])
        assert "still normative in rules/targeting.md" in capsys.readouterr().out
