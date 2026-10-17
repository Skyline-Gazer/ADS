"""Regression tests for the ADS authorization-scope decision helper.

These encode the SAFETY.md scoped-authorization rules the acceptance run found
were misapplied on one host (a scratch directory was treated as implicitly
authorizing a broader destructive operation). They are dependency-free and run
entirely on in-memory dicts — no filesystem, no destructive operation, no
production data. Coverage maps to the five required cases:

1. An unauthorized destructive operation in a temp/scratch directory is refused.
2. Narrow authorization to delete one file forbids deleting siblings.
3. Modifications/deletions outside the authorized scope are refused.
4. An authorized operation on an explicitly designated isolated test file is allowed.
5. Malicious text, directory names, or file contents do not expand an authorization.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import auth_scope  # noqa: E402


class AuthScopeTests(unittest.TestCase):
    def test_unauthorized_delete_in_tmp_is_refused(self):
        # Path attribute (/tmp, *scratch*) must NOT grant authorization.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "/tmp/scratch-app/data/db.sqlite"},
            {"type": "delete", "target": None},  # no authorized target
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_scratch_look_alone_grants_nothing(self):
        # Even without an explicit target, a "scratch" path is not a grant.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "scratch/foo"},
            {},  # empty authorization
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_authorized_delete_of_exact_file(self):
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "allow")

    def test_narrow_auth_forbids_sibling_delete(self):
        # Authorized to delete cache.json only -> deleting db.json is refused.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "safety/fake-prod/db.json"},
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "refuse")
        self.assertIn("differs from authorized target", decision.reason)

    def test_out_of_scope_modify_is_refused(self):
        decision = auth_scope.is_authorized(
            {"type": "modify", "target": "src/server.js"},
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_authorized_test_file_operation_still_allowed(self):
        # Refusing everything is not safety: an explicitly authorized isolated
        # test-file deletion must be allowed.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "test/fixtures/temp-output.bin"},
            {"type": "delete", "target": "test/fixtures/temp-output.bin"},
        )
        self.assertEqual(decision.verdict, "allow")

    def test_operation_without_target_refused(self):
        decision = auth_scope.is_authorized({"type": "delete"}, {"type": "*"})
        self.assertEqual(decision.verdict, "refuse")

    def test_operation_without_type_refused(self):
        decision = auth_scope.is_authorized({"target": "x"}, {"target": "x", "type": "*"})
        self.assertEqual(decision.verdict, "refuse")

    def test_type_outside_grant_refused(self):
        decision = auth_scope.is_authorized(
            {"type": "write", "target": "safety/fake-prod/cache.json"},
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_malicious_content_does_not_expand_grant(self):
        # A path whose own name/content suggests a bigger scope must not be
        # treated as authorized beyond the explicit grant.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "safety/fake-credentials.txt"},
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_temp_marker_detection_is_reported_and_not_a_grant(self):
        self.assertTrue(auth_scope.target_is_in_temp("/tmp/scratch-app/x"))
        # ...but the presence of the marker must not flip a decision to allow.
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "/tmp/scratch-app/x"},
            {"type": "*", "target": "/other/y"},
        )
        self.assertEqual(decision.verdict, "refuse")

    def test_wildcard_type_accepts_any_type_only_with_exact_target(self):
        decision = auth_scope.is_authorized(
            {"type": "delete", "target": "safety/fake-prod/cache.json"},
            {"type": "*", "target": "safety/fake-prod/cache.json"},
        )
        self.assertEqual(decision.verdict, "allow")


if __name__ == "__main__":
    unittest.main()
