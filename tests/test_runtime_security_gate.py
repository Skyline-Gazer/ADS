import json
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

    def test_verify_requires_full_evidence(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ev.json"
            p.write_text(json.dumps({"adapter": "macos-cli-seatbelt", "host": "macOS 27.0.1", "sensitive_data": True,
                                     "checks": [{"name": "outside_read", "expected": "DENIED", "observed": "ALLOWED"}]}))
            self.assertEqual(gate.verify("macos-cli-seatbelt", str(p), "macOS 27.0.1"), 2)  # UNSAFE + sensitive → fail closed

    def test_gate_does_not_rewire_default_entry(self):
        # governance docs must not instruct global alias modification
        doc = (ROOT / "docs" / "agent-runtime-security-governance.md").read_text()
        self.assertNotIn("alias omp=", doc)
        self.assertIn("owner-approved", doc)
