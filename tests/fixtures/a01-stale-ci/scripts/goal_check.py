#!/usr/bin/env python3
"""Current goal: YAML-only site contract, no mandatory CodeGraph/RTK revival."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIVED = (
    "RTK.md",
    ".ads-devtools.json",
    ".claude/settings.json",
    "codegraph.json",
    "contract.toml",
    ".codegraph",
)


def main() -> int:
    contract = ROOT / "contract.yaml"
    if not contract.is_file():
        print("GOAL_FAIL missing contract.yaml", file=sys.stderr)
        return 1
    values = {}
    for line in contract.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            print("GOAL_FAIL unreadable contract.yaml", file=sys.stderr)
            return 1
        values[key.strip()] = value.strip()
    if values.get("site_contract") != "yaml-only":
        print("GOAL_FAIL site_contract", file=sys.stderr)
        return 1
    revived = [rel for rel in REVIVED if (ROOT / rel).exists()]
    if revived:
        print("GOAL_FAIL revived=" + ",".join(revived), file=sys.stderr)
        return 1
    print("GOAL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
