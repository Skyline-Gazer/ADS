"""Contract tests for the mandatory consumer developer-toolchain policy."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ConsumerDevToolchainPolicyTests(unittest.TestCase):
    def test_policy_is_consumer_scoped_and_latest_stable(self):
        policy = (ROOT / "docs" / "consumer-dev-toolchain.md").read_text(encoding="utf-8")
        self.assertIn("projects that adopt ADS", policy)
        self.assertIn("does **not** require CodeGraph or RTK to be installed or initialized in the ADS", policy)
        self.assertIn("latest stable upstream release", policy)
        self.assertIn("full RTK", policy)
        self.assertIn("development branch", policy)
        self.assertIn("production", policy)

    def test_codegraph_sync_and_status_are_mandatory(self):
        policy = (ROOT / "docs" / "consumer-dev-toolchain.md").read_text(encoding="utf-8")
        self.assertIn("codegraph sync", policy)
        self.assertIn("codegraph status", policy)
        self.assertIn("A file watcher is useful but does not replace the ADS checkpoint.", policy)

    def test_bootstrap_and_adopt_skills_reference_policy(self):
        for relative in ("skills/bootstrap/SKILL.md", "skills/adopt/SKILL.md"):
            content = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("consumer-dev-toolchain.md", content)
            self.assertIn("full RTK", content)
            self.assertIn("production", content)

    def test_consumer_manifest_does_not_pin_tool_versions(self):
        manifest = (ROOT / "templates" / "consumer-devtools" / ".ads-devtools.json.example").read_text(encoding="utf-8")
        self.assertIn('"version_policy": "latest-stable"', manifest)
        self.assertNotIn('"version":', manifest)
        self.assertIn('"edition": "full"', manifest)

    def test_generic_guard_is_separate_from_tool_integration(self):
        guard = (ROOT / "templates" / "consumer-devtools" / "check-production-boundary.py").read_text(encoding="utf-8")
        self.assertIn("policy enforcement", guard)
        self.assertIn(".ads-devtools.json", guard)
        self.assertIn("dev_only_paths", guard)


if __name__ == "__main__":
    unittest.main()
