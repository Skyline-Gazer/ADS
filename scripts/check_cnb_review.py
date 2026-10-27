#!/usr/bin/env python3
"""Fail-closed, current-SHA CNB structured code-review gate."""
import argparse
import json
from pathlib import Path
import re
import sys

SHA = re.compile(r"[a-f0-9]{40}\Z")
STATUS = {"passed", "needs_modification", "critical"}
SEVERITY = {"critical", "warning", "info"}

class ReviewGateError(ValueError):
    pass

def gate(data, review_head, current_head):
    if not isinstance(review_head, str) or not SHA.fullmatch(review_head):
        raise ReviewGateError("untrusted or absent review source SHA")
    if not isinstance(current_head, str) or not SHA.fullmatch(current_head):
        raise ReviewGateError("cannot verify current remote source SHA")
    if review_head != current_head:
        raise ReviewGateError("STALE_REVIEW: source HEAD changed since review started")
    if not isinstance(data, dict) or set(data) != {"status", "issues"}:
        raise ReviewGateError("review result missing required structured fields")
    if not isinstance(data["status"], str) or data["status"] not in STATUS or not isinstance(data["issues"], list):
        raise ReviewGateError("review result has invalid status or issue collection")
    counts = {"critical": 0, "warning": 0, "info": 0}
    for item in data["issues"]:
        if not isinstance(item, dict) or not isinstance(item.get("severity"), str) or item["severity"] not in SEVERITY:
            raise ReviewGateError("review issue has missing or unknown severity")
        if not isinstance(item.get("problem"), str) or not item["problem"].strip():
            raise ReviewGateError("review issue missing problem evidence")
        counts[item["severity"]] += 1
    if data["status"] == "critical" and not counts["critical"]:
        raise ReviewGateError("review status critical but issue list inconsistent")
    if counts["critical"]:
        raise ReviewGateError(f"BLOCKED: {counts['critical']} critical review issue(s)")
    if counts["warning"]:
        raise ReviewGateError(f"BLOCKED: {counts['warning']} warning issue(s) require fixes or separately authorized disposition")
    if data["status"] == "needs_modification" and not data["issues"]:
        raise ReviewGateError("review requires modification but provides no actionable issues")
    return counts

def gate_candidate(data, reviewed, current):
    """Snapshots come from trusted platform/ref readback, never from report JSON."""
    for key in ("source", "target", "merge"):
        for snapshot in (reviewed, current):
            value = snapshot.get(key)
            if not isinstance(value, str) or not SHA.fullmatch(value):
                raise ReviewGateError(f"missing trusted {key} SHA")
        if reviewed[key] != current[key]:
            raise ReviewGateError(f"STALE_REVIEW: {key} changed")
    return gate(data, reviewed["source"], current["source"])

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True)
    parser.add_argument("--review-head", required=True)
    parser.add_argument("--current-head", required=True)
    parser.add_argument("--review-target")
    parser.add_argument("--current-target")
    parser.add_argument("--review-merge")
    parser.add_argument("--current-merge")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.result).read_text(encoding="utf-8"))
        candidate = (args.review_target, args.current_target, args.review_merge, args.current_merge)
        if any(value is not None for value in candidate):
            counts = gate_candidate(data,
                {"source": args.review_head, "target": args.review_target, "merge": args.review_merge},
                {"source": args.current_head, "target": args.current_target, "merge": args.current_merge})
        else:
            counts = gate(data, args.review_head, args.current_head)
    except (ReviewGateError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"REVIEW_BLOCKED: {exc}", file=sys.stderr)
        return 1
    print(f"REVIEW_PASS: reviewed current source SHA; optional info findings: {counts['info']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
