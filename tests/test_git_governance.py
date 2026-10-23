import unittest
from pathlib import Path

from scripts.check_git_governance import validate_pull_request


def event(base, head, body="Refs #123"):
    return {
        "pull_request": {
            "base": {"ref": base},
            "head": {"ref": head},
            "body": body,
        }
    }


class GitGovernanceTests(unittest.TestCase):
    def test_task_branch_targets_dev_with_issue_reference(self):
        self.assertEqual(validate_pull_request(event("dev", "feat/123-user-auth")), [])

    def test_fix_branch_targets_dev(self):
        self.assertEqual(validate_pull_request(event("dev", "fix/124-timeout", "Closes #124")), [])

    def test_task_branch_cannot_target_production(self):
        errors = validate_pull_request(event("main", "feat/123-user-auth"))
        self.assertTrue(any("must come from" in error for error in errors))

    def test_dev_can_promote_to_production(self):
        self.assertEqual(validate_pull_request(event("main", "dev", "Release candidate; Refs #125")), [])

    def test_release_branch_can_target_production(self):
        self.assertEqual(validate_pull_request(event("main", "release/v0.4.0", "Release; Refs #126")), [])

    def test_hotfix_backport_can_target_production(self):
        self.assertEqual(validate_pull_request(event("main", "hotfix/127-crash", "Backport; Refs #127")), [])

    def test_unknown_base_is_rejected(self):
        errors = validate_pull_request(event("feature", "feat/123-user-auth"))
        self.assertTrue(any("unsupported PR base" in error for error in errors))

    def test_missing_issue_reference_is_rejected(self):
        errors = validate_pull_request(event("dev", "feat/user-auth", "Implement login"))
        self.assertTrue(any("must explicitly reference" in error for error in errors))

    def test_issue_reference_in_title_only_is_not_enough(self):
        errors = validate_pull_request(event("dev", "feat/user-auth", "Implement login #123"))
        self.assertTrue(any("must explicitly reference" in error for error in errors))

    def test_issue_reference_placeholder_comment_is_not_enough(self):
        body = "<!-- Required: Refs #123 or Closes #123 -->\nImplement login"
        errors = validate_pull_request(event("dev", "feat/user-auth", body))
        self.assertTrue(any("must explicitly reference" in error for error in errors))

    def test_direct_branch_as_task_head_is_rejected(self):
        errors = validate_pull_request(event("dev", "main"))
        self.assertTrue(any("separate task branch" in error for error in errors))

    def test_configurable_production_branch(self):
        self.assertEqual(validate_pull_request(event("production", "dev", "Release; Refs #125"), production_branch="production"), [])

    def test_missing_pull_request_payload_is_rejected(self):
        self.assertTrue(validate_pull_request({}))

    def test_consumer_template_checker_matches_canonical_checker(self):
        root = Path(__file__).resolve().parents[1]
        canonical = (root / "scripts" / "check_git_governance.py").read_text(encoding="utf-8")
        template = (root / "templates" / "git-governance" / "check_git_governance.py").read_text(encoding="utf-8")
        self.assertEqual(template, canonical)


if __name__ == "__main__":
    unittest.main()
