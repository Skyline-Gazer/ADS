#!/usr/bin/env python3
"""Validate the GitHub pull-request branch model required by ADS."""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ISSUE_REFERENCE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?|refs?|references?)\s+#(\d+)\b", re.IGNORECASE)
TASK_BRANCH = re.compile(r"^(?:feat|feature|fix|bugfix|chore|docs|refactor|test|ci|build|perf|style|deps|dependabot|renovate|security|sec|infra|ops|revert|spike|experiment|maintenance|upgrade)/.+$")
RELEASE_BRANCH = re.compile(r"^release/.+$")
HOTFIX_BRANCH = re.compile(r"^hotfix/.+$")


def referenced_issue_numbers(body):
    """Return unique Issue numbers explicitly referenced outside HTML comments."""
    visible_body = re.sub(r"<!--.*?-->", "", body or "", flags=re.DOTALL)
    return sorted({int(match.group(1)) for match in ISSUE_REFERENCE.finditer(visible_body)})


def validate_pull_request(event, development_branch="dev", production_branch="main"):
    """Return policy violations for a GitHub pull_request event payload."""
    pull_request = event.get("pull_request")
    if not isinstance(pull_request, dict):
        return ["event payload does not contain a pull_request object"]

    base = pull_request.get("base", {}).get("ref", "")
    head = pull_request.get("head", {}).get("ref", "")
    body = pull_request.get("body") or ""
    errors = []

    if not base or not head:
        return ["pull request payload is missing base/head branch names"]

    if base == development_branch:
        if head in {development_branch, production_branch}:
            errors.append("task PR must use a separate task branch, not a protected integration/production branch")
        elif not TASK_BRANCH.fullmatch(head):
            errors.append(f"PR targeting {development_branch!r} must come from a recognized task branch; got {head!r}")
    elif base == production_branch:
        if head != development_branch and not (RELEASE_BRANCH.fullmatch(head) or HOTFIX_BRANCH.fullmatch(head)):
            errors.append(f"PR targeting {production_branch!r} must come from {development_branch!r}, release/*, or hotfix/*; got {head!r}")
    else:
        errors.append(f"unsupported PR base {base!r}; ordinary work targets {development_branch!r}, production promotion targets {production_branch!r}")

    if not referenced_issue_numbers(body):
        errors.append("PR description must explicitly reference a GitHub Issue (for example, Refs #123 or Closes #123)")
    return errors


def verify_issue_references(body, repository, token):
    """Verify that referenced numbers resolve to Issues (not PRs) when API access is available."""
    numbers = referenced_issue_numbers(body)
    if not token or not repository:
        return [], False
    errors = []
    for number in numbers:
        url = f"https://api.github.com/repos/{repository}/issues/{number}"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                errors.append(f"referenced Issue #{number} does not exist in or is not accessible from {repository}")
            else:
                errors.append(f"could not verify Issue #{number}: GitHub API returned HTTP {exc.code}")
            continue
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            errors.append(f"could not verify Issue #{number}: {type(exc).__name__}")
            continue
        if "pull_request" in payload:
            errors.append(f"#{number} is a pull request, not an Issue; reference the owning Issue")
    return errors, True


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH is required for pull-request policy validation", file=sys.stderr)
        return 2
    try:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read GitHub event payload: {exc}", file=sys.stderr)
        return 2
    errors = validate_pull_request(
        event,
        development_branch=os.environ.get("ADS_DEVELOPMENT_BRANCH", "dev"),
        production_branch=os.environ.get("ADS_PRODUCTION_BRANCH", "main"),
    )
    pull_request = event.get("pull_request") or {}
    repository = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not errors:
        issue_errors, verified = verify_issue_references(pull_request.get('body') or '', repository, token)
        errors.extend(issue_errors)
        if not verified:
            print("WARNING: Issue existence could not be verified without GITHUB_TOKEN and GITHUB_REPOSITORY; only reference syntax was checked.", file=sys.stderr)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Git governance check passed for PR base, branch type, and Issue reference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
