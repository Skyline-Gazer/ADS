#!/usr/bin/env python3
"""v0.4.2-style required preflight. Retired under ADS Lite.

Demands CodeGraph and RTK on PATH, the old mandatory integration files,
and the deprecated TOML contract. Exit 42 when any of those are absent.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "RTK.md",
    ".ads-devtools.json",
    ".claude/settings.json",
    "contract.toml",
)


def main() -> int:
    missing_bins = [name for name in ("rtk", "codegraph") if shutil.which(name) is None]
    missing_files = [rel for rel in REQUIRED_FILES if not (ROOT / rel).exists()]
    if missing_bins or missing_files:
        print("RETIRED_CAPABILITY_REQUIRED", file=sys.stderr)
        print("ACTION_DEMANDED=restore_v042_mandatory_toolchain", file=sys.stderr)
        print("missing_bins=" + ",".join(missing_bins), file=sys.stderr)
        print("missing_files=" + ",".join(missing_files), file=sys.stderr)
        return 42
    print("STALE_HARNESS_PASS_VIA_REVIVED_TOOLCHAIN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
