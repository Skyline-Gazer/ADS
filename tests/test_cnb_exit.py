"""Generic pin/configuration exit compatibility; no native service shutdown claim."""
from importlib.util import spec_from_file_location, module_from_spec
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from scripts.check_repository_provider import validate
from scripts.cnb_release_gate import main

ROOT = Path(__file__).resolve().parents[1]
GENERIC = '3abf6025657a5d716476029cc8cbf5239543210b'

class CNBExitTests(unittest.TestCase):
    def test_immutable_generic_pin_roundtrip_preserves_consumer_source(self):
        spec = spec_from_file_location('consumer_acceptance', ROOT / 'scripts/test-v041-consumer.py')
        consumer = module_from_spec(spec)
        spec.loader.exec_module(consumer)
        candidate = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        before = subprocess.check_output(['git', 'show-ref'], cwd=ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            result = consumer.pin_roundtrip(ROOT, candidate, Path(scratch), baseline=GENERIC)
        self.assertEqual(result['state'], 'PASS')
        self.assertEqual(result['stages'][-1]['ads_sha'], GENERIC)
        self.assertEqual(subprocess.check_output(['git', 'show-ref'], cwd=ROOT), before)

    def test_exit_to_github_rejects_queued_mode_b_action(self):
        cfg = json.loads((ROOT / 'templates/git-provider/.ads-project.json.example').read_text())
        cfg['git'].update(primary='github', github_mirror={'enabled': False, 'direction': 'disabled', 'branches': [], 'tags': 'disabled'})
        cfg['review'].update(auto='host-on-demand', npc='disabled')
        self.assertEqual(validate(cfg)['git']['primary'], 'github')
        with tempfile.TemporaryDirectory() as scratch:
            policy, approval = Path(scratch) / 'policy.json', Path(scratch) / 'approval.json'
            policy.write_text(json.dumps(cfg))
            approval.write_text('{}')
            self.assertEqual(main(['import', '--policy', str(policy), '--approval', str(approval), '--execute']), 1)
