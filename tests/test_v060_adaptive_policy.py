"""Contract tests for v0.6.0 Adaptive Goal Execution (execution patch, Lite preserved)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V060AdaptivePolicyTests(unittest.TestCase):
    def test_deliver_defines_goal_contract_without_mandatory_files(self):
        deliver = (ROOT / "skills" / "deliver" / "SKILL.md").read_text(encoding="utf-8")
        # Keep the v0.6 behavior contract while allowing shorter v0.7 wording.
        lowered = deliver.lower()
        for concept in ("goal", "invariants", "acceptance", "scope", "stop"):
            self.assertIn(concept, lowered)
        self.assertIn("do not create a mandatory contract file", lowered)
        for concept in ("process", "state", "outcome", "merge"):
            self.assertIn(concept, lowered)
        self.assertIn("production deploy", deliver.lower())
        self.assertIn("cnb-review.md", deliver)
        self.assertNotIn("docs/recipes/", deliver)

    def test_recover_requires_takeover_and_state_reread(self):
        recover = (ROOT / "skills" / "recover" / "SKILL.md").read_text(encoding="utf-8")
        lowered = recover.lower()
        self.assertIn("reuse the existing task branch/pr", lowered)
        self.assertIn("reread real state", lowered)
        self.assertIn("provider", lowered)

    def test_quality_defines_evidence_classes(self):
        quality = (ROOT / "QUALITY.md").read_text(encoding="utf-8")
        for concept in ("Process", "State", "Outcome"):
            self.assertIn(concept, quality)
        self.assertIn("cnb-review.md", quality)
        self.assertIn("live state again", quality.lower())

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
