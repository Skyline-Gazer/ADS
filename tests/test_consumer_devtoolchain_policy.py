"""Contract tests for the optional consumer developer-toolchain profile."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ConsumerDevToolchainPolicyTests(unittest.TestCase):
    def test_policy_is_consumer_scoped_and_latest_stable(self):
        policy = (ROOT / "docs" / "consumer-dev-toolchain.md").read_text(encoding="utf-8")
        self.assertIn("consumer repositories that opted in", policy)
        self.assertIn("does **not** require CodeGraph or RTK to be installed or initialized in the ADS", policy)
        self.assertIn("latest stable upstream release", policy)
        self.assertIn("full RTK", policy)
        self.assertIn("development branch", policy)
        self.assertIn("production", policy)

    def test_codegraph_lifecycle_prefers_auto_sync_and_checks_freshness(self):
        policy = (ROOT / "docs" / "consumer-dev-toolchain.md").read_text(encoding="utf-8")
        self.assertIn("codegraph sync", policy)
        self.assertIn("codegraph status", policy)
        self.assertIn("native file watcher/auto-sync", policy)
        self.assertIn("Do not run `codegraph sync` after every source edit", policy)
        self.assertIn("Each independently indexed Git worktree must have its own index.", policy)
        self.assertIn("full reindexing", policy)

    def test_profile_and_lite_adoption_reference_toolchain_policy(self):
        profile = (ROOT / "profiles" / "consumer-devtoolchain" / "README.md").read_text(encoding="utf-8")
        self.assertIn("consumer-dev-toolchain.md", profile)
        lite = (ROOT / "docs" / "lite-adoption.md").read_text(encoding="utf-8")
        self.assertIn("consumer-devtoolchain", lite)
        self.assertIn("not part of lite", profile.lower())

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
