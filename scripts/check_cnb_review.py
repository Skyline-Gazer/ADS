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
    if data["status"] not in STATUS or not isinstance(data["issues"], list):
        raise ReviewGateError("review result has invalid status or issue collection")
    counts = {"critical": 0, "warning": 0, "info": 0}
    for item in data["issues"]:
        if not isinstance(item, dict) or item.get("severity") not in SEVERITY:
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

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True)
    parser.add_argument("--review-head", required=True)
    parser.add_argument("--current-head", required=True)
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.result).read_text(encoding="utf-8"))
        counts = gate(data, args.review_head, args.current_head)
    except (ReviewGateError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"REVIEW_BLOCKED: {exc}", file=sys.stderr)
        return 1
    print(f"REVIEW_PASS: reviewed current source SHA; optional info findings: {counts['info']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
