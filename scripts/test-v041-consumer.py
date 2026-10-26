#!/usr/bin/env python3
"""Isolated ADS pin upgrade/rollback and optional real developer-tool acceptance.

All consumer repositories and tool integration are disposable test fixtures.
CLI success is deliberately distinct from native Agent Host verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

STABLE = "2af17d9e1d816844c49835ae91b784405765ad46"
ROOT = Path(__file__).resolve().parents[1]


def run(argv, cwd, expected=(0,)):
    result = subprocess.run([str(part) for part in argv], cwd=cwd,
                            capture_output=True, text=True, timeout=180)
    if result.returncode not in expected:
        raise AssertionError(f"{argv[0]} failed ({result.returncode}):\n"
                             f"{result.stdout}\n{result.stderr}")
    return result


def git(root, *args):
    return run(["git", "-C", root, *args], root).stdout.strip()


def init_consumer(root):
    root.mkdir()
    git(root, "init", "-b", "dev")
    git(root, "config", "user.name", "ADS Acceptance")
    git(root, "config", "user.email", "acceptance@example.invalid")
    (root / "app.ts").write_text(
        "export function adsAcceptanceFixture() { return 1; }\n", encoding="utf-8")


def pin_roundtrip(source, candidate, scratch, baseline=STABLE):
    """Use a real local Git submodule; no cross-repository credential is needed."""
    for revision in (baseline, candidate):
        if not re.fullmatch(r"[a-f0-9]{40}", revision):
            raise ValueError("baseline and candidate must be immutable full commit SHAs")
        if git(source, "rev-parse", "--verify", revision + "^{commit}") != revision:
            raise ValueError("revision did not resolve to the exact approved commit")
    consumer = scratch / "pin-consumer"
    init_consumer(consumer)
    original = (consumer / "app.ts").read_bytes()
    git(consumer, "-c", "protocol.file.allow=always", "submodule", "add",
        "--name", "ads", str(source), ".ads")
    observed = []
    for name, revision in (("v0.4", baseline), ("candidate", candidate), ("rollback-v0.4", baseline)):
        git(consumer / ".ads", "checkout", "--detach", revision)
        git(consumer, "add", ".ads", ".gitmodules", "app.ts")
        git(consumer, "commit", "--allow-empty", "-m", f"test: {name} ADS pin")
        git(consumer, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "--recursive")
        assert git(consumer, "rev-parse", "HEAD:.ads") == revision
        assert git(consumer / ".ads", "rev-parse", "HEAD") == revision
        assert not git(consumer / ".ads", "branch", "--show-current")
        assert not git(consumer / ".ads", "status", "--porcelain")
        for relative in ("AGENTS.md", "STANDARD.md", "SAFETY.md", "QUALITY.md",
                         "skills/bootstrap/SKILL.md", "skills/adopt/SKILL.md", "skills/deliver/SKILL.md"):
            assert (consumer / ".ads" / relative).is_file(), relative
        run([sys.executable, consumer / ".ads/scripts/check-ads.py"], consumer / ".ads")
        assert (consumer / "app.ts").read_bytes() == original
        observed.append({"stage": name, "ads_sha": revision,
                         "consumer_sha": git(consumer, "rev-parse", "HEAD")})
    assert git(consumer, "rev-list", "--count", "HEAD") == "3"
    return {"state": "PASS", "kind": "real-local-Git-submodule",
            "stages": observed, "consumer_source_sha256": hashlib.sha256(original).hexdigest(),
            "private_remote_access": "NOT_TESTED"}


def development_digest(root):
    """Exclude generated data; repeat initialization must preserve integration files."""
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()
            and not any(part in {".git", ".codegraph", ".rtk"} for part in path.relative_to(root).parts)}


def tool_lifecycle(source, candidate, evidence, source_sha, scratch, preflight):
    consumer = scratch / "tool-consumer"
    init_consumer(consumer)
    git(consumer, "-c", "protocol.file.allow=always", "submodule", "add",
        "--name", "ads", str(source), ".ads")
    git(consumer / ".ads", "checkout", "--detach", candidate)
    (consumer / "AGENTS.md").write_text(
        f"# Consumer fixture\nADS pin: `{candidate}`. Read `.ads/AGENTS.md` before work.\n", encoding="utf-8")
    git(consumer, "add", "app.ts", "AGENTS.md", ".ads", ".gitmodules")
    git(consumer, "commit", "-m", "test: consumer with ADS guidance and no tool index")
    assert not (consumer / ".codegraph").exists()
    base = [sys.executable, preflight, "--root", consumer, "--evidence", evidence,
            "--codegraph-source-sha", source_sha, "--initialize", "--rtk-host", "codex"]

    def preflight_run(symbol, recover=False):
        command = [*base, "--query", symbol]
        if recover:
            command.append("--recover")
        result = run(command, consumer, expected=(3,))
        print(result.stdout, file=sys.stderr)
        return result.returncode

    # Exit 3 proves CLI success only. CI is not an actual native Agent Host.
    first = preflight_run("adsAcceptanceFixture")
    assert (consumer / ".codegraph").is_dir()
    status_before = json.loads(run(["codegraph", "status", "--json", consumer], consumer).stdout)
    files_before = development_digest(consumer)
    repeat = preflight_run("adsAcceptanceFixture")
    assert development_digest(consumer) == files_before, "repeat setup changed consumer integration"
    status_after = json.loads(run(["codegraph", "status", "--json", consumer], consumer).stdout)
    assert status_after["lastIndexed"] == status_before["lastIndexed"], "healthy index was rebuilt"

    with (consumer / "app.ts").open("a", encoding="utf-8") as stream:
        stream.write("export function adsAcceptanceRecovered() { return 2; }\n")
    recovered = preflight_run("adsAcceptanceRecovered", recover=True)
    query = json.loads(run(["codegraph", "query", "adsAcceptanceRecovered", "--path", consumer,
                            "--json", "--limit", "1"], consumer).stdout)
    assert query and query[0]["node"]["name"] == "adsAcceptanceRecovered", query
    assert not git(consumer, "ls-files", ".codegraph", ".rtk")

    guard = source / "templates/consumer-devtools/check-production-boundary.py"
    run([sys.executable, guard, "--root", consumer, "--target-branch", "dev"], consumer)
    run([sys.executable, guard, "--root", consumer, "--target-branch", "main"], consumer, expected=(1,))
    production = scratch / "release-preparation"
    artifacts = scratch / "build-output"
    production.mkdir()
    artifacts.mkdir()
    (production / "app.ts").write_bytes((consumer / "app.ts").read_bytes())
    (artifacts / "index.html").write_text("<!doctype html><title>ADS fixture</title>", encoding="utf-8")
    boundary = [sys.executable, guard, "--root", production, "--target-branch", "main",
                "--artifact-root", artifacts]
    run(boundary, production)
    (artifacts / ".codegraph").mkdir()
    (artifacts / ".codegraph/index.sqlite").write_text("negative fixture", encoding="utf-8")
    run(boundary, production, expected=(1,))
    return {"state": "PASS", "kind": "real-official-tools-isolated-consumer",
            "initialization_exit": first, "idempotence_exit": repeat, "recovery_exit": recovered,
            "production_clean": "PASS", "development_contamination_rejected": "PASS",
            "build_artifact_contamination_rejected": "PASS", "native_agent_host": "UNVERIFIED"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ads-root", type=Path, default=ROOT)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--baseline", default=STABLE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workspace", type=Path, help="Existing parent for disposable consumer fixtures")
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--codegraph-source-sha")
    parser.add_argument("--preflight-script", type=Path,
                        help="Defaults to the candidate consumer preflight template")
    args = parser.parse_args(argv)
    source = args.ads_root.resolve()
    if bool(args.evidence) != bool(args.codegraph_source_sha):
        parser.error("real tool lifecycle requires both --evidence and --codegraph-source-sha")
    with tempfile.TemporaryDirectory(prefix="ads-v041-consumer-", dir=args.workspace) as directory:
        scratch = Path(directory)
        report = {"candidate": args.candidate,
                  "submodule_compatibility": pin_roundtrip(source, args.candidate, scratch, args.baseline),
                  "tool_lifecycle": {"state": "NOT_RUN", "native_agent_host": "UNVERIFIED"}}
        if args.evidence:
            preflight = (args.preflight_script or
                         source / "templates/consumer-devtools/check-consumer-devtools.py").resolve()
            report["tool_lifecycle"] = tool_lifecycle(source, args.candidate, args.evidence.resolve(),
                                                      args.codegraph_source_sha, scratch, preflight)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
