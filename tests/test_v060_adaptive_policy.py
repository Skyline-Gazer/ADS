"""Contract tests for v0.6.0 Adaptive Goal Execution (execution patch, Lite preserved)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V060AdaptivePolicyTests(unittest.TestCase):
    def test_deliver_defines_goal_contract_without_mandatory_files(self):
        deliver = (ROOT / "skills" / "deliver" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Goal Contract", deliver)
        self.assertIn("Invariants", deliver)
        self.assertIn("create a new file for ordinary tasks", deliver)
        self.assertIn("Process", deliver)
        self.assertIn("Outcome", deliver)
        self.assertIn("Convergence", deliver)
        self.assertIn("production deploy", deliver.lower())
        self.assertIn("cnb-review.md", deliver)
        self.assertNotIn("docs/recipes/", deliver)

    def test_recover_requires_takeover_and_state_reread(self):
        recover = (ROOT / "skills" / "recover" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("take over", recover.lower())
        self.assertIn("re-read actual state", recover.lower())
        self.assertIn("Provider", recover)

    def test_quality_defines_evidence_classes(self):
        quality = (ROOT / "QUALITY.md").read_text(encoding="utf-8")
        self.assertIn("Process, State, and Outcome evidence", quality)
        self.assertIn("cnb-review.md", quality)
        self.assertIn("re-read", quality.lower())

    def test_lite_baseline_not_reverted(self):
        lite = (ROOT / "docs" / "lite-adoption.md").read_text(encoding="utf-8")
        self.assertIn("normative default", lite.lower())
        profiles = (ROOT / "profiles" / "README.md").read_text(encoding="utf-8")
        self.assertIn("not enabled by default", profiles.lower())
        template = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("lite default", template.lower())
        self.assertNotIn("Mandatory consumer developer toolchain", template)

    def test_release_doc_states_design_constraint(self):
        plan = (ROOT / "docs" / "releases" / "v0.6.0.md").read_text(encoding="utf-8")
        self.assertIn("execution-semantics patch", plan)
        self.assertIn("not a second standards inflation", plan)


if __name__ == "__main__":
    unittest.main()
