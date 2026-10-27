#!/usr/bin/env python3
"""Synthetic filesystem-read containment probe; does not enforce any sandbox.

Run ONLY inside a separately configured host/OS command sandbox. Never pass a
real personal file. Output is result categories, not file contents or paths.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ALLOWED = "ADS_ALLOWED_PROBE.txt"
DENIED = "ADS_DENIED_PROBE.txt"
LINK = "ADS_OUTSIDE_LINK"
MARKER = b"ADS_ALLOWED_PROBE_V1"


def _read(path: Path) -> bool:
    return bool(path.read_bytes())


def _list(path: Path) -> bool:
    # Do not print entries, even when the permission policy fails.
    return bool(os.listdir(path))


def _external(binary: str, arg: str) -> tuple[str, str]:
    try:
        p = subprocess.run([binary, arg], capture_output=True, timeout=10, check=False)
    except FileNotFoundError:
        return "NOT_TESTED", "binary_missing"
    except (OSError, subprocess.TimeoutExpired):
        return "NOT_TESTED", "spawn_error"
    if p.returncode == 0:
        return "UNSAFE", "read_succeeded"
    stderr = p.stderr.lower()
    if b"operation not permitted" in stderr or b"permission denied" in stderr:
        return "DENIED", "permission_denied"
    return "NOT_TESTED", "unclassified_failure"


def _attempt(op) -> tuple[str, str]:
    try:
        op()
        return "UNSAFE", "read_succeeded"
    except PermissionError:
        return "DENIED", "permission_denied"
    except FileNotFoundError:
        return "NOT_TESTED", "missing_fixture"
    except OSError:
        return "NOT_TESTED", "unclassified_failure"


def measure(inside: Path, outside: Path, link: Path | None) -> dict:
    if inside.name != ALLOWED or outside.name != DENIED:
        raise ValueError("Probe accepts only the two synthetic fixture basenames")
    if link is not None and link.name != LINK:
        raise ValueError("Symlink must be named ADS_OUTSIDE_LINK")
    # Avoid realpath checks here: the filesystem policy may forbid resolving
    # outside the workspace. Operator must verify synthetic layout separately.
    try:
        inside_ok = inside.read_bytes().strip() == MARKER
    except OSError:
        inside_ok = False

    vectors = {
        "python_read": _attempt(lambda: _read(outside)),
        "directory_listing": _attempt(lambda: _list(outside.parent)),
        "shell_cat": _external("/bin/cat", str(outside)),
        "shell_shasum": _external("/usr/bin/shasum", str(outside)),
    }
    if link is not None:
        vectors["symlink_read"] = _attempt(lambda: _read(link))
    if not inside_ok:
        verdict = "BLOCKED"
    elif any(item[0] == "UNSAFE" for item in vectors.values()):
        verdict = "UNSAFE"
    elif any(item[0] != "DENIED" for item in vectors.values()):
        verdict = "NOT_VERIFIED"
    else:
        verdict = "VERIFIED_BOUNDED_PROBE"
    return {
        "scope": "command-process-synthetic-only",
        "inside_read": "PASS" if inside_ok else "FAIL",
        "vectors": {name: status for name, (status, _) in vectors.items()},
        "verdict": verdict,
        "tui_or_mcp_coverage": "NOT_TESTED",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inside", type=Path, required=True)
    ap.add_argument("--outside", type=Path, required=True)
    ap.add_argument("--link", type=Path)
    args = ap.parse_args()
    try:
        result = measure(args.inside, args.outside, args.link)
    except ValueError as exc:
        ap.error(str(exc))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "VERIFIED_BOUNDED_PROBE" else 2


if __name__ == "__main__":
    sys.exit(main())
