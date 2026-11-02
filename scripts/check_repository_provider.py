#!/usr/bin/env python3
"""Read-only validation of ADS project Git provider policy (stdlib only)."""
import argparse
import json
from pathlib import Path
import re
import sys

class ProviderError(ValueError):
    pass

def object_with_keys(value, name, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ProviderError(f"{name}: expected fields {sorted(keys)}")
    return value

def validate(config):
    object_with_keys(config, "root", {"schema_version", "git", "review", "release"})
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ProviderError("unsupported schema version")
    git = object_with_keys(config["git"], "git", {"primary", "development_branch", "production_branch", "issue_provider", "github_mirror"})
    if git["primary"] not in ("github", "cnb") or git["issue_provider"] not in ("github", "cnb"):
        raise ProviderError("unknown provider")
    dev, prod = git["development_branch"], git["production_branch"]
    if dev != "dev" or not isinstance(prod, str) or prod == dev or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", prod) or "//" in prod or ".." in prod:
        raise ProviderError("dev required, production branch invalid")
    mirror = object_with_keys(git["github_mirror"], "github_mirror", {"enabled", "direction", "branches", "tags"})
    review = object_with_keys(config["review"], "review", {"auto", "npc", "max_fix_rounds"})
    release = object_with_keys(config["release"], "release", {"approval_required", "force_push"})
    if release != {"approval_required": True, "force_push": False}:
        raise ProviderError("release must require authorization and prohibit force push")
    if type(review["max_fix_rounds"]) is not int or not 1 <= review["max_fix_rounds"] <= 3:
        raise ProviderError("fix rounds must be 1 through 3")
    if git["primary"] == "cnb":
        if mirror != {"enabled": True, "direction": "cnb-to-github", "branches": [prod], "tags": "approved-releases-only"}:
            raise ProviderError("CNB requires one-way production-only mirror and approved tags")
        if review["auto"] not in ("cnb-code-review", "host-on-demand") or review["npc"] != "on-demand-read-only":
            raise ProviderError("CNB review must be automatic or on demand, with read-only NPC")
    else:
        if mirror != {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}:
            raise ProviderError("GitHub primary must not mirror")
        if review["auto"] != "host-on-demand" or review["npc"] != "disabled":
            raise ProviderError("GitHub primary uses existing reviewer")
    return config

def load(path):
    path = Path(path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProviderError("invalid JSON or unreadable file") from exc
    return validate(data)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".ads-project.json")
    args = parser.parse_args(argv)
    try:
        cfg = load(args.path)
    except ProviderError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    if cfg is None:
        print("UNCONFIGURED: inspect actual remotes/CI and ask once; no changes made")
        return 2
    print(f"CONFIGURED: {cfg['git']['primary']}; live remote state not VERIFIED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
