#!/usr/bin/env python3
"""Read-only latest-stable check for a consumer project's development checkout.

Copy this file to the consumer repository's scripts/ directory. It never installs
or upgrades software and never modifies host configuration. RTK host integration
still requires a separate smoke test through the active agent.
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
    if repo == "andysom25/codegraph":
        # Use the official npm dist-tag: this CodeGraph upstream has no GitHub Releases API entry.
        url = "https://registry.npmjs.org/@andysom25%2Fcodegraph/latest"
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "ADS-consumer-devtools-check"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            package = json.load(response)
        version = package.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("npm dist-tag did not return a stable CodeGraph semver version")
        return version, "https://www.npmjs.com/package/@andysom25/codegraph"

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


def verify_full_rtk_edition() -> tuple[str, str]:
    """Use package metadata where possible; both RTK editions share the same binary name."""
    brew = shutil.which("brew")
    if brew:
        full = subprocess.run(
            [brew, "list", "--versions", "rtk"], capture_output=True, text=True, check=False, timeout=8
        )
        oss = subprocess.run(
            [brew, "list", "--versions", "rtk-oss"], capture_output=True, text=True, check=False, timeout=8
        )
        if full.returncode == 0 and oss.returncode != 0:
            return "VERIFIED", "Homebrew package metadata identifies formula rtk (not rtk-oss)"
        if oss.returncode == 0:
            return "FAIL", "Homebrew package metadata identifies rtk-oss; full RTK is required"
        if full.returncode == 0 and oss.returncode == 0:
            return "FAIL", "both RTK editions appear installed; the upstream packages conflict"
    return (
        "UNVERIFIED",
        "the full and OSS editions share the binary name; verify package/install provenance or obtain permission to install the full edition",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-branch", default="main")
    parser.add_argument("--allow-production-checkout", action="store_true")
    args = parser.parse_args(argv)

    branch_result = subprocess.run(
        ["git", "branch", "--show-current"],
        check=False,
        capture_output=True,
        text=True,
    )
    branch = branch_result.stdout.strip()
    if branch_result.returncode != 0 or not branch:
        print("BLOCKED: cannot prove this is a development-branch checkout.", file=sys.stderr)
        return 2
    if branch == args.production_branch and not args.allow_production_checkout:
        print(f"BLOCKED: run consumer tool initialization from a development branch, not {branch}.", file=sys.stderr)
        return 2

    failed = False
    for name, (command, repo) in UPSTREAMS.items():
        try:
            latest, release_url = latest_stable(repo)
        except (OSError, ValueError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"{name}: UPSTREAM_UNVERIFIED — official latest stable release unavailable: {exc}")
            failed = True
            continue

        try:
            installed, executable = installed_version(command)
        except FileNotFoundError:
            print(
                f"{name}: MISSING — latest stable={latest}, release={release_url}. "
                "Ask the user before installing."
            )
            failed = True
            continue
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"{name}: UNVERIFIED — latest stable={latest}, release={release_url}, reason={exc}")
            failed = True
            continue

        freshness = "LATEST" if installed == latest else "OUTDATED"
        print(
            f"{name}: {freshness} — installed={installed}, latest={latest}, "
            f"executable={executable}, release={release_url}"
        )
        if freshness != "LATEST":
            failed = True
            continue

        if name == "codegraph":
            try:
                status = subprocess.run(
                    [executable, "status"],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                print(f"codegraph project index: UNVERIFIED — {exc}")
                failed = True
            else:
                if status.returncode != 0:
                    print(f"codegraph project index: NEEDS_INIT_OR_SYNC — status exit={status.returncode}")
                    failed = True
                else:
                    print("codegraph project index: STATUS_COMMAND_PASS — inspect status output before relying on the graph")

        if name == "rtk":
            edition, reason = verify_full_rtk_edition()
            print(f"rtk edition: {edition} — {reason}")
            if edition != "VERIFIED":
                failed = True
            print("rtk host integration: REQUIRED_SEPARATE_SMOKE_TEST — this script verifies the binary version only")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
