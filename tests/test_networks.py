"""The network registry, and the safety property that makes it safe to have.

A network was a two-value enum in four argparse calls plus a `utm_source:
"snapchat"` literal. This makes it one file — but a registry that could *grant*
permission would be a downgrade on the guarantees SPEC decision #3 rests on, so
the most important tests here are the ones showing it can only ever refuse.
"""
from __future__ import annotations

import pytest
import yaml
from conftest import REPO, propose_argv, run

from ad_management_agent import cli, networks

RULES = REPO / "rules"


def write_registry(root, data):
    (root / "rules" / "networks.yaml").write_text(yaml.safe_dump({"networks": data}))


class TestTheRealRegistry:
    def test_both_networks_are_registered(self):
        assert set(networks.names(RULES)) == {"snap", "meta"}

    def test_both_networks_may_create_paused_only(self):
        # Meta flipped from `none` on 2026-08-27, in the same commit as meta-push.
        # `paused-only` is the ONLY permitted non-`none` value: if a third mode ever
        # appears here, it is a new capability and wants its own review.
        assert networks.get(RULES, "snap")["creation"] == "paused-only"
        assert networks.get(RULES, "meta")["creation"] == "paused-only"
        assert set(networks.CREATION_MODES) == {"none", "paused-only"}

    def test_meta_now_points_at_its_credentials(self):
        # SPEC.md decision #10, extended to Meta 2026-08-27. This asserts the
        # registry POINTS somewhere, not that a credential exists — the pointer is
        # documentation, and config.local.yaml is gitignored and may be empty.
        assert networks.get(RULES, "meta")["credentials"] == "config.local.yaml -> meta.*"

    def test_the_networks_disagree_about_the_ad_join_and_that_is_recorded(self):
        # The thing a hardcoded literal kept getting wrong.
        assert networks.get(RULES, "snap")["ad_join_param"] == "utm_id"
        assert networks.get(RULES, "meta")["ad_join_param"] == "utm_content"

    def test_snaps_utm_source_is_not_its_own_key(self):
        # `snap` vs `snapchat` is why only 7 of 151 signups joined to a costed ad
        # set. Both spellings are known here and nowhere else.
        assert networks.get(RULES, "snap")["utm_source"] == "snapchat"

    def test_an_unknown_network_names_the_registered_ones(self):
        with pytest.raises(networks.NetworkError, match="snap, meta"):
            networks.get(RULES, "truecaller")


