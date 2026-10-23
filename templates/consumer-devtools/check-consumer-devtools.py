#!/usr/bin/env python3
"""Read-only latest-stable preflight for a consumer project's development checkout.

Copy this file to the consumer repository's scripts/ directory. It never installs
or upgrades software and never modifies host configuration.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

UPSTREAMS = {
    "codegraph": ("codegraph", "andysom25/codegraph"),
    "rtk": ("rtk", "rtk-ai/rtk"),
}
VERSION_RE = re.compile(r"(?<![0-9A-Za-z])v?(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)")


def latest_stable(repo: str, timeout: float = 8.0) -> tuple[str, str]:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "ADS-consumer-devtools-check"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.load(response)
    if release.get("draft") or release.get("prerelease") or not release.get("tag_name"):
        raise ValueError("upstream did not return a latest stable release")
    return release["tag_name"].lstrip("v"), release.get("html_url", url)


def installed_version(command: str) -> tuple[str, str]:
    executable = shutil.which(command)
    if not executable:
        raise FileNotFoundError(f"{command} is not installed")
    if command == "rtk" and Path(executable).resolve().name.lower() in {"rtk-oss", "rtk-oss.exe"}:
        raise ValueError("the resolved executable is rtk-oss; full RTK is required")
    result = subprocess.run(
        [executable, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=8,
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode != 0:
        raise RuntimeError(f"{command} --version exited {result.returncode}")
    match = VERSION_RE.search(output)
    if not match:
        raise ValueError(f"could not parse version from {command} --version output")
    return match.group(1), executable


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-branch", default="main")
    parser.add_argument("--allow-production-checkout", action="store_true")
    args = parser.parse_args()

    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if branch == args.production_branch and not args.allow_production_checkout:
        print(f"BLOCKED: run consumer tool initialization from a development branch, not {branch}.", file=sys.stderr)
        return 2

    failed = False
    for name, (command, repo) in UPSTREAMS.items():
        try:
            installed, executable = installed_version(command)
        except FileNotFoundError as exc:
            print(f"{name}: MISSING — {exc}. Ask the user before installing.")
            failed = True
            continue
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"{name}: UNVERIFIED — {exc}")
            failed = True
            continue

        try:
            latest, release_url = latest_stable(repo)
        except (OSError, ValueError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"{name}: UPSTREAM_UNVERIFIED — installed={installed}, executable={executable}, reason={exc}")
            failed = True
            continue

        freshness = "LATEST" if installed == latest else "OUTDATED"
        print(
            f"{name}: {freshness} — installed={installed}, latest={latest}, "
            f"executable={executable}, release={release_url}"
        )
        if freshness != "LATEST":
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
