#!/usr/bin/env python3
"""Ensure classic GitHub branch protection via the authenticated gh CLI."""
import argparse
import json
import re
import subprocess
import sys
from urllib.parse import quote


class GhError(RuntimeError):
    pass


def run_gh(args, input_text=None):
    """Run gh without a shell, preserving stderr for actionable API errors."""
    try:
        result = subprocess.run(
            ["gh", *args],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise GhError("GitHub CLI `gh` is not installed or not on PATH.") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "unknown gh error").strip()
        raise GhError(detail)
    return result.stdout.strip()


def is_not_found_error(message):
    return bool(re.search(r"\bHTTP\s+404\b|\bNot Found\b", message, re.IGNORECASE))


def protection_contexts(protection):
    """Return all required status-check context names from a protection response."""
    status = (protection or {}).get('required_status_checks') or {}
    contexts = set(status.get('contexts') or [])
    contexts.update(
        item.get('context') for item in (status.get('checks') or [])
        if isinstance(item, dict) and item.get('context')
    )
    return contexts


def is_compliant(protection, required_checks):
    if not isinstance(protection, dict):
        return False
    status = protection.get('required_status_checks')
    if not isinstance(status, dict) or status.get('strict') is not True:
        return False
    if not set(required_checks).issubset(protection_contexts(protection)):
        return False
    admins = protection.get('enforce_admins')
    if not (admins is True or (isinstance(admins, dict) and admins.get('enabled') is True)):
        return False
    reviews = protection.get('required_pull_request_reviews')
    if not isinstance(reviews, dict) or reviews.get('dismiss_stale_reviews') is not True:
        return False
    for key in ('allow_force_pushes', 'allow_deletions'):
        flag = protection.get(key)
        if not (flag is False or (isinstance(flag, dict) and flag.get('enabled') is False)):
            return False
    return True


def _names_from_rule(value, key):
    """Convert GET response objects to the string names accepted by the PUT API."""
    items = (value or {}).get(key) or [] if isinstance(value, dict) else []
    names = []
    for item in items:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict):
            name = item.get({'users': 'login', 'teams': 'slug', 'apps': 'slug'}[key])
            if name:
                names.append(name)
    return names


def _normalize_rule(value):
    if not isinstance(value, dict):
        return value
    return {key: _names_from_rule(value, key) for key in ('users', 'teams', 'apps')}


def build_protection_payload(existing, required_checks):
    """Strengthen protection without removing existing checks/review requirements/restrictions."""
    existing = existing or {}
    old_status = existing.get('required_status_checks') or {}
    check_by_context = {}
    for item in old_status.get('checks') or []:
        if isinstance(item, dict) and item.get('context'):
            check = {'context': item['context']}
            if item.get('app_id') is not None:
                check['app_id'] = item['app_id']
            check_by_context[item['context']] = check
    contexts = set(old_status.get('contexts') or [])
    contexts.update(check_by_context)
    contexts.update(required_checks)
    for context in contexts:
        check_by_context.setdefault(context, {'context': context})

    old_reviews = existing.get('required_pull_request_reviews') or {}
    reviews = {
        'dismiss_stale_reviews': True,
        'require_code_owner_reviews': bool(old_reviews.get('require_code_owner_reviews', False)),
        'required_approving_review_count': max(0, int(old_reviews.get('required_approving_review_count', 0) or 0)),
        'require_last_push_approval': bool(old_reviews.get('require_last_push_approval', False)),
    }
    for key in ('dismissal_restrictions', 'bypass_pull_request_allowances'):
        value = old_reviews.get(key)
        if isinstance(value, dict):
            reviews[key] = _normalize_rule(value)

    restrictions = _normalize_rule(existing.get('restrictions')) if existing.get('restrictions') is not None else None
    payload = {
        'required_status_checks': {
            'strict': True,
            'contexts': sorted(check_by_context),
            'checks': [check_by_context[key] for key in sorted(check_by_context)],
        },
        'enforce_admins': True,
        'required_pull_request_reviews': reviews,
        'restrictions': restrictions,
        'allow_force_pushes': False,
        'allow_deletions': False,
    }
    for key in ('required_linear_history', 'block_creations', 'required_conversation_resolution', 'lock_branch', 'allow_fork_syncing'):
        value = existing.get(key)
        if isinstance(value, dict) and 'enabled' in value:
            payload[key] = bool(value['enabled'])
    return payload


