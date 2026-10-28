import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts import runtime_security_gate as gate

ROOT = Path(__file__).resolve().parents[1]

class RuntimeSecurityGateTests(unittest.TestCase):
    def test_adapters_present_and_typed(self):
        adapters = gate.all_adapters()
        for aid, a in adapters.items():
            self.assertIn("runtime_kinds", a)
            self.assertIn("status", a)
            if a["status"] == "supported":
                self.assertIn("command", a.get("verify", {}), f"{aid} claims support without a verify command")

    def test_macos_cli_adapter_is_only_supported(self):
        adapters = gate.all_adapters()
        supported = {k for k, a in adapters.items() if a["status"] == "supported"}
        self.assertEqual(supported, {"macos-cli-seatbelt"})

    def test_manifest_binds_current_generator(self):
        m = json.loads(gate.MANIFEST_PATH.read_text())
        self.assertEqual(m["manifest_version"], 1)
        gen = ROOT / "templates" / "host-security" / "gen_project_sandbox.py"
        self.assertEqual(m["generator_sha256"], hashlib.sha256(gen.read_bytes()).hexdigest())
        names = [c["name"] for c in m["required_checks"]]
        self.assertEqual(len(names), len(set(names)), "duplicate probe names in manifest")
        self.assertGreaterEqual(len(names), 40)

    def test_verify_fails_closed_on_forged_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ev.json"
            p.write_text(json.dumps({"adapter": "macos-cli-seatbelt", "host": "macOS 27.0.1",
                                     "checks": [{"name": "outside_read", "expected": "DENIED", "observed": "DENIED"}]}))
            self.assertEqual(gate.verify("macos-cli-seatbelt", str(p), "macOS 27.0.1"), 2)

    def test_verify_fails_closed_on_unsupported_adapter(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ev.jsonl"
            m = json.loads(gate.MANIFEST_PATH.read_text())
            rows = "".join(json.dumps(c) + "\n" for c in m["required_checks"])
            p.write_text(rows)
            # adapter 'claude-code' is planned: no support claim even with perfect evidence
            self.assertEqual(gate.verify("claude-code", str(p), "macOS 27.0.1"), 2)

    def test_gate_does_not_rewire_default_entry(self):
        doc = (ROOT / "docs" / "agent-runtime-security-governance.md").read_text()
        self.assertNotIn("alias omp=", doc)
        self.assertIn("owner-approved", doc)
