"""The UTM scheme, and the guard that keeps the documented command list honest."""
from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from conftest import run

from ad_management_agent import cli


class TestUtmUrl:
    """rules/tracking.md, written literally rather than as a {{macro}}.

    The 2026-08-21 incident was a macro that silently never resolved, costing a
    week of Snap spend in unattributable installs.
    """

    def url(self):
        return cli._utm_url("https://www.riteangle.dating/get/w",
                            "RA_TRAFFIC_GET_IN_PAN_TOF_202608",
                            "squad-uuid", "ad-uuid", "STORY_FOURTEEN-SUITORS_A_20260824")

    def test_all_five_parameters_are_present(self):
        q = parse_qs(urlsplit(self.url()).query)
        assert set(q) == {"utm_source", "utm_medium", "utm_campaign", "utm_term",
                          "utm_id", "utm_content"}

    def test_utm_id_carries_the_ad_id(self):
        # traffic-quality.ts's adSetKeyOf reads utm_id as the Snap ad id. This is
        # the parameter the join actually uses.
        assert parse_qs(urlsplit(self.url()).query)["utm_id"] == ["ad-uuid"]

    def test_utm_term_carries_the_ad_squad_id(self):
        assert parse_qs(urlsplit(self.url()).query)["utm_term"] == ["squad-uuid"]

    def test_no_unresolved_macro_survives(self):
        assert "{{" not in self.url()

    def test_the_source_matches_the_documented_scheme(self):
        # tracking.md specifies {snapchat|meta} for utm_source, while the ledger's
        # own network label is `snap`. Both spellings are correct in their own
        # place; the normalisation between them belongs to pocket-dating-coach.
        assert parse_qs(urlsplit(self.url()).query)["utm_source"] == ["snapchat"]

    def test_the_path_is_preserved(self):
        assert urlsplit(self.url()).path == "/get/w"


class TestCommandsStayDocumented:
    def test_every_command_has_a_hand_written_section(self):
        # Runs against the real README and cheatsheet on purpose: this is the
        # regression test for both of them claiming, on the day snap-push shipped,
        # that this agent never calls a Snap API.
        assert run(["commands", "--check"]) == 0

    def test_the_generated_block_lists_every_subcommand(self):
        parser = cli.build_parser()
        block = cli._commands_markdown(parser)
        for name, _, _ in cli._subcommands(parser):
            assert f"`{name}`" in block

    def test_check_fails_when_a_command_has_no_section(self, ledger_root, monkeypatch):
        import shutil
        from pathlib import Path
        repo = Path(__file__).resolve().parents[1]
        (ledger_root / "wiki-export").mkdir(exist_ok=True)
        shutil.copy(repo / "README.md", ledger_root / "README.md")
        text = (repo / "wiki-export" / "Command-Cheatsheet.md").read_text()
        (ledger_root / "wiki-export" / "Command-Cheatsheet.md").write_text(
            text.replace("ad-agent abandon", "(removed)"))
        assert run(["commands", "--check"]) == 1
