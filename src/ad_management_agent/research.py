"""The research loop's stores: notes, learnings, questions, ideas.

Deliberately not `rules/`. Everything under `rules/` is **normative** — a skill
reads it and obeys. What lives here is **evidence and hypotheses**: dated,
sourced, revisable, sometimes contradicted by the next thing that arrives.
Mixing the two is what was already starting to happen — `rules/targeting.md`
carries inline parentheticals like "the Aug 9 note records that feminist-coded
copy tests well," and the live women's record cites that note as part of the
justification for a Rs 5,000 spend, with no way to find out whether it came from
a real test, a competitor screenshot, or a hunch.

**Precedence is one-directional and absolute: rules win.** Nothing here is a
constraint. A learning becomes normative only by a human promoting it into a
rules file, which is a decision, not a status change. See research/README.md.

Four stores, because they answer four different questions:

  notes/      what someone actually brought in, verbatim and immutable — the
              provenance a derived claim points back at
  learnings/  one claim per file, carrying its source kind and confidence
  questions/  the open-question queue, which is what makes research a loop
              rather than an errand
  ideas/      a proposal-shaped hypothesis with a verdict and a stated spend

The back-edge from a campaign verdict to the learning that spawned it is what
stops this being a pile that only ever grows. `log-evidence` is where it lands.
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from .ledger import Record, slugify

# --- vocabularies ---------------------------------------------------------

SUBJECTS = ("audience", "creative", "channel", "tracking", "competitor", "product", "budget")

# Where a claim came from. This is the field that stops a hunch and a measured
# result being cited at the same weight in a brief.
SOURCES = (
    "live-data",              # this account's own numbers, via ad-audit
    "platform-doc",           # Snap/Meta documentation or an official changelog
    "own-research",           # the app owner's own reading and field notes
    "competitor-observation", # what a rival is visibly doing
    "intuition",              # a hypothesis worth testing, honestly labelled
)

CONFIDENCES = ("high", "medium", "low")

# Only a measured result or an authoritative document can carry `high`. Everything
# else is a hypothesis, however plausible — capping it here is what makes the
# library's own confidence field mean something.
HIGH_CONFIDENCE_SOURCES = ("live-data", "platform-doc")

LEARNING_STATUSES = ("open", "supported", "contradicted", "mixed", "promoted", "retired")
QUESTION_STATUSES = ("open", "answered", "dropped")
IDEA_VERDICTS = ("recommend", "hold")
IDEA_STATUSES = ("open", "proposed", "dropped")
OUTCOMES = ("supported", "contradicted", "inconclusive")

# SPEC.md decision #6, inherited from pocket-dating-coach's ad-analytics.ts. A
# live-data claim under this sample is not a finding, whatever it looks like.
MIN_SAMPLE = 30

# How long a claim stays trustworthy without being reconfirmed. Competitor
# creative rots fastest; a platform behaviour lasts longer; nothing lasts forever.
STALENESS_DAYS = {
    "competitor-observation": 60,
    "intuition": 90,
    "own-research": 120,
    "live-data": 120,
    "platform-doc": 180,
}


class ResearchError(ValueError):
    """Raised when a research write would be malformed, duplicated, or dishonest."""


def _add_days(day: str, n: int) -> str:
    return (_dt.date.fromisoformat(day) + _dt.timedelta(days=n)).isoformat()


def _short(text: str, words: int = 5) -> str:
    """A readable slug from the first few words.

    Short on purpose: these ids get typed by hand into `log-evidence` and
    `--from-idea`. Pass an explicit `--slug` when the first few words do not
    identify the claim well.
    """
    return slugify(" ".join(re.sub(r"[^\w\s-]", " ", text).split()[:words])) or "item"


class Research:
    """File-backed stores. Every method is a deterministic read or write."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.notes_dir = self.root / "research" / "notes"
        self.learnings_dir = self.root / "research" / "learnings"
        self.questions_dir = self.root / "research" / "questions"
        self.ideas_dir = self.root / "ideas"

    def _ensure(self, d: Path) -> Path:
        d.mkdir(parents=True, exist_ok=True)
        return d

    # --- generic loading --------------------------------------------------
    def _all(self, d: Path) -> list[Record]:
        if not d.exists():
            return []
        return [Record.load(p) for p in sorted(d.glob("*.md"))]

    def notes(self) -> list[Record]:
        return self._all(self.notes_dir)

    def learnings(self) -> list[Record]:
        return self._all(self.learnings_dir)

    def questions(self) -> list[Record]:
        return self._all(self.questions_dir)

    def ideas(self) -> list[Record]:
        return self._all(self.ideas_dir)

    def find(self, item_id: str) -> Record:
        for store in (self.notes(), self.learnings(), self.questions(), self.ideas()):
            for rec in store:
                if rec.front_matter.get("id") == item_id:
                    return rec
        raise KeyError(f"no research item with id {item_id!r}")

    # --- notes: raw, verbatim, immutable ----------------------------------
    def ingest(self, *, title: str, text: str, source: str, today: str,
               slug: str | None = None) -> Record:
        """Store a note exactly as brought in. Never edited afterwards.

        The content is the provenance. If it could be rewritten, a derived claim
        pointing at it would prove nothing — which is the whole problem with
        "the Aug 9 note" as it currently exists.
        """
        if source not in SOURCES:
            raise ResearchError(f"source must be one of {', '.join(SOURCES)}, got {source!r}")
        if not text.strip():
            raise ResearchError("an empty note has no provenance to offer; pass --text or --file")

        note_id = f"note-{today}-{slugify(slug) if slug else _short(title)}"
        path = self._ensure(self.notes_dir) / f"{note_id}.md"
        if path.exists():
            raise ResearchError(
                f"{note_id} already exists and notes are immutable.\n"
                "Ingest the new material under its own title — a note is a record of what was\n"
                "brought in on a day, not a document to keep editing."
            )
        fm = {
            "id": note_id,
            "title": title,
            "source": source,
            "captured": today,
            "learnings": [],
        }
        rec = Record(path=path, front_matter=fm, body=f"\n{text.rstrip()}\n")
        rec.save()
        return rec

    # --- learnings: one claim per file ------------------------------------
    def learn(
        self,
        *,
        claim: str,
        subject: str,
        source: str,
        confidence: str,
        sample_n: int | None,
        evidence: str,
        derived_from: str | None,
        answers: str | None,
        today: str,
        slug: str | None = None,
    ) -> Record:
        if subject not in SUBJECTS:
            raise ResearchError(f"subject must be one of {', '.join(SUBJECTS)}, got {subject!r}")
        if source not in SOURCES:
            raise ResearchError(f"source must be one of {', '.join(SOURCES)}, got {source!r}")
        if confidence not in CONFIDENCES:
            raise ResearchError(f"confidence must be one of {', '.join(CONFIDENCES)}")

        # The confidence gate. Two rules, both about not letting a guess and a
        # measurement sit at the same weight in a brief that spends money.
        if confidence == "high" and source not in HIGH_CONFIDENCE_SOURCES:
            raise ResearchError(
                f"a {source!r} claim cannot be `high` confidence.\n"
                f"Only {' or '.join(HIGH_CONFIDENCE_SOURCES)} can — everything else is a hypothesis\n"
                "worth testing, however plausible. Use `medium` and let a test earn the upgrade."
            )
        if source == "live-data":
            if sample_n is None:
                raise ResearchError(
                    "a live-data claim needs --sample-n. SPEC.md decision #6 gates every claim "
                    "about live performance on pocket-dating-coach's own MIN_SAMPLE floor, and a "
                    "sample size that is not written down cannot be checked against it."
                )
            if sample_n < MIN_SAMPLE and confidence != "low":
                raise ResearchError(
                    f"n={sample_n} is below MIN_SAMPLE={MIN_SAMPLE}, so this is `inconclusive`, "
                    f"not a finding (SPEC.md decision #6).\nRecord it as `low` confidence, or as "
                    "an open question, rather than as something a brief can lean on."
                )

        if derived_from is not None:
            note = self.find(derived_from)
            if not note.front_matter.get("id", "").startswith("note-"):
                raise ResearchError(f"--derived-from expects a note id, got {derived_from!r}")

        learning_id = f"lrn-{today}-{slugify(slug) if slug else _short(claim)}"
        path = self._ensure(self.learnings_dir) / f"{learning_id}.md"
        if path.exists():
            raise ResearchError(
                f"{learning_id} already exists.\n"
                "If this is the same claim with new evidence, that is `log-evidence`, not a second\n"
                "atom — two files making the same claim is how a library stops being able to say\n"
                "what it believes."
            )

        fm = {
            "id": learning_id,
            "subject": subject,
            "claim": claim,
            "source": source,
            "confidence": confidence,
            "sample_n": sample_n,
            "status": "open",
            "created": today,
            "last_confirmed": today,
            "review_after": _add_days(today, STALENESS_DAYS[source]),
            "derived_from": derived_from,
            "questions": [],
            "recs": [],
            "promoted_to": None,
        }
        body = (
            f"\n## Claim\n\n{claim.strip()}\n"
            f"\n## Evidence\n\n- ({today}) {evidence.strip()}\n"
        )
        rec = Record(path=path, front_matter=fm, body=body)
        rec.save()

        if derived_from is not None:
            note = self.find(derived_from)
            note.front_matter.setdefault("learnings", []).append(learning_id)
            note.save()
        if answers is not None:
            self.answer(answers, text=f"Answered by {learning_id}: {claim}",
                        learning=learning_id, today=today)
        return rec

    def log_evidence(
        self,
        learning_id: str,
        *,
        outcome: str,
        text: str,
        from_ref: str | None,
        today: str,
    ) -> Record:
        """Attach a dated outcome to a learning, and move its status.

        This is the back-edge. Without it the library only ever grows and never
        corrects itself, which is the failure mode — a store that confidently
        records wrong things is worse than no store.
        """
        if outcome not in OUTCOMES:
            raise ResearchError(f"outcome must be one of {', '.join(OUTCOMES)}, got {outcome!r}")
        rec = self.find(learning_id)
        if not learning_id.startswith("lrn-"):
            raise ResearchError(f"{learning_id!r} is not a learning")
        if rec.front_matter.get("status") == "retired":
            raise ResearchError(
                f"{learning_id} is retired. Evidence about a retired claim belongs on whatever "
                "replaced it, or in a new atom."
            )

        was = rec.front_matter.get("status", "open")
        if outcome == "inconclusive":
            now = was
        elif was in ("open", outcome):
            now = outcome
        else:
            # supported meeting contradicted, in either order.
            now = "mixed"

        rec.front_matter["status"] = now
        if outcome == "supported":
            rec.front_matter["last_confirmed"] = today
            rec.front_matter["review_after"] = _add_days(
                today, STALENESS_DAYS[rec.front_matter.get("source", "own-research")]
            )
        if from_ref and from_ref.startswith("rec-"):
            recs = rec.front_matter.setdefault("recs", []) or []
            if from_ref not in recs:
                recs.append(from_ref)
            rec.front_matter["recs"] = recs

        origin = f" (from {from_ref})" if from_ref else ""
        rec.body = rec.body.rstrip() + f"\n- ({today}) **{outcome}**{origin}: {text.strip()}\n"
        rec.save()
        return rec

    def promote(self, learning_id: str, *, rule_file: str, today: str) -> Record:
        """Mark a learning as having graduated into a rules file.

        The edit to the rule itself is a human/skill decision made in the file;
        this only records that it happened, so the learning stops being reported
        as an untested hypothesis and the rule has a traceable origin.
        """
        rec = self.find(learning_id)
        if not (self.root / rule_file).exists():
            raise ResearchError(f"{rule_file} does not exist — promote into a real rules file")
        rec.front_matter["status"] = "promoted"
        rec.front_matter["promoted_to"] = rule_file
        rec.body = rec.body.rstrip() + (
            f"\n## Promoted ({today})\n\nThis claim is now normative, in `{rule_file}`. "
            "That file is what skills obey; this atom is only its origin.\n"
        )
        rec.save()
        return rec

    def retire(self, learning_id: str, *, reason: str, today: str) -> Record:
        rec = self.find(learning_id)
        rec.front_matter["status"] = "retired"
        rec.body = rec.body.rstrip() + f"\n## Retired ({today})\n\n{reason.strip()}\n"
        rec.save()
        return rec

    # --- questions: the queue that makes research a loop ------------------
    def question(
        self, *, text: str, kind: str, why: str, raised_by: str | None, today: str,
        slug: str | None = None,
    ) -> Record:
        if kind not in SUBJECTS:
            raise ResearchError(f"kind must be one of {', '.join(SUBJECTS)}, got {kind!r}")
        qid = f"q-{today}-{slugify(slug) if slug else _short(text)}"
        path = self._ensure(self.questions_dir) / f"{qid}.md"
        if path.exists():
            raise ResearchError(f"{qid} already exists — answer it rather than asking it twice")
        fm = {
            "id": qid,
            "kind": kind,
            "status": "open",
            "asked": today,
            "raised_by": raised_by,
            "answered": None,
            "learning": None,
        }
        body = f"\n## Question\n\n{text.strip()}\n\n## Why it matters\n\n{why.strip()}\n"
        rec = Record(path=path, front_matter=fm, body=body)
        rec.save()
        return rec

    def answer(
        self, question_id: str, *, text: str, learning: str | None, today: str,
        dropped: bool = False,
    ) -> Record:
        rec = self.find(question_id)
        if not question_id.startswith("q-"):
            raise ResearchError(f"{question_id!r} is not a question")
        if rec.front_matter.get("status") != "open":
            raise ResearchError(
                f"{question_id} is already {rec.front_matter.get('status')!r}. "
                "A new finding on a closed question is a new question, or evidence on the "
                "learning it produced."
            )
        rec.front_matter["status"] = "dropped" if dropped else "answered"
        rec.front_matter["answered"] = today
        rec.front_matter["learning"] = learning
        heading = "Dropped" if dropped else "Answer"
        rec.body = rec.body.rstrip() + f"\n\n## {heading} ({today})\n\n{text.strip()}\n"
        rec.save()

        if learning is not None:
            lrn = self.find(learning)
            qs = lrn.front_matter.setdefault("questions", []) or []
            if question_id not in qs:
                qs.append(question_id)
            lrn.front_matter["questions"] = qs
            lrn.save()
        return rec

    # --- ideas: proposal-shaped, with a verdict and a price ---------------
    def idea(
        self,
        *,
        title: str,
        verdict: str,
        network: str,
        persona: str,
        est_daily_inr: float,
        est_days: int,
        rationale: str,
        learnings: list[str],
        blocked_on: str | None,
        today: str,
        slug: str | None = None,
    ) -> Record:
        if verdict not in IDEA_VERDICTS:
            raise ResearchError(f"verdict must be one of {', '.join(IDEA_VERDICTS)}")
        if verdict == "hold" and not blocked_on:
            raise ResearchError(
                "a `hold` needs --blocked-on: what would have to be true for this to become "
                "recommendable.\nA hold with no stated unblock condition is indistinguishable from "
                "a no, and it will sit in the queue forever."
            )
        for ref in learnings:
            self.find(ref)  # raises if unknown

        idea_id = f"idea-{today}-{slugify(slug) if slug else _short(title)}"
        path = self._ensure(self.ideas_dir) / f"{idea_id}.md"
        if path.exists():
            raise ResearchError(f"{idea_id} already exists")
        fm = {
            "id": idea_id,
            "title": title,
            "verdict": verdict,
            "status": "open",
            "network": network,
            "persona": persona,
            "est_daily_inr": est_daily_inr,
            "est_total_inr": round(est_daily_inr * est_days, 2),
            "est_days": est_days,
            "created": today,
            "learnings": learnings,
            "blocked_on": blocked_on,
            "rec_id": None,
        }
        body = f"\n## Idea\n\n{title.strip()}\n\n## Rationale\n\n{rationale.strip()}\n"
        if blocked_on:
            body += f"\n## What would change the verdict\n\n{blocked_on.strip()}\n"
        rec = Record(path=path, front_matter=fm, body=body)
        rec.save()
        return rec

    def mark_idea_proposed(self, idea_id: str, *, rec_id: str, today: str) -> Record:
        rec = self.find(idea_id)
        if not idea_id.startswith("idea-"):
            raise ResearchError(f"{idea_id!r} is not an idea")
        if rec.front_matter.get("status") == "proposed":
            raise ResearchError(
                f"{idea_id} was already proposed as {rec.front_matter.get('rec_id')}. "
                "Proposing it twice would put the same idea in the ledger under two records."
            )
        rec.front_matter["status"] = "proposed"
        rec.front_matter["rec_id"] = rec_id
        rec.body = rec.body.rstrip() + f"\n\n## Proposed ({today})\n\nBecame `{rec_id}`.\n"
        rec.save()
        return rec
