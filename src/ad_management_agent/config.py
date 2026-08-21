"""Config loading.

config.local.yaml (gitignored) overrides config.example.yaml's defaults.
Missing keys fall back to sane defaults, so the ledger commands work with
zero setup — only `fetch-analytics` needs real values.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULTS = {
    "ledger": {"root": str(REPO_ROOT)},
    "pdc": {"analytics_url": "", "api_key": "", "readonly_db_url": ""},
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config() -> dict:
    cfg = DEFAULTS
    local = REPO_ROOT / "config.local.yaml"
    if local.exists():
        override = yaml.safe_load(local.read_text(encoding="utf-8")) or {}
        cfg = _deep_merge(cfg, override)
    return cfg
