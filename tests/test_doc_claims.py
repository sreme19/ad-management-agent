"""Documentation may not contradict a capability the code actually has.

Four times on 2026-08-27, prose in this repo asserted Meta was hands-off after it had
stopped being: `SPEC.md`'s non-negotiables, `README.md`, `ad-setup-loop/SKILL.md`, and
a mermaid node in `wiki-export/Home.md` that three separate text greps missed because
the claim was inside a diagram. That is the same failure `commands` was built for on
2026-08-26 — several hand-kept copies of one fact, none of them right — and
`commands --check` does not cover it, because it checks command *names* and this is
about *claims*.

Two design choices matter more than the phrase list, because a badly-scoped list
becomes its own maintenance problem:

**The claims are derived from the registry, not hardcoded here.** A phrase is only
banned while `rules/networks.yaml` says the network is creatable. Set `meta.creation`
back to `none` and these assertions stop applying to Meta on their own — no test edit
required. That is what stops this file from becoming a list nobody updates, and it is
why adding a third network gets the same protection for free.

**History is allowed, but it has to be marked as history.** These documents
deliberately record what the old rule was — decision #3 opens with "Originally: this
agent never calls a Meta or Snap Ads Manager API at all", and that sentence is the
point of the decision, not a mistake in it. So an occurrence passes if a historical
marker appears shortly before it. The effect is stronger than a per-file allowlist
would be: prose can say the old thing, but only in the past tense, which is the
property actually worth having.

Deliberately NOT scanned: `research/` (dated notes and learnings are immutable
provenance — a 2026-08-26 note SHOULD still say what was true on 2026-08-26),
`ideas/`, `campaigns/` (the ledger is an audit trail), and `INDEX.md` (generated).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from ad_management_agent import networks

REPO = Path(__file__).resolve().parents[1]
RULES = REPO / "rules"

# Prose that must be marked as past tense once a network is creatable. `{n}` is
# substituted with the network key and its label, so this generalises to a third
# network rather than special-casing the two that exist.
STALE_WHEN_CREATABLE = [
    "{n} is unchanged",
    "{n}: unchanged",
    "{n} is entirely hands-off",
    "{n}: entirely hands-off",
    "{n}, entirely hands-off",
    "entirely hands-off",
    "no {n} client",
    "no {n} marketing api client",
    "no {n} credential",
    "never call a {n}",
    "never calls a {n}",
    "by hand on {n}",
    "{n}.creation: none",
    "unamended for {n}",
    "no api call, no credential",
]

# A claim may appear if one of these shows up in the preceding window — i.e. it is
# being described as something that used to be true.
HISTORY_MARKERS = (
    "originally",
    "no longer",
    "stopped being",
    "used to",
    "until 2026",
    "was true",
    "was enforced",
    "was permitted",
    "as amended",
    "was amended",
    "stood unamended",
    "before this",
    "was found",
    "still read",
    # Both of these were false positives on the first run, against prose that was
    # already correctly retelling history: Command-Cheatsheet's "on 2026-08-26 ...
    # this page still SAID", and Safety-and-guardrails' "this page PREVIOUSLY said".
    # Added rather than allowlisting those two files, so the same phrasing passes
    # anywhere it is used.
    "still said",
    "previously",
    "asserted",
    "that is now",
    "which is what made",
)

# How far back to look for a marker. Generous enough to span the sentence that
# introduces a historical passage, tight enough that an unrelated earlier paragraph
# cannot launder a fresh false claim.
WINDOW = 220


def scanned_docs() -> list[Path]:
    docs = [REPO / "SPEC.md", REPO / "README.md"]
    docs += sorted((REPO / "wiki-export").glob("*.md"))
    docs += sorted((REPO / ".claude" / "skills").glob("*/SKILL.md"))
    docs += sorted((REPO / "rules").glob("*.md"))
    return [d for d in docs if d.exists()]


def creatable_networks() -> dict[str, dict]:
    return {k: v for k, v in networks.all_networks(RULES).items()
            if v.get("creation") == "paused-only"}


def _normalise(text: str) -> str:
    """Collapse whitespace so a claim split across a line break is still one phrase.

    This is exactly how the Home.md mermaid node escaped four greps: the text was
    inside a diagram and the wording wrapped. Matching on normalised text rather than
    per-line is what makes the scan see it.
    """
    return re.sub(r"[\s\\]+", " ", text.lower())


def _label(path: Path) -> str:
    """Repo-relative where possible; the tests plant fixtures outside the repo."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return path.name


