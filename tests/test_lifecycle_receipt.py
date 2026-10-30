import copy
import unittest

from scripts.check_lifecycle_receipt import validate_receipt

A = "a" * 40
B = "b" * 40


def receipt():
    return {
        "schema_version": 1,
        "checkpoint": "POST_MERGE",
        "repository": "owner/repo",
        "provider": "github-primary",
        "source_sha": A,
        "target_sha": B,
        "observed_target_sha": B,
        "project_state": "PROJECT_UNVERIFIED",
        "verdict": "PARTIAL",
        "workloads": [
            {"kind": "container_e2e", "executor": "github-actions",
             "status": "PASS", "tested_sha": A,
             "evidence_url": "https://github.com/owner/repo/actions/runs/1"}
        ],
        "drift": [
            {"kind": "EVIDENCE_GAP", "status": "BLOCKED",
             "issue_url": "https://github.com/owner/repo/issues/1"}
        ],
    }


class LifecycleTests(unittest.TestCase):
    def test_valid_remote_receipt(self):
        self.assertEqual(validate_receipt(receipt(), A), [])

    def test_stale_source(self):
        self.assertTrue(any("stale" in x for x in validate_receipt(receipt(), B)))

    def test_remote_pass_needs_url(self):
        x = receipt()
        del x["workloads"][0]["evidence_url"]
        self.assertTrue(any("remote PASS" in e for e in validate_receipt(x)))

    def test_local_heavy_rejected(self):
        x = receipt()
        x["workloads"][0]["executor"] = "local"
        self.assertTrue(any("heavy local" in e for e in validate_receipt(x)))

    def test_scoped_fallback_allowed(self):
        x = receipt()
        x["workloads"][0].update(
            executor="local", local_exception_authorized=True,
            fallback_reason="Runner unavailable", remote_attempt_evidence_url="https://github.com/owner/repo/actions/runs/2")
        self.assertEqual(validate_receipt(x), [])

    def test_post_merge_readback_required(self):
        x = receipt()
        x["observed_target_sha"] = A
        self.assertTrue(any("readback" in e for e in validate_receipt(x)))

    def test_unresolved_drift_blocks_go(self):
        x = receipt()
        x["verdict"] = "GO"
        self.assertTrue(any("unresolved" in e for e in validate_receipt(x)))

    def test_unverified_project_phase_exit_no_go(self):
        x = receipt()
        x.update(checkpoint="PHASE_EXIT", verdict="GO", drift=[])
        self.assertTrue(any("PROJECT_UNVERIFIED" in e for e in validate_receipt(x)))

    def test_verified_project_needs_evidence(self):
        x = receipt()
        x["project_state"] = "VERIFIED"
        self.assertTrue(any("evidence" in e for e in validate_receipt(x)))

    def test_false_resolved_drift_rejected(self):
        x = receipt()
        x["drift"][0]["status"] = "RESOLVED"
        self.assertTrue(any("resolution" in e for e in validate_receipt(x)))

    def test_invalid_json_object_and_boolean_schema(self):
        self.assertTrue(validate_receipt([]))
        x = copy.deepcopy(receipt())
        x["schema_version"] = True
        self.assertTrue(validate_receipt(x))


if __name__ == "__main__":
    unittest.main()
