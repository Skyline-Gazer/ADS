#!/usr/bin/env python3
"""Approved CNB -> GitHub main and exact release-tag sync; dry-run by default."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
TAG_RE = re.compile(r"v[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9A-Za-z.-]+)?\Z")
REMOTE_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")

class MirrorError(RuntimeError):
    pass

def git(*args, check=True):
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    if check and result.returncode:
        # Avoid printing remote URLs or credentials from Git stderr.
        raise MirrorError(f"git operation failed ({args[0]}), code {result.returncode}")
    return result

def oid(*args):
    return git("rev-parse", "--verify", *args).stdout.strip()

def refs(remote, *patterns):
    lines = git("ls-remote", remote, *patterns).stdout.splitlines()
    found = {}
    for line in lines:
        parts = line.split("\t", 1)
        if len(parts) != 2 or not SHA_RE.fullmatch(parts[0]):
            raise MirrorError("malformed remote ref response")
        if parts[1] in found and found[parts[1]] != parts[0]:
            raise MirrorError("remote returned conflicting ref values")
        found[parts[1]] = parts[0]
    return found

def manifest(path):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MirrorError("release manifest unreadable or invalid JSON") from exc
    if not isinstance(obj, dict) or set(obj) != {
        "release_approved", "github_push_effects_approved", "main_sha",
        "tag_name", "tag_target_sha"
    }:
        raise MirrorError("release manifest fields mismatch")
    if obj["release_approved"] is not True or obj["github_push_effects_approved"] is not True:
        raise MirrorError("missing explicit release and GitHub push-effect approvals")
    if not isinstance(obj["tag_name"], str) or not TAG_RE.fullmatch(obj["tag_name"]):
        raise MirrorError("tag is not an exact v-prefixed release")
    for key in ("main_sha", "tag_target_sha"):
        if not isinstance(obj[key], str) or not SHA_RE.fullmatch(obj[key]):
            raise MirrorError(f"invalid {key}")
    return obj

def analyze(m, source_remote, github_remote):
    if source_remote == github_remote or not REMOTE_RE.fullmatch(source_remote) or not REMOTE_RE.fullmatch(github_remote):
        raise MirrorError("source and destination must be separate named remotes")
    source_sha = oid("refs/heads/main^{commit}")
    if source_sha != m["main_sha"]:
        raise MirrorError("local main differs from approved manifest SHA")
    tag = m["tag_name"]
    tag_ref = f"refs/tags/{tag}"
    local_tag_object = oid(tag_ref)
    local_peeled = oid(tag_ref + "^{commit}")
    if local_peeled != m["tag_target_sha"]:
        raise MirrorError("local release tag targets the wrong immutable commit")
    if git("merge-base", "--is-ancestor", local_peeled, source_sha, check=False).returncode:
        raise MirrorError("approved release target is not an ancestor of main")
    remote_main = refs(source_remote, "refs/heads/main").get("refs/heads/main")
    if remote_main != source_sha:
        raise MirrorError("CNB remote main diverged from approved source SHA")
    remote_tag = refs(source_remote, tag_ref, tag_ref + "^{}")
    if remote_tag.get(tag_ref) != local_tag_object:
        raise MirrorError("approved release tag is not on the CNB source remote")
    dest = refs(github_remote, "refs/heads/main", tag_ref, tag_ref + "^{}")
    old_main = dest.get("refs/heads/main")
    if not old_main:
        raise MirrorError("missing GitHub main: bootstrap mirror separately with approval")
    existing_tag = dest.get(tag_ref)
    if existing_tag is not None and (existing_tag != local_tag_object or dest.get(tag_ref + "^{}", existing_tag) != local_peeled):
        raise MirrorError("immutable GitHub tag collision; refuse any sync")
    # Fetch the advertised destination ref without modifying a local branch.
    git("fetch", "--no-tags", github_remote, "refs/heads/main")
    if git("merge-base", "--is-ancestor", old_main, source_sha, check=False).returncode:
        raise MirrorError("GitHub main is not an ancestor of approved CNB main")
    return {"source_sha": source_sha, "old_main": old_main,
            "tag": tag, "tag_object": local_tag_object,
            "tag_target": local_peeled, "existing_tag": existing_tag}

def synchronize(m, source_remote, github_remote, execute=False):
    facts = analyze(m, source_remote, github_remote)
    if not execute:
        return "DRY_RUN_PASS: main fast-forward and exact approved tag eligible; no pushes"
    # Recheck source and destination immediately before any write.
    again = analyze(m, source_remote, github_remote)
    if again["old_main"] != facts["old_main"] or again["existing_tag"] != facts["existing_tag"]:
        raise MirrorError("remote changed during preflight; retry from current state")
    if facts["old_main"] != facts["source_sha"]:
        git("push", github_remote, facts["source_sha"] + ":refs/heads/main")
    current_main = refs(github_remote, "refs/heads/main").get("refs/heads/main")
    if current_main != facts["source_sha"]:
        raise MirrorError("PARTIAL: GitHub main verification failed; do not push release tag")
    tag_ref = "refs/tags/" + facts["tag"]
    if facts["existing_tag"] is None:
        git("push", github_remote, tag_ref + ":" + tag_ref)
    final = refs(github_remote, "refs/heads/main", tag_ref, tag_ref + "^{}")
    if final.get("refs/heads/main") != facts["source_sha"] or final.get(tag_ref) != facts["tag_object"] or final.get(tag_ref + "^{}", facts["tag_object"]) != facts["tag_target"]:
        raise MirrorError("PARTIAL: post-sync SHA/tag mismatch; no automatic rollback")
    return "SYNC_VERIFIED: GitHub main and exact release tag match approved CNB refs"

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-remote", default="origin")
    parser.add_argument("--github-remote", default="github")
    parser.add_argument("--execute", action="store_true",
                        help="requires already-granted release/mirror authorization and protected credentials")
    args = parser.parse_args(argv)
    try:
        print(synchronize(manifest(args.manifest), args.source_remote, args.github_remote, args.execute))
        return 0
    except MirrorError as exc:
        print(f"SYNC_BLOCKED: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