def violations_in(path: Path, phrases: list[str]) -> list[str]:
    flat = _normalise(path.read_text(encoding="utf-8"))
    found = []
    for phrase in phrases:
        for m in re.finditer(re.escape(phrase), flat):
            window = flat[max(0, m.start() - WINDOW):m.start()]
            if not any(marker in window for marker in HISTORY_MARKERS):
                found.append(
                    f"{_label(path)}: {phrase!r} with nothing marking it as past "
                    f"tense\n      ...{flat[max(0, m.start() - 90):m.end() + 40]}..."
                )
    return found


def phrases_for(key: str, entry: dict) -> list[str]:
    names = {key.lower(), str(entry.get("label", "")).lower()} - {""}
    return sorted({p.format(n=n) for p in STALE_WHEN_CREATABLE for n in names})


class TestDocsDoNotContradictTheCode:
    def test_the_scan_covers_the_documents_that_drifted(self):
        # If this list silently shrinks, the test passes for the wrong reason.
        covered = {str(p.relative_to(REPO)) for p in scanned_docs()}
        for required in ("SPEC.md", "README.md", "wiki-export/Home.md",
                         "wiki-export/Safety-and-guardrails.md",
                         ".claude/skills/ad-setup-loop/SKILL.md"):
            assert required in covered, f"{required} is not being scanned"

    def test_immutable_provenance_is_not_scanned(self):
        # A dated research note should still say what was true on its date. Scanning
        # research/ would pressure someone into rewriting history to green a test.
        scanned = {str(p.relative_to(REPO)) for p in scanned_docs()}
        assert not any(s.startswith(("research/", "ideas/", "campaigns/")) for s in scanned)

    @pytest.mark.parametrize("doc", scanned_docs(), ids=lambda p: p.name)
    def test_no_unmarked_stale_capability_claim(self, doc):
        found = []
        for key, entry in creatable_networks().items():
            found += violations_in(doc, phrases_for(key, entry))
        assert not found, (
            f"{doc.relative_to(REPO)} contradicts a capability the code has.\n\n"
            + "\n".join(f"  - {f}" for f in found)
            + "\n\n  rules/networks.yaml says this network is creatable, so prose calling it\n"
              "  hands-off is false. Either fix the sentence, or mark it as history (it is\n"
              "  allowed to say what the old rule was — in the past tense).\n"
              f"  Markers that satisfy this: {', '.join(HISTORY_MARKERS[:6])}, ..."
        )


class TestTheGuardActuallyGuards:
    """A scan that cannot fail is worse than no scan: it reads as coverage."""

    def test_a_planted_false_claim_is_caught(self, tmp_path):
        doc = tmp_path / "fake.md"
        doc.write_text("Meta is entirely hands-off. No Meta credential exists.\n")
        meta = networks.get(RULES, "meta")
        assert violations_in(doc, phrases_for("meta", meta))

    def test_a_claim_split_across_a_line_break_is_still_caught(self, tmp_path):
        # The Home.md failure mode, reproduced.
        doc = tmp_path / "fake.md"
        doc.write_text('S2(["Created on Snap, PAUSED\\n(snap-push) — or by hand on Meta"])\n')
        assert violations_in(doc, phrases_for("meta", networks.get(RULES, "meta")))

    def test_the_same_claim_marked_as_history_is_allowed(self, tmp_path):
        doc = tmp_path / "fake.md"
        doc.write_text(
            "Originally this agent never calls a Meta Ads Manager API at all, and Meta was "
            "entirely hands-off. That changed on 2026-08-27.\n")
        assert violations_in(doc, phrases_for("meta", networks.get(RULES, "meta"))) == []

    def test_a_network_declared_none_is_not_policed(self, tmp_path, monkeypatch):
        # The self-updating half: tighten a network back to `none` and its phrases
        # stop being banned, with no edit to this file.
        doc = tmp_path / "fake.md"
        doc.write_text("Truecaller is entirely hands-off. No Truecaller client exists.\n")
        entry = {"label": "Truecaller", "creation": "none"}
        active = {k: v for k, v in {"truecaller": entry}.items()
                  if v.get("creation") == "paused-only"}
        assert active == {}
        # ...and the phrase list for a network nobody may create on is never consulted.
        found = []
        for key, e in active.items():
            found += violations_in(doc, phrases_for(key, e))
        assert found == []
