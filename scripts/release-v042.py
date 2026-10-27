#!/usr/bin/env python3
"""Validate or publish the owner-approved v0.4.2 manifest on exact main.

Read-only by default. The private sandbox receipt is an operator attestation:
the ADS workflow token cannot independently read that private repository.
No credential is installed, no ref is forced, and existing releases are never edited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPOSITORY = "Skyline-Gazer/ADS"
SANDBOX = "Skyline-Gazer/ADS-Acceptance-Sandbox"
VERSION = "v0.4.2"
MANIFEST = "release/v0.4.2-publish.json"
NOTES = "docs/releases/v0.4.2-notes.md"
WORKFLOWS = (
    ".github/workflows/validate.yml",
    ".github/workflows/v03-consumer-compat.yml",
    ".github/workflows/v04-consumer-acceptance.yml",
    ".github/workflows/v041-consumer-acceptance.yml",
)
SHA = re.compile(r"[0-9a-f]{40}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def full_sha(value):
    return isinstance(value, str) and bool(SHA.fullmatch(value))


def positive_integer(value):
    return type(value) is int and value > 0


def command(args, root, payload=None):
    result = subprocess.run(
        args, cwd=root, input=payload, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {result.stderr.strip()}")
    return result.stdout.strip()


class GitHub:
    def __init__(self, root):
        self.root = root

    def api(self, endpoint, *, payload=None, missing=False):
        args = ["gh", "api", endpoint]
        if payload is not None:
            args += ["--method", "POST", "--input", "-"]
        try:
            output = command(args, self.root, json.dumps(payload) if payload is not None else None)
        except RuntimeError as exc:
            if missing and "(HTTP 404)" in str(exc):
                return None
            raise
        return json.loads(output)


def validate_manifest(manifest, notes):
    require(isinstance(manifest, dict), "manifest must be an object")
    require(manifest.get("version") == VERSION, "manifest version must be v0.4.2")
    require(manifest.get("release_approved") is True, "explicit Owner release approval is required")
    target = manifest.get("release_target_sha")
    require(full_sha(target), "release target must be a full lowercase commit SHA")
    require(full_sha(manifest.get("previous_main_sha")), "previous_main_sha must bind preserved release history")
    require(positive_integer(manifest.get("source_pull_request")), "merged source PR number is required")
    require(manifest.get("notes_sha256") == hashlib.sha256(notes).hexdigest(), "release notes digest mismatch")
    text = notes.decode("utf-8")
    require(text.startswith("# ADS v0.4.2\n"), "release notes version/title mismatch")
    require("Known limitations" in text, "release notes must describe known limitations")
    require("NOT_VERIFIED" in text, "release notes must preserve unresolved Mac host containment gate")
    receipt = manifest.get("private_consumer_ci")
    require(isinstance(receipt, dict), "independent private consumer receipt is required")
    require(receipt.get("repository") == SANDBOX, "unexpected consumer repository")
    require(receipt.get("workflow") == "Private ADS Submodule Acceptance", "unexpected consumer workflow")
    require(receipt.get("result") == "success", "consumer acceptance must succeed")
    require(receipt.get("tested_ads_sha") == target, "consumer receipt does not test the exact target")
    require(full_sha(receipt.get("head_sha")), "consumer head SHA must be complete")
    require(positive_integer(receipt.get("pull_request_number")), "consumer PR number is required")
    run_id = receipt.get("run_id")
    require(positive_integer(run_id), "consumer run ID is required")
    require(receipt.get("run_url") == f"https://github.com/{SANDBOX}/actions/runs/{run_id}", "consumer receipt URL mismatch")
    require(receipt.get("verification") == "operator-verified-successful-run-and-job-logs", "consumer receipt requires independent operator verification")
    return target


def check_main(root, github, manifest, expected_main):
    require(full_sha(expected_main), "expected main SHA must be complete")
    remote = github.api(f"repos/{REPOSITORY}/git/ref/heads/main")
    require(remote.get("object", {}).get("sha") == expected_main, "remote main drifted from approved workflow context")
    require(command(["git", "rev-parse", "HEAD"], root) == expected_main, "checkout is not the exact approved main SHA")
    target = manifest["release_target_sha"]
    command(["git", "cat-file", "-e", target + "^{commit}"], root)
    command(["git", "merge-base", "--is-ancestor", target, expected_main], root)
    command(["git", "merge-base", "--is-ancestor", manifest["previous_main_sha"], target], root)
    changed = command(["git", "diff", "--name-only", target, expected_main], root).splitlines()
    require(changed == [MANIFEST], f"main differs from frozen target outside its approval manifest: {changed}")


def check_source_and_ci(github, manifest):
    target = manifest["release_target_sha"]
    pr = github.api(f"repos/{REPOSITORY}/pulls/{manifest['source_pull_request']}")
    require(pr.get("merged") is True and pr.get("state") == "closed", "source PR is not merged")
    require(pr.get("base", {}).get("ref") == "dev", "source PR must have integrated into dev")
    require(pr.get("base", {}).get("repo", {}).get("full_name") == REPOSITORY, "source PR belongs to another repository")
    source = pr.get("merge_commit_sha")
    require(full_sha(source), "source PR lacks merged SHA")
    compare = github.api(f"repos/{REPOSITORY}/compare/{source}...{target}")
    require(compare.get("status") in ("ahead", "identical") and compare.get("merge_base_commit", {}).get("sha") == source, "source fix is not an ancestor of the tested release target")
    require(full_sha(pr.get("head", {}).get("sha")), "source PR head SHA is invalid")
    receipts = {}
    for path in WORKFLOWS:
        endpoint = f"repos/{REPOSITORY}/actions/workflows/{Path(path).name}/runs?head_sha={target}&per_page=100"
        runs = github.api(endpoint).get("workflow_runs", [])
        exact = [run for run in runs if run.get("head_sha") == target and run.get("path", "").split("@", 1)[0] == path]
        require(exact, f"no exact-target CI run for {path}")
        latest = max(exact, key=lambda run: (run.get("id", 0), run.get("run_attempt", 0)))
        require(latest.get("repository", {}).get("full_name") == REPOSITORY, f"wrong CI repository: {path}")
        require(latest.get("head_branch") == "dev", f"CI must test the integrated dev target: {path}")
        require(latest.get("event") in {"push", "workflow_dispatch"}, f"untrusted CI event: {path}")
        require(latest.get("status") == "completed" and latest.get("conclusion") == "success", f"latest exact-target CI is not successful: {path}")
        receipts[path] = {"run_id": latest["id"], "run_attempt": latest["run_attempt"]}
    return receipts


def tag_state(github, target):
    ref = github.api(f"repos/{REPOSITORY}/git/ref/tags/{VERSION}", missing=True)
    if ref is None:
        return None
    obj = ref.get("object", {})
    require(obj.get("type") == "tag" and full_sha(obj.get("sha")), "existing release ref is not an annotated tag")
    tag = github.api(f"repos/{REPOSITORY}/git/tags/{obj['sha']}")
    require(tag.get("tag") == VERSION, "existing tag name mismatch")
    require(tag.get("object", {}).get("type") == "commit" and tag.get("object", {}).get("sha") == target, "existing tag points to a different target; never overwrite")
    return obj["sha"]


def release_state(github, target, notes, tag):
    release = github.api(f"repos/{REPOSITORY}/releases/tags/{VERSION}", missing=True)
    if release is None:
        return None
    require(tag is not None, "Release exists without its matching annotated tag")
    require(release.get("tag_name") == VERSION and release.get("target_commitish") == target, "existing Release target mismatch")
    require(release.get("name") == "ADS v0.4.2", "existing Release title mismatch")
    require(release.get("draft") is False and release.get("prerelease") is False, "existing Release state mismatch")
    normalize = lambda text: text.replace("\r\n", "\n").rstrip()
    require(normalize(release.get("body") or "") == normalize(notes), "existing Release notes mismatch; never edit automatically")
    return release


def execute(root, manifest, expected_main, github, publish=False):
    notes_bytes = (root / NOTES).read_bytes()
    target = validate_manifest(manifest, notes_bytes)
    notes = notes_bytes.decode("utf-8")
    check_main(root, github, manifest, expected_main)
    receipts = check_source_and_ci(github, manifest)
    tag = tag_state(github, target)
    release = release_state(github, target, notes, tag)
    if not publish:
        return {"mode": "VALIDATED_ONLY", "target": target, "ci": receipts, "tag": tag, "release_exists": release is not None,
                "private_receipt": "operator-attested; not queried with repository token"}
    # Recheck immediately before mutations; each retry validates all gates again.
    check_main(root, github, manifest, expected_main)
    receipts = check_source_and_ci(github, manifest)
    if tag is None:
        created = github.api(f"repos/{REPOSITORY}/git/tags", payload={
            "tag": VERSION, "message": "ADS v0.4.2 — consumer governance stabilization",
            "object": target, "type": "commit",
        })
        require(full_sha(created.get("sha")), "GitHub returned an invalid tag object SHA")
        check_main(root, github, manifest, expected_main)
        receipts = check_source_and_ci(github, manifest)
        github.api(f"repos/{REPOSITORY}/git/refs", payload={"ref": f"refs/tags/{VERSION}", "sha": created["sha"]})
    tag = tag_state(github, target)
    require(tag is not None, "published tag was not independently observed")
    check_main(root, github, manifest, expected_main)
    receipts = check_source_and_ci(github, manifest)
    if release is None:
        github.api(f"repos/{REPOSITORY}/releases", payload={
            "tag_name": VERSION, "target_commitish": target, "name": "ADS v0.4.2",
            "body": notes, "draft": False, "prerelease": False, "make_latest": "true",
        })
    require(release_state(github, target, notes, tag) is not None, "published Release was not independently observed")
    require(tag_state(github, target) == tag, "remote tag changed during publication")
    check_main(root, github, manifest, expected_main)
    receipts = check_source_and_ci(github, manifest)
    return {"mode": "PUBLISHED" if release is None else "ALREADY_PUBLISHED", "target": target, "tag": tag, "ci": receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-main-sha", required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    try:
        if args.publish:
            require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY and os.environ.get("GITHUB_REF") == "refs/heads/main" and os.environ.get("GITHUB_EVENT_NAME") == "push", "publication requires the authorized main-push workflow")
        manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
        print(json.dumps(execute(root, manifest, args.expected_main_sha, GitHub(root), args.publish), indent=2))
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"RELEASE BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
