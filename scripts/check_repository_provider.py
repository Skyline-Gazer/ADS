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
    if isinstance(config, dict) and type(config.get("schema_version")) is int and config["schema_version"] == 2:
        return validate_v2(config)
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
        if review["auto"] != "cnb-code-review" or review["npc"] != "on-demand-read-only":
            raise ProviderError("CNB must enable automatic review and read-only NPC")
    else:
        if mirror != {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}:
            raise ProviderError("GitHub primary must not mirror")
        if review["auto"] != "host-on-demand" or review["npc"] != "disabled":
            raise ProviderError("GitHub primary uses existing reviewer")
    return config

def validate_v2(config):
    """Separate Mode B authority; schema v1's one-way mirror stays unchanged."""
    object_with_keys(config, "root", {"schema_version", "git", "review", "release"})
    git = object_with_keys(config["git"], "git", {
        "mode", "development_provider", "release_provider", "issue_provider",
        "development_branch", "production_branch", "cnb_repository", "github_repository",
        "transfer_prefix"})
    if git["mode"] != "cnb-development-github-release-gate" or git["development_provider"] != "cnb" or git["release_provider"] != "github":
        raise ProviderError("Mode B requires CNB development and GitHub release authority")
    if git["development_branch"] != "dev" or git["production_branch"] != "main" or git["issue_provider"] not in ("github", "cnb"):
        raise ProviderError("Mode B requires dev/main and an explicit issue authority")
    if git["transfer_prefix"] != "release/cnb-":
        raise ProviderError("Mode B requires exact release/cnb-<SHA> transfers")
    for key in ("cnb_repository", "github_repository"):
        value = git[key]
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+", value) or ".." in value:
            raise ProviderError("canonical repository identity required")
    review = object_with_keys(config["review"], "review", {"auto", "npc", "max_fix_rounds", "release_app_id", "release_check", "ci_app_id", "ci_check"})
    if review["auto"] != "cnb-code-review" or review["npc"] != "on-demand-read-only" or type(review["max_fix_rounds"]) is not int or not 1 <= review["max_fix_rounds"] <= 3:
        raise ProviderError("automatic CNB review, read-only NPC and at most three repairs required")
    if type(review["release_app_id"]) is not int or review["release_app_id"] <= 0 or not isinstance(review["release_check"], str) or not review["release_check"].strip():
        raise ProviderError("independently observed trusted release App/check required")
    if type(review["ci_app_id"]) is not int or review["ci_app_id"] <= 0 or not isinstance(review["ci_check"], str) or not review["ci_check"].strip():
        raise ProviderError("trusted deterministic CI App/check required")
    if (review["release_app_id"], review["release_check"]) == (review["ci_app_id"], review["ci_check"]):
        raise ProviderError("release review and deterministic CI must be distinct checks")
    release = object_with_keys(config["release"], "release", {"approval_required", "force_push", "copy_direction", "enabled", "development_paths"})
    if not isinstance(release["development_paths"], list) or not release["development_paths"] or any(not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts for path in release["development_paths"]):
        raise ProviderError("explicit relative development paths required")
    if release["approval_required"] is not True or release["force_push"] is not False or release["copy_direction"] != "github-to-cnb" or type(release["enabled"]) is not bool:
        raise ProviderError("Mode B requires approved forward-only GitHub publication copy")
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
    print(f"CONFIGURED: {cfg['git'].get('primary', cfg['git'].get('mode'))}; live remote state not VERIFIED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
