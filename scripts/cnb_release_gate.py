#!/usr/bin/env python3
"""Mode B candidate import and approved GitHub -> CNB publication copy.

Dry-run by default. Policy and approval are supplied by the protected controller,
not by the candidate checkout. Native PR merges/releases stay provider-owned.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

if __package__:
    from .sync_cnb_release import git, oid, refs, SHA_RE, TAG_RE, MirrorError
    from .check_repository_provider import validate, ProviderError
else:
    from sync_cnb_release import git, oid, refs, SHA_RE, TAG_RE, MirrorError
    from check_repository_provider import validate, ProviderError


def require(value, message):
    if not value:
        raise MirrorError(message)


def remote_identity(remote, host, repository):
    require(re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', remote), 'named remote required')
    url = git('remote', 'get-url', remote).stdout.strip()
    parsed = urlsplit(url)
    require(parsed.scheme == 'https' and parsed.hostname == host and not parsed.username and
            not parsed.password and not parsed.query and not parsed.fragment and not parsed.port and
            parsed.path.removesuffix('.git') == '/' + repository, 'remote identity differs from trusted policy')
    return remote


def live(remote, ref):
    value = refs(remote, ref).get(ref)
    require(value and SHA_RE.fullmatch(value), 'required live ref is absent')
    return value


def ancestor(parent, child):
    require(git('merge-base', '--is-ancestor', parent, child, check=False).returncode == 0,
            'required release ancestry is absent')


def check_manifest(manifest, action):
    fields = {'schema_version', 'action', 'source_sha', 'source_tree', 'expected_target_sha',
              'tag_name', 'tag_object', 'tag_target', 'github_pr', 'origin_event', 'development_sha', 'source_branch'}
    require(isinstance(manifest, dict) and set(manifest) == fields and type(manifest['schema_version']) is int and manifest['schema_version'] == 1,
            'invalid release approval fields')
    require(manifest['action'] == action and manifest['origin_event'] == ('cnb-approved-candidate' if action == 'import' else 'github-approved-release'),
            'wrong authority/event direction; reject sync loops')
    for key in ('source_sha', 'source_tree', 'expected_target_sha'):
        require(isinstance(manifest[key], str) and SHA_RE.fullmatch(manifest[key]), 'invalid immutable ' + key)
    require(isinstance(manifest['development_sha'], str) and SHA_RE.fullmatch(manifest['development_sha']), 'approved development SHA required')
    require(isinstance(manifest['source_branch'], str) and re.fullmatch(r'release/[A-Za-z0-9._/-]+', manifest['source_branch']) and '..' not in manifest['source_branch'], 'reviewed release-preparation branch required')
    if action == 'copy':
        for key in ('tag_object', 'tag_target'):
            require(isinstance(manifest[key], str) and SHA_RE.fullmatch(manifest[key]), 'invalid ' + key)
        require(isinstance(manifest['tag_name'], str) and TAG_RE.fullmatch(manifest['tag_name']), 'exact approved release tag required')
        require(type(manifest['github_pr']) is int and manifest['github_pr'] > 0, 'native release PR required')
    else:
        require(all(manifest[key] is None for key in ('tag_name', 'tag_object', 'tag_target', 'github_pr')), 'candidate imports cannot publish releases')
    return manifest


def github_api(repository, endpoint):
    result = subprocess.run(['gh', 'api', f'repos/{repository}/{endpoint}', '--paginate', '--slurp'],
                            capture_output=True, text=True, timeout=45)
    require(result.returncode == 0, 'native GitHub evidence unavailable')
    try:
        pages = json.loads(result.stdout)
        require(isinstance(pages, list) and pages, 'empty native GitHub evidence')
        return pages
    except json.JSONDecodeError as exc:
        raise MirrorError('malformed native GitHub evidence') from exc


def verify_github_release(policy, manifest, api=github_api):
    repository = policy['git']['github_repository']
    pr = api(repository, f'pulls/{manifest["github_pr"]}')[0]
    require(pr.get('merged') is True and pr.get('merge_commit_sha') == manifest['source_sha'] and
            pr.get('base', {}).get('ref') == 'main' and pr.get('base', {}).get('repo', {}).get('full_name') == repository,
            'release is not the approved native merged main PR')
    require(pr.get('head', {}).get('ref') == 'dev' or re.fullmatch(r'release/.+', pr.get('head', {}).get('ref', '')),
            'release PR does not follow reviewed promotion')
    protection = api(repository, 'branches/main/protection')[0]
    require(protection.get('required_pull_request_reviews') is not None and protection.get('enforce_admins', {}).get('enabled') is True and protection.get('allow_force_pushes', {}).get('enabled') is False and protection.get('allow_deletions', {}).get('enabled') is False, 'native GitHub main protection is unverified')
    checks = [check for page in api(repository, f'commits/{manifest["source_sha"]}/check-runs?per_page=100') for check in page.get('check_runs', [])]
    for app_key, check_key in [('release_app_id', 'release_check'), ('ci_app_id', 'ci_check')]:
        trusted = [check for check in checks if check.get('name') == policy['review'][check_key] and
                   check.get('app', {}).get('id') == policy['review'][app_key]]
        require(trusted, 'trusted App/check is absent on the exact release candidate')
        latest = max(trusted, key=lambda check: check.get('id', 0))
        require(latest.get('head_sha') == manifest['source_sha'] and latest.get('status') == 'completed' and latest.get('conclusion') == 'success',
                'latest exact-candidate Review/CI check is not successful')
    return pr


def verify_production_tree(sha, development_paths):
    from importlib.util import spec_from_file_location, module_from_spec
    guard_path = Path(__file__).resolve().parents[1] / 'templates/consumer-devtools/check-production-boundary.py'
    spec = spec_from_file_location('cnb_production_guard', guard_path)
    guard = module_from_spec(spec)
    spec.loader.exec_module(guard)
    with tempfile.TemporaryDirectory(prefix='ads-cnb-release-tree-') as scratch:
        root = Path(scratch) / 'candidate'
        git('worktree', 'add', '--detach', str(root), sha)
        try:
            require(not guard.violations(root), 'production tree contains developer tooling')
            for name in development_paths:
                require(not (root / name).exists() and not (root / name).is_symlink(), 'custom development path leaked into production')
        finally:
            git('worktree', 'remove', str(root))


def import_candidate(policy, manifest, cnb='cnb', github='github', execute=False):
    check_manifest(manifest, 'import')
    remote_identity(cnb, 'cnb.cool', policy['git']['cnb_repository'])
    remote_identity(github, 'github.com', policy['git']['github_repository'])
    require(live(cnb, 'refs/heads/dev') == manifest['development_sha'], 'CNB dev moved since approval')
    source_ref = 'refs/heads/' + manifest['source_branch']
    git('check-ref-format', source_ref)
    require(live(cnb, source_ref) == manifest['source_sha'], 'clean preparation branch moved')
    require(live(github, 'refs/heads/dev') == manifest['expected_target_sha'], 'GitHub dev moved since approval')
    git('fetch', '--no-tags', cnb, 'refs/heads/dev', source_ref)
    ancestor(manifest['development_sha'], manifest['source_sha'])
    require(oid(manifest['source_sha'] + '^{tree}') == manifest['source_tree'], 'frozen candidate tree mismatch')
    verify_production_tree(manifest['source_sha'], policy['release']['development_paths'])
    ref = 'refs/heads/' + policy['git']['transfer_prefix'] + manifest['source_sha']
    existing = refs(github, ref).get(ref)
    require(existing in (None, manifest['source_sha']), 'transfer ref collision')
    if execute:
        require(policy['release']['enabled'] is True, 'Mode B execution is disabled')
        require(live(cnb, 'refs/heads/dev') == manifest['development_sha'] and live(cnb, source_ref) == manifest['source_sha'] and live(github, 'refs/heads/dev') == manifest['expected_target_sha'], 'refs moved before import')
        if existing is None:
            git('push', github, manifest['source_sha'] + ':' + ref)
        require(live(github, ref) == manifest['source_sha'], 'transfer readback mismatch')
    return {'state': 'IMPORTED' if execute else 'DRY_RUN', 'ref': ref, 'sha': manifest['source_sha'], 'next': 'reviewed transfer PR to GitHub dev; separate release PR to main'}


def copy_release(policy, manifest, cnb='cnb', github='github', execute=False, api=github_api):
    check_manifest(manifest, 'copy')
    remote_identity(cnb, 'cnb.cool', policy['git']['cnb_repository'])
    remote_identity(github, 'github.com', policy['git']['github_repository'])
    verify_github_release(policy, manifest, api)
    tag = 'refs/tags/' + manifest['tag_name']
    expected = {'refs/heads/main': manifest['source_sha'], tag: manifest['tag_object'], tag + '^{}': manifest['tag_target']}
    require(refs(github, *expected) == expected, 'authoritative GitHub release/tag drift')
    git('fetch', '--no-tags', github, 'refs/heads/main', tag)
    require(oid(manifest['source_sha'] + '^{tree}') == manifest['source_tree'], 'released tree differs from approval')
    verify_production_tree(manifest['source_sha'], policy['release']['development_paths'])
    require(git('cat-file', '-t', manifest['tag_object']).stdout.strip() == 'tag', 'annotated tag object required')
    require(oid(manifest['tag_object'] + '^{commit}') == manifest['tag_target'], 'annotated tag target mismatch')
    ancestor(manifest['tag_target'], manifest['source_sha'])
    before = refs(cnb, 'refs/heads/main', tag, tag + '^{}')
    require(before.get('refs/heads/main') in (manifest['expected_target_sha'], manifest['source_sha']), 'CNB main drift; no overwrite')
    require(before.get(tag) in (None, manifest['tag_object']) and before.get(tag + '^{}') in (None, manifest['tag_target']), 'immutable CNB tag collision')
    ancestor(before['refs/heads/main'], manifest['source_sha'])
    if execute:
        require(policy['release']['enabled'] is True, 'Mode B execution is disabled')
        verify_github_release(policy, manifest, api)
        require(refs(github, *expected) == expected and refs(cnb, *expected) == before, 'provider refs moved before publication copy')
        if before['refs/heads/main'] != manifest['source_sha']:
            git('push', cnb, manifest['source_sha'] + ':refs/heads/main')
        require(live(cnb, 'refs/heads/main') == manifest['source_sha'], 'PARTIAL: branch copy failed; tag withheld')
        require(refs(github, *expected) == expected, 'PARTIAL: GitHub release drift; tag withheld')
        if tag not in before:
            git('push', cnb, manifest['tag_object'] + ':' + tag)
        require(refs(cnb, *expected) == expected, 'PARTIAL: publication readback failed; retain refs for safe retry')
    return {'state': ('ALREADY_COPIED' if before == expected else 'COPIED') if execute else 'DRY_RUN', 'release_sha': manifest['source_sha'], 'tag_object': manifest['tag_object'], 'tag_target': manifest['tag_target'], 'next': 'reviewed CNB dev reconciliation preserving development files'}


def verify_reconciliation(previous_dev, release, reconciled, dev_paths):
    for sha in (previous_dev, release, reconciled):
        require(isinstance(sha, str) and SHA_RE.fullmatch(sha), 'immutable reconciliation SHA required')
    ancestor(previous_dev, reconciled)
    ancestor(release, reconciled)
    for name in dev_paths:
        require(isinstance(name, str) and name and not name.startswith('/') and '..' not in Path(name).parts, 'invalid development path')
        require(oid(previous_dev + ':' + name) == oid(reconciled + ':' + name), 'reconciliation deleted/changed development integration')
    return {'state': 'RECONCILIATION_VERIFIED', 'sha': reconciled}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['import', 'copy'])
    parser.add_argument('--policy', required=True)
    parser.add_argument('--approval', required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args(argv)
    try:
        root = Path(git('rev-parse', '--show-toplevel').stdout.strip()).resolve()
        for filename in (args.policy, args.approval):
            require(not Path(filename).resolve().is_relative_to(root), 'policy/approval must come from outside the untrusted candidate checkout')
        policy = validate(json.loads(Path(args.policy).read_text()))
        require(policy['schema_version'] == 2, 'Mode B requires separate schema v2')
        approval = json.loads(Path(args.approval).read_text())
        function = import_candidate if args.action == 'import' else copy_release
        print(json.dumps(function(policy, approval, execute=args.execute), sort_keys=True))
        return 0
    except (MirrorError, ProviderError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f'RELEASE_GATE_BLOCKED: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