class TestTheRegistryCanOnlyRefuse:
    """The whole reason a yaml file is allowed to hold this."""

    def test_require_creation_passes_for_snap(self):
        networks.require_creation(RULES, "snap", mode="paused-only")

    def test_require_creation_passes_for_meta(self):
        # Was test_require_creation_refuses_meta until 2026-08-27. Changed to assert
        # the new direction rather than deleted, per SPEC.md's note on this flip: a
        # deleted test is a check nobody notices going missing.
        networks.require_creation(RULES, "meta", mode="paused-only")

    def test_a_network_declared_none_is_still_refused(self, ledger_root):
        # The field has to keep working as a refusal now that neither real network
        # uses it, or the next network added inherits a guard nothing tests.
        write_registry(ledger_root, {
            "snap": {"label": "Snapchat", "utm_source": "snapchat", "ad_join_param": "utm_id",
                     "ad_set_join_param": "utm_term", "creation": "paused-only"},
            "truecaller": {"label": "Truecaller", "utm_source": "truecaller",
                           "ad_join_param": "utm_id", "ad_set_join_param": "utm_term",
                           "creation": "none"},
        })
        with pytest.raises(networks.NetworkError):
            networks.require_creation(ledger_root / "rules", "truecaller", mode="paused-only")

    def test_tightening_snap_to_none_blocks_the_push(self, ledger_root):
        # Editing the registry can take a capability away...
        write_registry(ledger_root, {
            "snap": {"label": "Snapchat", "utm_source": "snapchat", "ad_join_param": "utm_id",
                     "ad_set_join_param": "utm_term", "creation": "none", "credentials": False},
        })
        run(propose_argv(ledger_root))
        assert run(["snap-push", f"rec-{cli._today()}-w2330", "--dry-run"]) == 2

    def test_tightening_meta_to_none_blocks_its_push_too(self, ledger_root):
        # The mirror of the snap case, and the reason the field still matters now
        # that both real networks read paused-only: it can still take a capability
        # away, per-network, without touching code.
        write_registry(ledger_root, {
            "snap": {"label": "Snapchat", "utm_source": "snapchat", "ad_join_param": "utm_id",
                     "ad_set_join_param": "utm_term", "creation": "paused-only"},
            "meta": {"label": "Meta", "utm_source": "meta", "ad_join_param": "utm_content",
                     "ad_set_join_param": "utm_term", "creation": "none"},
        })
        run(propose_argv(ledger_root, network="meta"))
        assert run(["meta-push", f"rec-{cli._today()}-w2330", "--dry-run"]) == 2

    def test_loosening_meta_grants_snap_push_nothing(self, ledger_root):
        # ...and cannot give one. snap-push checks the record's OWN network before it
        # ever consults the registry, so declaring meta creatable here does not teach
        # that command a second API. Still true now that a Meta client exists — the
        # two pushes are separate commands, not one command reading a flag.
        write_registry(ledger_root, {
            "snap": {"label": "Snapchat", "utm_source": "snapchat", "ad_join_param": "utm_id",
                     "ad_set_join_param": "utm_term", "creation": "paused-only",
                     "credentials": False},
            "meta": {"label": "Meta", "utm_source": "meta", "ad_join_param": "utm_content",
                     "ad_set_join_param": "utm_term", "creation": "paused-only",
                     "credentials": False},
        })
        run(propose_argv(ledger_root, network="meta"))
        assert run(["snap-push", f"rec-{cli._today()}-w2330", "--dry-run"]) == 2


class TestMalformedRegistry:
    def test_a_missing_file_is_an_error_not_a_default(self, ledger_root):
        (ledger_root / "rules" / "networks.yaml").unlink()
        assert run(propose_argv(ledger_root)) == 2

    def test_an_unknown_creation_mode_is_refused(self, ledger_root):
        write_registry(ledger_root, {
            "snap": {"label": "S", "utm_source": "snapchat", "ad_join_param": "utm_id",
                     "ad_set_join_param": "utm_term", "creation": "yes-please"},
        })
        assert run(propose_argv(ledger_root)) == 2

    def test_a_network_missing_its_join_param_is_refused(self, ledger_root):
        write_registry(ledger_root, {
            "snap": {"label": "S", "utm_source": "snapchat", "ad_set_join_param": "utm_term",
                     "creation": "paused-only"},
        })
        assert run(propose_argv(ledger_root)) == 2

    def test_an_empty_registry_is_refused(self, ledger_root):
        (ledger_root / "rules" / "networks.yaml").write_text("networks: {}\n")
        assert run(propose_argv(ledger_root)) == 2


class TestCommandsValidateTheirNetwork:
    def test_propose_refuses_an_unregistered_network(self, ledger_root):
        assert run(propose_argv(ledger_root, network="truecaller")) == 2
        assert not (ledger_root / "campaigns" / "w2330").exists()

    def test_log_setup_refuses_one(self, ledger_root):
        run(propose_argv(ledger_root))
        assert run(["log-setup", f"rec-{cli._today()}-w2330", "--network", "truecaller",
                    "--campaign-id", "c", "--ad-set-id", "s", "--ad-id", "a"]) == 2

    def test_idea_refuses_one(self, ledger_root):
        assert run(["idea", "--slug", "x", "--title", "T", "--verdict", "recommend",
                    "--network", "truecaller", "--persona", "P", "--est-daily", "1000",
                    "--est-days", "5", "--rationale", "r"]) == 2
