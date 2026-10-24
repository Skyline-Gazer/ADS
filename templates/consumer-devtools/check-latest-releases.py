#!/usr/bin/env python3
"""Query official latest-stable releases without installing tools or changing a repository."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import sys
import urllib.error
import urllib.request

UPSTREAMS = ("andysom25/codegraph", "rtk-ai/rtk")


def latest_stable(repo: str, timeout: float = 8.0) -> dict:
    if repo == "andysom25/codegraph":
        # Use the official npm dist-tag; this CodeGraph upstream has no GitHub Releases API entry.
        url = "https://registry.npmjs.org/@andysom25%2Fcodegraph/latest"
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "ADS-consumer-devtools-release-check"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            package = json.load(response)
        version = package.get("version")
        import re
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("npm dist-tag did not return a stable CodeGraph semver version")
        return {
            "repository": repo,
            "version": version,
            "release_url": "https://www.npmjs.com/package/@andysom25/codegraph",
            "published_at": package.get("time", {}).get(version),
        }

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "ADS-consumer-devtools-release-check"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.load(response)
    if release.get("draft") or release.get("prerelease") or not release.get("tag_name"):
        raise ValueError("upstream did not return a latest stable release")
    return {
        "repository": repo,
        "version": release["tag_name"].lstrip("v"),
        "release_url": release.get("html_url", url),
        "published_at": release.get("published_at"),
    }

def main() -> int:
    results = []
    failures = []
    for repo in UPSTREAMS:
        try:
            results.append(latest_stable(repo))
        except (OSError, ValueError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            failures.append({"repository": repo, "state": "UNVERIFIED", "reason": str(exc)})

    print(json.dumps({
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "policy": "latest-stable",
        "results": results,
        "failures": failures,
    }, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
