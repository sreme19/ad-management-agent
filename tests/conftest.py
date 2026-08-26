"""A throwaway ledger per test.

Every test here runs against a temp directory, never the real `campaigns/`. That is
not only hygiene: an earlier hand-run of these same flows wrote a stray record into
the live ledger because `cli` does `from .config import load_config`, so patching
`config.load_config` did nothing. The name to patch is `cli.load_config`, and the
`ledger` fixture is the only place that knows it.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from ad_management_agent import cli

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def ledger_root(tmp_path, monkeypatch) -> Path:
    (tmp_path / "rules").mkdir()
    shutil.copy(REPO / "rules" / "destinations.yaml", tmp_path / "rules" / "destinations.yaml")

    creative = tmp_path / "creatives" / "test-asset"
    creative.mkdir(parents=True)
    creative.joinpath("qa.md").write_text("Finished-asset gate — Verdict: `pass`\n")
    creative.joinpath("prompts.md").write_text("the prompt, with no outcome attached yet\n")
    creative.joinpath("asset-a.jpg").write_bytes(b"\xff\xd8\xff\xe0")

    tmp_path.joinpath("brief.md").write_text("# Brief\n\nA test brief.\n")

    monkeypatch.setattr(cli, "load_config",
                        lambda: {"ledger": {"root": str(tmp_path)}, "pdc": {}})
    return tmp_path


def run(argv: list[str]) -> int:
    """Invoke the CLI the way a shell would, returning its exit code."""
    try:
        cli.main(argv)
    except SystemExit as exc:
        return exc.code or 0
    return 0


def propose_argv(root: Path, slug: str = "w2330", **over) -> list[str]:
    flags = {
        "network": "snap",
        "campaign-name": "RA_TRAFFIC_GET_IN_PAN_TOF_202608",
        "ad-set-name": "WOMEN_23-30_CASUAL_LPV",
        "ad-name": "STORY_TEST_A_20260826",
        "targeting-summary": "prose reasoning for this audience",
        "creative-ref": "creatives/test-asset",
        "destination-url": "https://www.riteangle.dating/get/w",
        "budget-cap": "1000",
        "duration-days": "5",
        "brief": str(root / "brief.md"),
        "gender": "FEMALE",
        "min-age": "23",
        "max-age": "30",
        "countries": "in",
        "os": "ANDROID",
    }
    flags.update({k.replace("_", "-"): v for k, v in over.items()})
    argv = ["propose", slug]
    for key, value in flags.items():
        argv += [f"--{key}", value]
    return argv