def api_json(endpoint, method=None, payload=None):
    args = ['api']
    if method:
        args.extend(['--method', method])
    args.append(endpoint)
    if payload is not None:
        args.extend(['--input', '-'])
        output = run_gh(args, json.dumps(payload))
    else:
        output = run_gh(args)
    return json.loads(output) if output else {}


def get_protection(repo, branch):
    endpoint = f"repos/{repo}/branches/{quote(branch, safe='')}/protection"
    try:
        return api_json(endpoint)
    except GhError as exc:
        if is_not_found_error(str(exc)):
            return None
        raise GhError(
            f"Cannot inspect branch protection for {repo}:{branch}: {exc}. "
            "Do not assume the branch is unprotected. Confirm gh authentication, repository-admin permission, and GitHub plan support."
        ) from exc


def ensure_branch(repo, branch, required_checks, dry_run=False):
    branch_endpoint = f"repos/{repo}/branches/{quote(branch, safe='')}"
    try:
        api_json(branch_endpoint)
    except GhError as exc:
        if is_not_found_error(str(exc)):
            raise GhError(f"Required branch {repo}:{branch} does not exist. Establish it through a reviewable migration before enabling protection.") from exc
        raise GhError(f"Cannot verify branch {repo}:{branch}: {exc}. Confirm repository access before changing protection.") from exc

    current = get_protection(repo, branch)
    if is_compliant(current, required_checks):
        print(f"{branch}: already protected; required checks, PR gate, admin enforcement, force-push and deletion controls verified.")
        return

    payload = build_protection_payload(current, required_checks)
    action = 'enable' if current is None else 'strengthen'
    if dry_run:
        print(f"{branch}: would {action} classic branch protection with:")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    endpoint = f"repos/{repo}/branches/{quote(branch, safe='')}/protection"
    try:
        api_json(endpoint, method='PUT', payload=payload)
    except GhError as exc:
        raise GhError(
            f"Could not {action} protection for {repo}:{branch}: {exc}. "
            "This normally requires repository-admin access and a GitHub plan that supports branch protection for this repository. "
            "Do not mark ADS adoption complete until protection is verified or the owner records an explicit, accepted limitation."
        ) from exc

    verified = get_protection(repo, branch)
    if not is_compliant(verified, required_checks):
        raise GhError(f"{repo}:{branch} protection update returned but verification failed; inspect the branch protection settings manually.")
    print(f"{branch}: protection {action}d and verified.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', help='owner/repository; defaults to the current gh repository')
    parser.add_argument('--branches', nargs='+', default=['dev', 'main'], help='existing branches to protect (default: dev main)')
    parser.add_argument('--required-check', action='append', dest='required_checks', default=[], help='exact required CI check name; repeat for each required check')
    parser.add_argument('--dry-run', action='store_true', help='show intended changes without applying them')
    args = parser.parse_args(argv)
    required_checks = sorted({item.strip() for item in args.required_checks if item.strip()})
    if not required_checks:
        parser.error("at least one --required-check is required; inspect the real CI check names instead of guessing")
    if any(not re.fullmatch(r'[A-Za-z0-9_. /()\-]+', name) for name in required_checks):
        parser.error("required check names contain unsupported characters")

    try:
        run_gh(["auth", "status"])
        repo = args.repo
        if not repo:
            repo = run_gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
            raise GhError(f"Invalid repository name {repo!r}; expected owner/repository.")
        for branch in args.branches:
            if not re.fullmatch(r'[A-Za-z0-9_.\-/]+', branch) or branch.startswith('-'):
                raise GhError(f"Invalid branch name {branch!r}.")
            ensure_branch(repo, branch, required_checks, dry_run=args.dry_run)
    except (GhError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
