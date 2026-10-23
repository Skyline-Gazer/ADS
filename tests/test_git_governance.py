import unittest
from pathlib import Path
from io import BytesIO
from unittest.mock import patch
import urllib.error

from scripts.check_git_governance import referenced_issue_numbers, validate_pull_request, verify_issue_references


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

    def test_normative_policy_is_referenced_by_ads_and_consumer_entrypoints(self):
        root = Path(__file__).resolve().parents[1]
        policy = (root / "docs" / "git-governance.md").read_text(encoding="utf-8")
        self.assertIn("applies equally to the ADS repository and every project that adopts ADS", policy)
        self.assertIn("latest `dev`", policy)
        for relative in ("STANDARD.md", "QUALITY.md", "AGENTS.md", "templates/AGENTS.md", "skills/adopt/SKILL.md", "skills/bootstrap/SKILL.md", "skills/deliver/SKILL.md", "skills/recover/SKILL.md", "docs/agent-adoption.md"):
            self.assertIn("git-governance.md", (root / relative).read_text(encoding="utf-8"), relative)

    def test_adoption_and_bootstrap_enable_branch_protection_with_gh(self):
        root = Path(__file__).resolve().parents[1]
        policy = (root / "docs" / "git-governance.md").read_text(encoding="utf-8")
        self.assertIn("scripts/ensure_branch_protection.py", policy)
        self.assertIn("a `403` means the state could not be inspected", policy)
        self.assertIn("does not create branches or change the default branch", policy)
        for relative in ("skills/adopt/SKILL.md", "skills/bootstrap/SKILL.md", "templates/AGENTS.md", "docs/agent-adoption.md", "templates/git-governance/README.md"):
            content = (root / relative).read_text(encoding="utf-8")
            self.assertIn("gh", content, relative)
            self.assertIn("ensure-ads-branch-protection.py", content, relative)

    def test_delivery_skill_does_not_allow_direct_commits_to_integration_branches(self):
        root = Path(__file__).resolve().parents[1]
        delivery = (root / "skills" / "deliver" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("PR targeting `dev`", delivery)
        self.assertNotIn("authorized direct-commit path", delivery)

    def test_consumer_template_checker_matches_canonical_checker(self):
        root = Path(__file__).resolve().parents[1]
        canonical = (root / "scripts" / "check_git_governance.py").read_text(encoding="utf-8")
        template = (root / "templates" / "git-governance" / "check_git_governance.py").read_text(encoding="utf-8")
        self.assertEqual(template, canonical)

    def test_issue_numbers_ignore_html_comments_and_deduplicate(self):
        body = "Refs #45 and Closes #48\n<!-- placeholder: Refs #999 -->\nRefs #45"
        self.assertEqual(referenced_issue_numbers(body), [45, 48])

    def test_issue_reference_must_resolve_to_a_real_issue(self):
        payload = b'{"number":48,"title":"Git governance"}'
        with patch("scripts.check_git_governance.urllib.request.urlopen", return_value=BytesIO(payload)):
            errors, verified = verify_issue_references("Refs #48", "Skyline-Gazer/ADS", "test-token")
        self.assertTrue(verified)
        self.assertEqual(errors, [])

    def test_pull_request_reference_is_not_accepted_as_an_issue(self):
        payload = b'{"number":49,"title":"PR","pull_request":{"url":"https://api.github.com/..."}}'
        with patch("scripts.check_git_governance.urllib.request.urlopen", return_value=BytesIO(payload)):
            errors, verified = verify_issue_references("Refs #49", "Skyline-Gazer/ADS", "test-token")
        self.assertTrue(verified)
        self.assertTrue(any("not an Issue" in error for error in errors))

    def test_nonexistent_issue_is_rejected(self):
        error = urllib.error.HTTPError("https://api.github.com/repos/Skyline-Gazer/ADS/issues/999", 404, "Not Found", {}, None)
        with patch("scripts.check_git_governance.urllib.request.urlopen", side_effect=error):
            errors, verified = verify_issue_references("Refs #999", "Skyline-Gazer/ADS", "test-token")
        self.assertTrue(verified)
        self.assertTrue(any("does not exist" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
