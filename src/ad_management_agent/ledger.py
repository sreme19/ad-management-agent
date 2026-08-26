"""Deterministic, zero-API ledger for ad campaign recommendations.

Nothing in this file calls the Anthropic API or any LLM. Every function here
is a pure file read/write. The actual reasoning (targeting, creative, copy)
happens live in whichever Claude Code session is running the skill that
calls into this module via the CLI — this module only persists the result.

Lifecycle: proposed -> executing -> live -> reviewed, with an `abandoned`
side-exit from `proposed`. See SPEC.md "Ledger" for the full rationale.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

STATUSES = ("proposed", "executing", "live", "reviewed", "abandoned")
VERDICTS = ("working", "not-working", "inconclusive")

_FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "campaign"


def new_rec_id(slug: str, today: str) -> str:
    return f"rec-{today}-{slug}"


@dataclass
class Record:
    path: Path
    front_matter: dict
    body: str

    @property
    def rec_id(self) -> str:
        return self.front_matter["rec_id"]

    @property
    def status(self) -> str:
        return self.front_matter["status"]

    def save(self) -> None:
        fm = yaml.safe_dump(self.front_matter, sort_keys=False).strip()
        self.path.write_text(f"---\n{fm}\n---\n{self.body}", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Record":
        text = path.read_text(encoding="utf-8")
        m = _FRONT_MATTER_RE.match(text)
        if not m:
            raise ValueError(f"{path}: missing YAML front matter")
        fm = yaml.safe_load(m.group(1)) or {}
        return cls(path=path, front_matter=fm, body=m.group(2))


class Ledger:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.campaigns_dir = self.root / "campaigns"
        self.campaigns_dir.mkdir(parents=True, exist_ok=True)

    def _record_path(self, slug: str) -> Path:
        return self.campaigns_dir / slug / "record.md"

    def find(self, rec_id: str) -> Record:
        for p in sorted(self.campaigns_dir.glob("*/record.md")):
            rec = Record.load(p)
            if rec.rec_id == rec_id:
                return rec
        raise KeyError(f"no record with rec_id {rec_id!r}")

    def all(self) -> list[Record]:
        return [Record.load(p) for p in sorted(self.campaigns_dir.glob("*/record.md"))]

    def propose(
        self,
        *,
        slug: str,
        network: str,
        campaign_name: str,
        ad_set_name: str,
        ad_name: str,
        targeting_summary: str,
        targeting: dict | None,
        creative_ref: str,
        destination_url: str,
        budget_cap_inr_per_day: float,
        duration_days: int,
        brief_path: str,
        today: str,
    ) -> Record:
        base_slug = slugify(slug)
        slug = base_slug
        path = self._record_path(slug)
        i = 2
        while path.exists():
            slug = f"{base_slug}-{i}"
            path = self._record_path(slug)
            i += 1
        path.parent.mkdir(parents=True, exist_ok=True)

        rec_id = new_rec_id(slug, today)
        fm = {
            "rec_id": rec_id,
            "network": network,
            "status": "proposed",
            "campaign_name": campaign_name,
            "ad_set_name": ad_set_name,
            "ad_name": ad_name,
            "campaign_id": None,
            "ad_set_id": None,
            "ad_id": None,
            "targeting_summary": targeting_summary,
            # Prose above for the human, normalized block below for the pusher.
            # See targeting.py for why both exist rather than only the prose.
            "targeting": targeting or None,
            "creative_ref": creative_ref,
            "destination_url": destination_url,
            "budget_cap_inr_per_day": budget_cap_inr_per_day,
            "duration_days": duration_days,
            "created": today,
        }
        brief = Path(brief_path).read_text(encoding="utf-8") if brief_path else ""
        body = f"\n## Brief (proposed)\n\n{brief.strip()}\n"
        rec = Record(path=path, front_matter=fm, body=body)
        rec.save()
        return rec

    AMENDABLE = (
        "campaign_name",
        "ad_set_name",
        "ad_name",
        "targeting_summary",
        "targeting",
        "creative_ref",
        "destination_url",
        "budget_cap_inr_per_day",
        "duration_days",
    )

    def amend(
        self,
        rec_id: str,
        *,
        changes: dict,
        reason: str,
        today: str,
    ) -> tuple[Record, dict]:
        """Revise a still-proposed recommendation, keeping an audit trail of what moved.

        Only `proposed` records may be amended. Once a record is `live` the fields
        describe what was actually built, and rewriting them would silently falsify
        the thing `ad-audit` joins a real outcome back to — a change after launch is a
        `log-setup --deviated` note, not an amendment. `reviewed`/`abandoned` are history.

        Returns the record and a {field: (old, new)} diff of what actually changed.
        """
        rec = self.find(rec_id)
        status = rec.front_matter.get("status")
        if status != "proposed":
            raise ValueError(
                f"{rec_id} is {status!r}, not 'proposed' — only a proposal can be amended.\n"
                "A change to something already live belongs in `log-setup --deviated`, which "
                "records what differed rather than rewriting what was proposed."
            )

        bad = [k for k in changes if k not in self.AMENDABLE]
        if bad:
            raise ValueError(
                f"not amendable: {', '.join(sorted(bad))}. "
                f"Amendable fields are: {', '.join(self.AMENDABLE)}."
            )

        # A dict-valued field (targeting) is applied whole but reported per sub-key,
        # so the Amendment section says "min_age 18 -> 23" rather than dumping two
        # mappings and leaving the reader to spot the difference.
        diff = {}
        applied = {}
        for field, new in changes.items():
            old = rec.front_matter.get(field)
            if old == new:
                continue
            applied[field] = new
            if isinstance(new, dict) and isinstance(old, dict):
                for k in sorted(set(old) | set(new)):
                    if old.get(k) != new.get(k):
                        diff[f"{field}.{k}"] = (old.get(k), new.get(k))
            else:
                diff[field] = (old, new)

        if not diff:
            return rec, diff

        rec.front_matter.update(applied)
        rec.front_matter["amended"] = today

        rows = "\n".join(f"- `{f}`: {old!r} → {new!r}" for f, (old, new) in sorted(diff.items()))
        rec.body += f"\n## Amendment ({today})\n\n- Reason: {reason}\n{rows}\n"
        rec.save()
        return rec, diff

    def log_setup(
        self,
        rec_id: str,
        *,
        network: str,
        campaign_id: str,
        ad_set_id: str,
        ad_id: str,
        deviated: str | None,
        today: str,
    ) -> Record:
        rec = self.find(rec_id)
        if rec.front_matter.get("network") != network:
            raise ValueError(
                f"{rec_id} was proposed for network={rec.front_matter.get('network')!r}, "
                f"not {network!r}"
            )
        rec.front_matter.update(
            {
                "status": "live",
                "campaign_id": campaign_id,
                "ad_set_id": ad_set_id,
                "ad_id": ad_id,
                "executed": today,
            }
        )
        section = (
            f"\n## Execution\n\n- Date: {today}\n- Campaign ID: {campaign_id}\n"
            f"- Ad set ID: {ad_set_id}\n- Ad ID: {ad_id}\n"
        )
        if deviated:
            section += f"- Deviated from brief: {deviated}\n"
        rec.body += section
        rec.save()
        return rec

    def record_campaign_caps(
        self,
        rec_id: str,
        *,
        daily_inr: float | None,
        lifetime_inr: float | None,
        today: str,
    ) -> Record:
        """Record what the parent campaign's caps actually were at push time.

        Not part of the lifecycle and not amendable — it is an observation of the
        platform, written by `snap-push` because that is the only moment the value
        is known for certain. `budget_cap_inr_per_day` is what was *proposed*; the
        effective daily spend is the lower of that and this. Without both figures
        on the record, `ad-agent open` cannot tell a properly funded ad set from
        one silently capped below rules/budget.md's floor, which is exactly what
        happened on 2026-08-26.

        A verified absence is information too: `campaign_daily_cap_inr: null` with
        a `campaign_caps_verified` date means "checked, no cap", which is different
        from a record that was never checked at all.
        """
        rec = self.find(rec_id)
        rec.front_matter["campaign_daily_cap_inr"] = daily_inr
        rec.front_matter["campaign_lifetime_cap_inr"] = lifetime_inr
        rec.front_matter["campaign_caps_verified"] = today
        rec.save()
        return rec

    NOTE_KINDS = ("budget", "targeting", "creative", "incident", "observation")

    def note(self, rec_id: str, *, text: str, kind: str, today: str) -> Record:
        """Append a dated, append-only note to a record, whatever its status.

        The lifecycle has no other home for something that happens *during* a run.
        `amend` deliberately refuses a live record, because its fields have to keep
        describing what was actually built; `log_setup` fires once; `log_review` is
        the end. So a mid-flight change — a budget raised on day three, an ad set
        paused for a day, a tracking wobble — would otherwise leave no trace, and the
        verdict would end up judged against conditions that quietly moved.

        Notes never rewrite anything. They only accumulate.
        """
        if kind not in self.NOTE_KINDS:
            raise ValueError(f"kind must be one of {self.NOTE_KINDS}, got {kind!r}")
        rec = self.find(rec_id)
        rec.front_matter["last_note"] = today
        rec.body += f"\n## Note — {kind} ({today})\n\n{text.strip()}\n"
        rec.save()
        return rec

    def log_review(
        self,
        rec_id: str,
        *,
        verdict: str,
        summary: str,
        review_log_path: str | None,
        today: str,
    ) -> Record:
        if verdict not in VERDICTS:
            raise ValueError(f"verdict must be one of {VERDICTS}, got {verdict!r}")
        rec = self.find(rec_id)
        rec.front_matter.update({"status": "reviewed", "verdict": verdict, "reviewed": today})
        detail = Path(review_log_path).read_text(encoding="utf-8") if review_log_path else ""
        rec.body += (
            f"\n## Review\n\n- Date: {today}\n- Verdict: {verdict}\n- Summary: {summary}\n\n"
            f"{detail.strip()}\n"
        )
        rec.save()
        return rec

    def abandon(self, rec_id: str, *, reason: str, today: str) -> Record:
        rec = self.find(rec_id)
        rec.front_matter.update({"status": "abandoned", "abandoned": today})
        rec.body += f"\n## Abandoned\n\n- Date: {today}\n- Reason: {reason}\n"
        rec.save()
        return rec

    def write_index(self) -> Path:
        records = self.all()
        lines = [
            "<!-- Generated by `ad-agent`. Do not hand-edit — regenerated on every ledger command. -->",
            "",
            "# Campaign ledger index",
            "",
            "| rec_id | network | status | campaign | ad set id | verdict | created |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in records:
            fm = r.front_matter
            lines.append(
                f"| {fm.get('rec_id', '')} | {fm.get('network', '')} | {fm.get('status', '')} | "
                f"{fm.get('campaign_name') or ''} | {fm.get('ad_set_id') or ''} | "
                f"{fm.get('verdict') or ''} | {fm.get('created', '')} |"
            )
        out = self.root / "INDEX.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out
