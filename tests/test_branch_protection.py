import unittest
from pathlib import Path

from scripts.ensure_branch_protection import (
    build_protection_payload,
    is_compliant,
    is_not_found_error,
)


class BranchProtectionTests(unittest.TestCase):
    def test_missing_protection_is_not_compliant(self):
        self.assertFalse(is_compliant(None, ["branch-policy"]))

    def test_compliant_protection_requires_all_controls(self):
        protection = {
            "required_status_checks": {"strict": True, "checks": [{"context": "branch-policy", "app_id": None}]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {"required_approving_review_count": 0, "dismiss_stale_reviews": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        self.assertTrue(is_compliant(protection, ["branch-policy"]))
        self.assertFalse(is_compliant(protection, ["branch-policy", "unit-tests"]))

    def test_admin_force_push_and_deletion_controls_are_mandatory(self):
        base = {
            "required_status_checks": {"strict": True, "contexts": ["branch-policy"]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {"required_approving_review_count": 0, "dismiss_stale_reviews": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        for key, value in (
            ("enforce_admins", {"enabled": False}),
            ("allow_force_pushes", {"enabled": True}),
            ("allow_deletions", {"enabled": True}),
            ("required_status_checks", {"strict": False, "contexts": ["branch-policy"]}),
            ("required_pull_request_reviews", None),
        ):
            changed = dict(base)
            changed[key] = value
            self.assertFalse(is_compliant(changed, ["branch-policy"]), key)

    def test_payload_enables_pr_checks_and_preserves_existing_restrictions(self):
        existing = {
            "required_status_checks": {
                "strict": False,
                "contexts": ["lint"],
                "checks": [{"context": "security", "app_id": 15368}],
            },
            "enforce_admins": {"enabled": False},
            "required_pull_request_reviews": {
                "required_approving_review_count": 2,
                "require_code_owner_reviews": True,
                "dismiss_stale_reviews": False,
                "require_last_push_approval": True,
            },
            "restrictions": {"url": "ignored", "users": [{"login": "release-bot"}], "teams": [], "apps": []},
            "allow_force_pushes": {"enabled": True},
            "allow_deletions": {"enabled": True},
            "required_linear_history": {"enabled": True},
        }
        payload = build_protection_payload(existing, ["branch-policy"])
        status = payload["required_status_checks"]
        self.assertTrue(status["strict"])
        self.assertEqual(status["contexts"], ["branch-policy", "lint", "security"])
        by_name = {item["context"]: item for item in status["checks"]}
        self.assertEqual(by_name["security"]["app_id"], 15368)
        self.assertNotIn("app_id", by_name["lint"])
        self.assertNotIn("app_id", by_name["branch-policy"])
        self.assertTrue(payload["enforce_admins"])
        self.assertEqual(payload["required_pull_request_reviews"]["required_approving_review_count"], 2)
        self.assertTrue(payload["required_pull_request_reviews"]["require_code_owner_reviews"])
        self.assertTrue(payload["required_pull_request_reviews"]["dismiss_stale_reviews"])
        self.assertTrue(payload["required_pull_request_reviews"]["require_last_push_approval"])
        self.assertEqual(payload["restrictions"]["users"], ["release-bot"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])
        self.assertTrue(payload["required_linear_history"])

    def test_not_found_detection_does_not_treat_forbidden_as_missing(self):
        self.assertTrue(is_not_found_error("gh: Not Found (HTTP 404)"))
        self.assertFalse(is_not_found_error("HTTP 403: Resource not accessible by integration"))

    def test_consumer_helper_matches_canonical_script(self):
        root = Path(__file__).resolve().parents[1]
        canonical = (root / "scripts" / "ensure_branch_protection.py").read_text(encoding="utf-8")
        template = (root / "templates" / "git-governance" / "ensure-ads-branch-protection.py").read_text(encoding="utf-8")
        self.assertEqual(template, canonical)


if __name__ == "__main__":
    unittest.main()
