#!/usr/bin/env python3
"""Validate a declared lifecycle receipt, without impersonating live Provider verification."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
CHECKPOINTS = {"SESSION_START", "TASK_PREFLIGHT", "PRE_MERGE", "POST_MERGE", "PHASE_EXIT", "RELEASE", "PROVIDER_CUTOVER"}
READBACK = {"POST_MERGE", "PHASE_EXIT", "RELEASE", "PROVIDER_CUTOVER"}
HEAVY = {"container_build", "container_e2e", "browser", "performance", "sca", "full_ci", "platform_e2e", "deploy"}
KINDS = HEAVY | {"code_edit", "lint", "unit", "docs"}
EXECUTORS = {"local", "github-actions", "cnb-build", "remote-preview", "other-remote"}
DRIFT = {"STATUS_DRIFT", "SCOPE_DRIFT", "EVIDENCE_GAP", "PROVIDER_DRIFT", "RELEASE_DRIFT"}


def url(text: object) -> bool:
    return isinstance(text, str) and text.startswith("https://") and "/" in text[8:] and not any(c.isspace() for c in text)


def sha(text: object) -> bool:
    return isinstance(text, str) and SHA.fullmatch(text) is not None


def validate_receipt(data: object, expected_head: str | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["receipt must be JSON object"]
    errors: list[str] = []
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("invalid schema_version")
    checkpoint = data.get("checkpoint")
    if not isinstance(checkpoint, str) or checkpoint not in CHECKPOINTS:
        errors.append("invalid checkpoint")
    repository = data.get("repository")
    if not isinstance(repository, str) or not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        errors.append("invalid repository")
    if data.get("provider") not in ("github-primary", "cnb-primary-github-mirror"):
        errors.append("invalid provider")
    if not sha(data.get("source_sha")) or not sha(data.get("target_sha")):
        errors.append("invalid source/target SHA")
    if expected_head is not None and data.get("source_sha") != expected_head:
        errors.append("stale source_sha")
    if checkpoint in READBACK and (not sha(data.get("observed_target_sha")) or data["observed_target_sha"] != data.get("target_sha")):
        errors.append("missing or mismatched target readback")
    project = data.get("project_state")
    verdict = data.get("verdict")
    if project not in ("VERIFIED", "PROJECT_UNVERIFIED", "NOT_APPLICABLE"):
        errors.append("invalid project_state")
    if verdict not in ("GO", "HOLD", "PARTIAL"):
        errors.append("invalid verdict")
    if project == "VERIFIED" and not url(data.get("project_evidence_url")):
        errors.append("declared Project VERIFIED missing evidence")
    if checkpoint in {"PHASE_EXIT", "RELEASE", "PROVIDER_CUTOVER"} and verdict == "GO" and project == "PROJECT_UNVERIFIED":
        errors.append("PROJECT_UNVERIFIED cannot GO at dependent gate")
    if checkpoint in {"RELEASE", "PROVIDER_CUTOVER"} and verdict == "GO" and project == "NOT_APPLICABLE" and not data.get("project_na_reason"):
        errors.append("Project N/A needs explanation")

    workloads = data.get("workloads")
    if not isinstance(workloads, list):
        errors.append("missing workloads array")
        workloads = []
    for n, job in enumerate(workloads):
        if not isinstance(job, dict):
            errors.append(f"workloads[{n}] must be object")
            continue
        kind, executor, status = job.get("kind"), job.get("executor"), job.get("status")
        if not isinstance(kind, str) or kind not in KINDS or executor not in EXECUTORS or status not in ("PASS", "FAIL", "BLOCKED", "NOT_TESTED"):
            errors.append(f"workloads[{n}] invalid kind/executor/status")
            continue
        if status == "PASS":
            if job.get("tested_sha") != data.get("source_sha"):
                errors.append(f"workloads[{n}] PASS not bound to exact source SHA")
            if executor != "local" and not url(job.get("evidence_url")):
                errors.append(f"workloads[{n}] remote PASS missing URL")
        if kind in HEAVY and executor == "local":
            if not (job.get("local_exception_authorized") is True and
                    isinstance(job.get("fallback_reason"), str) and job["fallback_reason"].strip() and
                    url(job.get("remote_attempt_evidence_url"))):
                errors.append(f"workloads[{n}] heavy local requires scoped exception and remote failure evidence")
            if status == "PASS" and verdict == "GO" and checkpoint in {"RELEASE", "PROVIDER_CUTOVER"}:
                errors.append(f"workloads[{n}] local-heavy cannot prove release/cutover GO")
    drift = data.get("drift")
    if not isinstance(drift, list):
        errors.append("missing drift array")
        drift = []
    for n, item in enumerate(drift):
        if not isinstance(item, dict):
            errors.append(f"drift[{n}] must be object")
            continue
        if item.get("kind") not in DRIFT or item.get("status") not in ("OPEN", "RESOLVED", "DEFERRED", "BLOCKED") or not url(item.get("issue_url")):
            errors.append(f"drift[{n}] invalid classification/issue")
        if item.get("status") == "RESOLVED" and not (item.get("resolution") and url(item.get("evidence_url"))):
            errors.append(f"drift[{n}] resolution needs action and evidence")
        if item.get("status") != "RESOLVED" and verdict == "GO":
            errors.append(f"drift[{n}] unresolved drift cannot GO")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--expected-head")
    args = parser.parse_args()
    if args.expected_head is not None and not sha(args.expected_head):
        parser.error("--expected-head must be 40-character lowercase SHA")
    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("RECEIPT_INVALID: unreadable or invalid JSON")
        return 2
    errors = validate_receipt(data, args.expected_head)
    for err in errors:
        print("RECEIPT_INVALID: " + err)
    if errors:
        return 1
    print("RECEIPT_DECLARED_VALID: structural check only; confirm Provider and Project with live evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
