#!/usr/bin/env python3
"""Fail closed if consumer CodeGraph/RTK integration leaks into production.

Copy into the consumer repository and run in PR merge-candidate CI targeting
the configured production branch. This generic guard is policy enforcement;
it is not the CodeGraph/RTK integration itself.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FORBIDDEN_NAMES = {
    ".ads-devtools.json",
    "codegraph.db",
    "codegraph.sqlite",
    "codegraph.sqlite3",
    "codegraph-index.sqlite",
    "codegraph-index.sqlite3",
    "rtk.exe",
}
FORBIDDEN_DIRS = {".ads-devtools", ".codegraph", ".rtk"}
HOST_CONFIGS = {
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".codex/config.toml",
    ".omp/oh-my-openagent.json",
    ".opencode/opencode.json",
    ".cursor/mcp.json",
    ".agents/settings.json",
}
TOOL_MARKER = re.compile(r"(?i)\b(?:codegraph|rtk(?:-oss)?)\b")
INTEGRATION_MARKER = re.compile(r"(?i)\b(?:command|hooks?|mcp|plugin|executable|binary|wrapper|sync|init)\b")
SKIP_DIRS = {".git", ".ads", "node_modules", ".venv", "venv"}


def files_under(root: Path):
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.is_file():
            yield relative, path


def violations(root: Path) -> list[str]:
    found: list[str] = []
    all_files = list(files_under(root))
    manifest_path = root / ".ads-devtools.json"
    manifest: dict = {}
    if manifest_path.is_file():
        found.append(".ads-devtools.json: consumer developer-tool manifest is forbidden on production")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            found.append(f".ads-devtools.json: cannot parse dev-only path declarations: {exc}")

    for rel, path in all_files:
        rel_posix = rel.as_posix()
        if rel.name in FORBIDDEN_NAMES and rel_posix != ".ads-devtools.json":
            found.append(f"{rel_posix}: forbidden generated artifact or tool binary")
        if any(part.lower() in FORBIDDEN_DIRS for part in rel.parts):
            found.append(f"{rel_posix}: forbidden tool configuration/artifact directory")
        if rel.name.lower() in {"rtk", "rtk.exe"}:
            found.append(f"{rel_posix}: RTK executable must not enter production")
        if rel_posix in HOST_CONFIGS:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if TOOL_MARKER.search(text) and INTEGRATION_MARKER.search(text):
                found.append(f"{rel_posix}: appears to contain CodeGraph/RTK host integration")

    for declared in manifest.get("dev_only_paths", []):
        if not isinstance(declared, str) or not declared:
            found.append(".ads-devtools.json: dev_only_paths must contain non-empty relative paths")
            continue
        candidate = (root / declared).resolve()
        if not candidate.is_relative_to(root.resolve()):
            found.append(f".ads-devtools.json: path escapes repository root: {declared}")
        elif candidate.exists():
            found.append(f"{declared}: declared dev-only path exists in production tree")

    return sorted(set(found))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--target-branch", required=True, help="production branch or PR base branch")
    args = parser.parse_args()
    root = args.root.resolve()

    if args.target_branch != "main":
        print(f"PASS/SKIP: {args.target_branch!r} is not the configured production branch 'main'; dev-only integration may remain here.")
        return 0

    problems = violations(root)
    if problems:
        print("FAIL: consumer CodeGraph/RTK configuration or artifacts would enter production main:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in problems), file=sys.stderr)
        return 1
    print("PASS: no known consumer CodeGraph/RTK integration or generated artifact in production main.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
