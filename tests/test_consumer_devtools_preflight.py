"""Consumer initialization must fail closed before project mutations."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch
import hashlib
import json
import subprocess

SCRIPT = Path(__file__).resolve().parents[1] / 'templates/consumer-devtools/check-consumer-devtools.py'
SPEC = spec_from_file_location('preflight', SCRIPT)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def status(root, initialized=True, pending=0):
    return {'initialized': initialized, 'projectPath': str(root), 'indexPath': str(root / '.codegraph'),
            'worktreeMismatch': None, 'pendingChanges': {'added': pending, 'modified': 0, 'removed': 0},
            'index': {'reindexRecommended': False}}


class PreflightTests(TestCase):
    def test_project_initializes_once_and_queries(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "app.ts").write_text("source")
            with patch.object(MODULE, 'project_status', side_effect=[status(root, False), status(root)]), patch.object(MODULE, 'run', return_value='[{"node":{"name":"symbol","filePath":"app.ts"}}]' ) as run:
                MODULE.initialize_codegraph('cg', root, 'symbol', True)
            self.assertEqual(run.call_args_list[0].args[0], ['cg', 'init', str(root)])
            with patch.object(MODULE, 'project_status', return_value=status(root)), patch.object(MODULE, 'run', return_value='[{"node":{"name":"symbol","filePath":"app.ts"}}]' ) as run:
                MODULE.initialize_codegraph('cg', root, 'symbol', True)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0][1], 'query')

    def test_stale_index_requires_explicit_recovery(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "app.ts").write_text("source")
            with patch.object(MODULE, 'project_status', return_value=status(root, pending=1)), patch.object(MODULE, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'unhealthy'):
                    MODULE.initialize_codegraph('cg', root, 'symbol')
                run.assert_not_called()
            with patch.object(MODULE, 'project_status', side_effect=[status(root, pending=1), status(root)]), patch.object(MODULE, 'run', return_value='[{"node":{"name":"symbol","filePath":"app.ts"}}]' ) as run:
                MODULE.initialize_codegraph('cg', root, 'symbol', recover=True)
                self.assertEqual(run.call_args_list[0].args[0][1], 'sync')

    def test_status_rejects_shared_index_and_wrong_worktree(self):
        root = Path('/tmp/consumer')
        for key, value in [('projectPath', '/another'), ('indexPath', '/shared/index'), ('worktreeMismatch', True)]:
            payload = status(root)
            payload[key] = value
            with patch.object(MODULE, 'run', return_value=json.dumps(payload)):
                with self.assertRaises(ValueError):
                    MODULE.project_status('cg', root)

    def test_empty_query_and_malformed_status_fail_closed(self):
        with patch.object(MODULE, 'run', return_value='{}'):
            with self.assertRaises(ValueError):
                MODULE.project_status('cg', Path('/tmp'))
        root = Path('/tmp')
        with patch.object(MODULE, 'project_status', return_value=status(root)), patch.object(MODULE, 'run', return_value='[]'):
            with self.assertRaisesRegex(ValueError, 'query'):
                MODULE.initialize_codegraph('cg', root, 'symbol')

    def test_uninitialized_status_rejects_actual_external_index(self):
        root = Path('/tmp/consumer').resolve()
        value = status(root, False)
        value['indexPath'] = '/outside/custom-index'
        with patch.object(MODULE, 'run', return_value=json.dumps(value)):
            with self.assertRaisesRegex(ValueError, 'mismatch'):
                MODULE.project_status('cg', root)

    def test_error_json_is_not_a_source_query_result(self):
        root = Path('/tmp').resolve()
        for result in [{'error': 'symbol lookup failed'}, [{'node': {'name': 'other'}, 'query': 'symbol'}]]:
            with patch.object(MODULE, 'project_status', return_value=status(root)), patch.object(MODULE, 'run', return_value=json.dumps(result)):
                with self.assertRaisesRegex(ValueError, 'query'):
                    MODULE.initialize_codegraph('cg', root, 'symbol')

    def test_provenance_is_checked_before_binary_execution(self):
        with TemporaryDirectory() as tmp:
            evidence = Path(tmp) / 'evidence.json'
            evidence.write_text('{"tools":{"codegraph":{},"rtk":{}}}')
            policy = type('Policy', (), {'inspect': lambda *args: {'errors': []}})()
            with patch.object(MODULE, 'run', return_value='feat/task'), patch.object(MODULE.shutil, 'which', return_value='/untrusted/tool'), patch.object(MODULE, 'load_policy_module', return_value=policy), patch.object(MODULE, 'verify_executable', side_effect=ValueError('hash mismatch')), patch.object(MODULE, 'installed_version') as version:
                self.assertEqual(MODULE.main(['--evidence', str(evidence), '--query', 'symbol']), 1)
                version.assert_not_called()

    def test_external_codegraph_directory_is_rejected_before_status(self):
        with patch.dict(MODULE.os.environ, {'CODEGRAPH_DIR': '/outside/index'}), patch.object(MODULE, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'escapes'):
                MODULE.project_status('cg', Path('/tmp/consumer').resolve())
            run.assert_not_called()

    def test_attestation_binds_active_executable(self):
        with TemporaryDirectory() as tmp:
            binary = Path(tmp) / 'tool'
            binary.write_text('official distribution')
            item = {'executable': str(binary), 'executable_sha256': hashlib.sha256(binary.read_bytes()).hexdigest()}
            MODULE.verify_executable(item, str(binary))
            binary.write_text('substituted')
            with self.assertRaisesRegex(ValueError, 'hash'):
                MODULE.verify_executable(item, str(binary))

    def test_project_adapter_rejects_global_symlink_and_unknown_host(self):
        with TemporaryDirectory() as tmp, TemporaryDirectory() as outside:
            root = Path(tmp).resolve()
            (root / 'AGENTS.md').symlink_to(Path(outside) / 'AGENTS.md')
            with patch.object(MODULE, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'escapes'):
                    MODULE.initialize_rtk('rtk', root, 'codex', True)
                run.assert_not_called()
                with self.assertRaisesRegex(ValueError, 'explicit supported'):
                    MODULE.initialize_rtk('rtk', root, None, True)

    def test_rtk_uses_explicit_project_adapter_and_preserves_failure(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            def command(argv, cwd):
                if argv[1:3] == ['init', '--codex']:
                    (root / '.codex').mkdir()
                    (root / '.codex/hooks.json').write_text('{"hook":"rtk"}')
                return 'long raw git output' if argv[0] == 'git' else 'short'
            failure = subprocess.CompletedProcess([], 7, stdout='ADS_FAILURE_SENTINEL', stderr='')
            with patch.object(MODULE, 'run', side_effect=command) as run, patch.object(MODULE.subprocess, 'run', return_value=failure):
                MODULE.initialize_rtk('rtk', root, 'codex', True)
                self.assertEqual(run.call_args_list[0].args[0], ['rtk', 'init', '--codex'])
            failure.returncode = 0
            with patch.object(MODULE, 'run', side_effect=command), patch.object(MODULE.subprocess, 'run', return_value=failure):
                with self.assertRaisesRegex(ValueError, 'preserve failure'):
                    MODULE.initialize_rtk('rtk', root, 'codex')

    def test_production_blocks_before_tool_checks(self):
        with patch.object(MODULE, 'run', return_value='main'), patch.object(MODULE, 'installed_version') as installed:
            self.assertEqual(MODULE.main([]), 1)
            installed.assert_not_called()

    def test_missing_tools_require_consent_without_install(self):
        with patch.object(MODULE, 'run', return_value='feat/task'), patch.object(MODULE.shutil, 'which', return_value=None):
            self.assertEqual(MODULE.main([]), 1)


if __name__ == '__main__':
    main()
