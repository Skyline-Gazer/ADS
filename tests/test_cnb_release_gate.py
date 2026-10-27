"""Real bare-Git transport with explicitly simulated native review/protection.

These tests are supplementary; they do not attest CNB or Greptile execution.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from scripts import cnb_release_gate as gate

ROOT = Path(__file__).resolve().parents[1]

class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.old_cwd = Path.cwd()
        self.root = Path(self.scratch.name)
        self.work = self.root / 'work'
        self.work.mkdir()
        self.cnb = self.root / 'cnb.git'
        self.github = self.root / 'github.git'
        for remote in (self.cnb, self.github):
            subprocess.run(['git', 'init', '--bare', str(remote)], capture_output=True, check=True)
        os.chdir(self.work)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'ADS test')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.work / 'app.txt').write_text('baseline')
        self.git('add', '.')
        self.git('commit', '-m', 'baseline')
        self.base = self.sha()
        for name, location in [('cnb', self.cnb), ('github', self.github)]:
            self.git('remote', 'add', name, str(location))
            self.git('push', name, 'main')
        self.git('switch', '-c', 'dev')
        (self.work / '.ads-devtools.json').write_text('{"dev_only_paths":[".ads-devtools.json"]}')
        self.git('add', '.')
        self.git('commit', '-m', 'development integration')
        self.git('push', 'cnb', 'dev')
        self.git('push', 'github', 'dev')
        self.policy = json.loads((ROOT / 'templates/git-provider/mode-b.json.example').read_text())
        self.policy['review'].update(release_app_id=12, release_check='Greptile', ci_app_id=34, ci_check='verify')
        self.policy['release'].update(enabled=True, development_paths=['.ads-devtools.json'])
        self.identity = patch.object(gate, 'remote_identity', side_effect=lambda remote, host, repo: remote)
        self.identity.start()
        self.writer = patch.object(gate, 'require_verified_writer')
        self.writer.start()  # Explicit simulation; native writer enforcement remains unverified.

    def tearDown(self):
        self.identity.stop()
        self.writer.stop()
        os.chdir(self.old_cwd)
        self.scratch.cleanup()

    def git(self, *args):
        result = subprocess.run(['git', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def sha(self, ref='HEAD'):
        return self.git('rev-parse', ref)

    def candidate(self, round_number=1):
        self.git('switch', 'dev')
        (self.work / 'app.txt').write_text(f'round {round_number}')
        self.git('add', '.')
        self.git('commit', '-m', f'feature {round_number}')
        dev = self.sha()
        self.git('push', 'cnb', 'dev')
        branch = f'release/preparation-{round_number}'
        self.git('switch', '-c', branch)
        self.git('rm', '.ads-devtools.json')
        self.git('commit', '-m', 'strip only independent preparation')
        source = self.sha()
        self.git('push', 'cnb', branch)
        return {'schema_version': 1, 'action': 'import', 'source_sha': source, 'source_tree': self.sha('HEAD^{tree}'),
                'expected_target_sha': gate.live('github', 'refs/heads/dev'), 'development_sha': dev, 'source_branch': branch,
                'tag_name': None, 'tag_object': None, 'tag_target': None, 'github_pr': None, 'origin_event': 'cnb-approved-candidate'}

    def native_evidence(self, repository, endpoint):
        if endpoint.startswith('pulls/'):
            return [{'merged': True, 'merge_commit_sha': self.release['source_sha'], 'base': {'ref': 'main', 'repo': {'full_name': repository}}, 'head': {'ref': 'dev'}}]
        if endpoint.startswith('releases/tags/'):
            return [{'tag_name': self.release['tag_name'], 'draft': False}]
        if endpoint.endswith('/protection'):
            return [{'required_pull_request_reviews': {'required_approving_review_count': 1, 'dismiss_stale_reviews': True},
                     'required_status_checks': {'strict': True, 'checks': [{'context': 'Greptile', 'app_id': 12}, {'context': 'verify', 'app_id': 34}]},
                     'enforce_admins': {'enabled': True}, 'allow_force_pushes': {'enabled': False}, 'allow_deletions': {'enabled': False}}]
        return [{'check_runs': [{'id': i, 'name': name, 'app': {'id': app}, 'head_sha': self.release['source_sha'], 'status': 'completed', 'conclusion': 'success'}
                               for i, name, app in [(1, 'Greptile', 12), (2, 'verify', 34)]]}]

    def publish_github(self, manifest, round_number=1):
        self.git('switch', '-C', 'github-dev', manifest['expected_target_sha'])
        self.git('merge', '--no-ff', manifest['source_sha'], '-m', 'reviewed import PR (fixture)')
        self.git('push', 'github', 'HEAD:refs/heads/dev')
        previous_main = gate.live('cnb', 'refs/heads/main')
        self.git('switch', 'main')
        self.git('merge', '--no-ff', 'github-dev', '-m', 'approved release PR (fixture)')
        sha = self.sha()
        self.assertEqual(self.sha('HEAD^{tree}'), manifest['source_tree'])
        tag = f'v0.0.{round_number}-fixture'
        self.git('tag', '-a', tag, '-m', 'isolated annotated fixture')
        self.git('push', 'github', 'main', 'refs/tags/' + tag)
        self.release = {**manifest, 'action': 'copy', 'source_sha': sha, 'expected_target_sha': previous_main,
                        'tag_name': tag, 'tag_object': self.sha('refs/tags/' + tag), 'tag_target': sha,
                        'github_pr': round_number, 'origin_event': 'github-approved-release'}
        return self.release

    def test_two_rounds_import_copy_recovery_and_reconciliation(self):
        for number in (1, 2):
            manifest = self.candidate(number)
            old = gate.refs('github', 'refs/heads/*')
            self.assertEqual(gate.import_candidate(self.policy, manifest)['state'], 'DRY_RUN')
            self.assertEqual(gate.refs('github', 'refs/heads/*'), old)
            self.assertEqual(gate.import_candidate(self.policy, manifest, execute=True)['state'], 'IMPORTED')
            release = self.publish_github(manifest, number)
            if number == 1:
                self.git('push', 'cnb', 'main')  # interrupted after branch, before tag
            self.assertEqual(gate.copy_release(self.policy, release, execute=True, api=self.native_evidence)['state'], 'COPIED')
            self.assertEqual(gate.copy_release(self.policy, release, execute=True, api=self.native_evidence)['state'], 'ALREADY_COPIED')
            self.git('switch', 'dev')
            self.git('merge', '--no-ff', '--no-commit', release['source_sha'])
            self.git('restore', '--source', manifest['development_sha'], '--staged', '--worktree', '.ads-devtools.json')
            self.git('commit', '-m', 'reviewed reconciliation preserves tooling in same merge')
            self.assertEqual(gate.verify_reconciliation(manifest['development_sha'], release['source_sha'], self.sha(), ['.ads-devtools.json'])['state'], 'RECONCILIATION_VERIFIED')
            self.git('push', 'cnb', 'dev')

    def test_stale_candidate_wrong_direction_disabled_and_contamination(self):
        manifest = self.candidate()
        for key, value in [('source_sha', 'a' * 40), ('expected_target_sha', 'b' * 40), ('origin_event', 'github-approved-release')]:
            with self.subTest(key=key), self.assertRaises(gate.MirrorError):
                gate.import_candidate(self.policy, {**manifest, key: value}, execute=True)
        disabled = copy.deepcopy(self.policy)
        disabled['release']['enabled'] = False
        with self.assertRaises(gate.MirrorError):
            gate.import_candidate(disabled, manifest, execute=True)
        with self.assertRaises(gate.MirrorError):
            gate.verify_production_tree(manifest['development_sha'], ['.ads-devtools.json'])

    def test_forged_check_and_tag_collision_block_before_writes(self):
        manifest = self.candidate()
        release = self.publish_github(manifest)
        def forged(repository, endpoint):
            value = self.native_evidence(repository, endpoint)
            if endpoint.startswith('commits/'):
                value[0]['check_runs'][0]['app']['id'] = 999
            return value
        with self.assertRaisesRegex(gate.MirrorError, 'trusted App'):
            gate.copy_release(self.policy, release, execute=True, api=forged)
        self.git('push', 'cnb', self.base + ':refs/tags/' + release['tag_name'])
        with self.assertRaisesRegex(gate.MirrorError, 'collision'):
            gate.copy_release(self.policy, release, execute=True, api=self.native_evidence)
        self.assertEqual(gate.live('cnb', 'refs/heads/main'), self.base)

    def test_latest_failed_check_overrides_old_success(self):
        manifest = self.candidate()
        release = self.publish_github(manifest)
        def failed(repository, endpoint):
            result = self.native_evidence(repository, endpoint)
            if endpoint.startswith('commits/'):
                result[0]['check_runs'].append({'id': 9, 'name': 'Greptile', 'app': {'id': 12}, 'head_sha': release['source_sha'], 'status': 'completed', 'conclusion': 'failure'})
            return result
        with self.assertRaisesRegex(gate.MirrorError, 'not successful'):
            gate.copy_release(self.policy, release, api=failed)

    def test_writes_are_blocked_without_verified_native_exclusive_writer(self):
        manifest = self.candidate()
        self.writer.stop()
        with self.assertRaisesRegex(gate.MirrorError, 'exclusive native publication writer'):
            gate.import_candidate(self.policy, manifest, execute=True)

    def test_release_preparation_cannot_hide_product_edits_or_unlisted_tool_paths(self):
        manifest = self.candidate()
        (self.work / 'app.txt').write_text('unreviewed product edit')
        self.git('add', 'app.txt')
        self.git('commit', '-m', 'unreviewed extra')
        self.git('push', 'cnb', manifest['source_branch'])
        manifest.update(source_sha=self.sha(), source_tree=self.sha('HEAD^{tree}'))
        with self.assertRaisesRegex(gate.MirrorError, 'outside approved'):
            gate.import_candidate(self.policy, manifest)
        with self.assertRaisesRegex(gate.MirrorError, 'must be covered'):
            gate.verify_clean_preparation(manifest['development_sha'], manifest['source_sha'], ['different-path'])

    def test_missing_native_required_check_blocks(self):
        manifest = self.candidate()
        release = self.publish_github(manifest)
        def missing(repository, endpoint):
            result = self.native_evidence(repository, endpoint)
            if endpoint.endswith('/protection'):
                result[0]['required_status_checks']['checks'].pop()
            return result
        with self.assertRaisesRegex(gate.MirrorError, 'protection is unverified'):
            gate.copy_release(self.policy, release, api=missing)

class RemoteIdentityTests(unittest.TestCase):
    def test_canonical_repo_and_no_embedded_credentials(self):
        for url, accepted in [('https://cnb.cool/group/repo.git', True), ('https://github.com/group/repo', False),
                              ('https://user:password@cnb.cool/group/repo', False), ('https://cnb.cool/other/repo', False)]:
            with patch.object(gate, 'git', return_value=subprocess.CompletedProcess([], 0, stdout=url)), self.subTest(url=url):
                if accepted:
                    self.assertEqual(gate.remote_identity('cnb', 'cnb.cool', 'group/repo'), 'cnb')
                else:
                    with self.assertRaises(gate.MirrorError): gate.remote_identity('cnb', 'cnb.cool', 'group/repo')

    def test_rejects_substituted_or_multiple_effective_push_urls(self):
        def result(*args):
            value = 'https://cnb.cool/group/repo.git'
            if '--push' in args:
                value = 'https://cnb.cool/group/other.git'
            return subprocess.CompletedProcess([], 0, stdout=value)
        with patch.object(gate, 'git', side_effect=result), self.assertRaises(gate.MirrorError):
            gate.remote_identity('cnb', 'cnb.cool', 'group/repo')
        with patch.object(gate, 'git', return_value=subprocess.CompletedProcess([], 0, stdout='https://cnb.cool/group/repo\nhttps://cnb.cool/group/repo')):
            with self.assertRaises(gate.MirrorError): gate.remote_identity('cnb', 'cnb.cool', 'group/repo')
