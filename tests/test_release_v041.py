"""Release gates use real isolated Git ancestry and a simulated GitHub API.

These tests never publish a remote tag/release or prove live GitHub permissions.
"""
from contextlib import redirect_stderr
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "release-v041.py"
SPEC = importlib.util.spec_from_file_location("release_v041", SCRIPT)
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)


class FakeGitHub:
    def __init__(self, target, main, notes):
        self.target, self.main, self.notes = target, main, notes
        self.tag = None
        self.release = None
        self.writes = []
        self.fail_release_once = False
        self.main_reads = 0
        self.drift_at = None
        self.invalidate_ci_at = None
        self.pr = {
            "merged": True, "state": "closed", "merge_commit_sha": target,
            "base": {"ref": "dev", "repo": {"full_name": RELEASE.REPOSITORY}},
            "head": {"sha": "b" * 40},
        }
        self.runs = {path: [{
            "id": index + 1, "run_attempt": 1, "head_sha": target, "path": path,
            "repository": {"full_name": RELEASE.REPOSITORY}, "head_branch": "dev",
            "event": "push", "status": "completed", "conclusion": "success",
        }] for index, path in enumerate(RELEASE.WORKFLOWS)}

    def matching_tag(self):
        self.tag = {
            "sha": "c" * 40, "type": "tag", "target": self.target,
        }

    def matching_release(self):
        self.release = {
            "id": 42, "tag_name": RELEASE.VERSION, "target_commitish": self.target,
            "name": "ADS v0.4.1", "body": self.notes,
            "draft": False, "prerelease": False,
        }

    def api(self, endpoint, *, payload=None, missing=False):
        prefix = f"repos/{RELEASE.REPOSITORY}/"
        if not endpoint.startswith(prefix):
            raise AssertionError("unexpected API repository")
        route = endpoint[len(prefix):]
        if payload is not None:
            self.writes.append((route, copy.deepcopy(payload)))
            if route == "git/tags":
                if payload["object"] != self.target:
                    raise AssertionError("wrong tag target")
                return {"sha": "c" * 40}
            if route == "git/refs":
                if self.tag is not None or payload["ref"] != "refs/tags/v0.4.1":
                    raise AssertionError("attempted tag overwrite or unrelated ref")
                self.matching_tag()
                return {"ref": payload["ref"], "object": {"sha": "c" * 40}}
            if route == "releases":
                if self.fail_release_once:
                    self.fail_release_once = False
                    raise RuntimeError("injected failure after the tag, before Release creation")
                if self.release is not None:
                    raise AssertionError("attempted duplicate Release creation")
                self.matching_release()
                return self.release
            raise AssertionError(f"unexpected mutation {route}")
        if route == "git/ref/heads/main":
            self.main_reads += 1
            if self.invalidate_ci_at and self.main_reads >= self.invalidate_ci_at:
                self.runs[RELEASE.WORKFLOWS[0]][0].update(run_attempt=2, status="in_progress", conclusion=None)
            sha = "f" * 40 if self.drift_at and self.main_reads >= self.drift_at else self.main
            return {"object": {"type": "commit", "sha": sha}}
        if route == "pulls/69":
            return self.pr
        if route.startswith("actions/workflows/"):
            filename = route.split("/")[2]
            return {"workflow_runs": self.runs[f".github/workflows/{filename}"]}
        if route == "git/ref/tags/v0.4.1":
            return {"object": {"type": self.tag["type"], "sha": self.tag["sha"]}} if self.tag else None
        if route == "git/tags/" + "c" * 40:
            return {"tag": RELEASE.VERSION, "object": {"type": "commit", "sha": self.tag["target"]}}
        if route == "releases/tags/v0.4.1":
            return self.release
        raise AssertionError(f"unexpected read {route}")


class ReleaseV041Tests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ads-v041-release-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "ADS release test")
        self.git("config", "user.email", "ads-test@example.invalid")
        self.write("release/v0.4-publish.json", '{"historical":"preserve"}\n')
        self.previous_main = self.commit("previous release audit history")
        self.notes = "# ADS v0.4.1\n\nConsumer governance fixes.\n\n## Known limitations\nNative host verification is separate.\n"
        self.write(RELEASE.NOTES, self.notes)
        self.target = self.commit("source candidate")
        self.manifest = {
            "version": RELEASE.VERSION, "release_approved": True,
            "release_target_sha": self.target, "previous_main_sha": self.previous_main,
            "source_pull_request": 69,
            "notes_sha256": hashlib.sha256(self.notes.encode()).hexdigest(),
            "private_consumer_ci": {
                "repository": RELEASE.SANDBOX, "workflow": "Private ADS Submodule Acceptance",
                "result": "success", "tested_ads_sha": self.target, "head_sha": "a" * 40,
                "pull_request_number": 18, "run_id": 1234,
                "run_url": f"https://github.com/{RELEASE.SANDBOX}/actions/runs/1234",
                "verification": "operator-verified-successful-run-and-job-logs",
            },
        }
        self.write(RELEASE.MANIFEST, json.dumps(self.manifest))
        self.main = self.commit("explicit publication manifest only")
        self.github = FakeGitHub(self.target, self.main, self.notes)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True, stderr=subprocess.PIPE).strip()

    def write(self, path, content):
        output = self.root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def execute(self, publish=False):
        return RELEASE.execute(self.root, self.manifest, self.main, self.github, publish)

    def blocked(self):
        with self.assertRaises((ValueError, RuntimeError)):
            self.execute(publish=True)
        self.assertEqual(self.github.writes, [])

    def test_read_only_validation_does_not_publish(self):
        result = self.execute()
        self.assertEqual(result["mode"], "VALIDATED_ONLY")
        self.assertEqual(self.github.writes, [])
        self.assertEqual(self.git("show", f"{self.target}:release/v0.4-publish.json"), '{"historical":"preserve"}')

    def test_exact_target_full_sha_and_owner_approval_required(self):
        for field, value in [("release_target_sha", self.target[:7]), ("release_approved", False),
                             ("version", "v0.4"), ("previous_main_sha", "main"), ("source_pull_request", True)]:
            with self.subTest(field=field):
                original = self.manifest[field]
                self.manifest[field] = value
                self.blocked()
                self.manifest[field] = original

    def test_notes_digest_and_version_are_frozen(self):
        self.write(RELEASE.NOTES, self.notes + "unapproved change\n")
        self.blocked()
        self.write(RELEASE.NOTES, self.notes.replace("# ADS v0.4.1", "# ADS v0.4"))
        self.manifest["notes_sha256"] = hashlib.sha256((self.root / RELEASE.NOTES).read_bytes()).hexdigest()
        self.blocked()

    def test_consumer_receipt_must_bind_exact_successful_independent_run(self):
        receipt = self.manifest["private_consumer_ci"]
        for field, value in [("result", "failure"), ("tested_ads_sha", "d" * 40),
                             ("repository", RELEASE.REPOSITORY), ("run_id", True),
                             ("run_url", "https://example.invalid"), ("verification", "self-reported")]:
            with self.subTest(field=field):
                original = receipt[field]
                receipt[field] = value
                self.blocked()
                receipt[field] = original

    def test_source_pr_must_be_merged_into_dev_at_exact_target(self):
        for field, value in [("merged", False), ("state", "open"), ("merge_commit_sha", "d" * 40)]:
            with self.subTest(field=field):
                original = self.github.pr[field]
                self.github.pr[field] = value
                self.blocked()
                self.github.pr[field] = original
        self.github.pr["base"]["ref"] = "main"
        self.blocked()

    def test_later_failure_or_pending_run_cannot_reuse_historical_success(self):
        path = RELEASE.WORKFLOWS[0]
        later = dict(self.github.runs[path][0], id=100, conclusion="failure")
        self.github.runs[path].append(later)
        self.blocked()
        later.update(status="in_progress", conclusion=None)
        self.blocked()

    def test_wrong_workflow_path_sha_branch_and_repository_are_rejected(self):
        run = self.github.runs[RELEASE.WORKFLOWS[0]][0]
        for field, value in [("path", ".github/workflows/unrelated.yml"), ("head_sha", "d" * 40),
                             ("head_branch", "feature/unreviewed"), ("event", "pull_request_target"), ("event", "pull_request"),
                             ("repository", {"full_name": "someone/fork"})]:
            with self.subTest(field=field):
                original = run[field]
                run[field] = value
                self.blocked()
                run[field] = original

    def test_checkout_tree_and_main_ancestry_are_required(self):
        self.write("unexpected.txt", "not in frozen target\n")
        self.main = self.commit("unapproved product difference")
        self.github.main = self.main
        self.blocked()

    def test_unrelated_previous_main_history_is_rejected(self):
        self.git("checkout", "--orphan", "unrelated")
        self.git("rm", "-rf", ".")
        self.write("unrelated.txt", "unrelated\n")
        self.manifest["previous_main_sha"] = self.commit("different history")
        self.git("checkout", "main")
        self.blocked()

    def test_remote_main_drift_before_write_is_rejected(self):
        self.github.drift_at = 2
        self.blocked()

    def test_remote_main_drift_after_tag_stops_release_creation(self):
        self.github.drift_at = 4
        with self.assertRaisesRegex(ValueError, "main drifted"):
            self.execute(publish=True)
        self.assertIsNotNone(self.github.tag)
        self.assertIsNone(self.github.release)

    def test_ci_rerun_after_validation_blocks_before_tag_write(self):
        self.github.invalidate_ci_at = 2
        self.blocked()
        self.assertIsNone(self.github.tag)

    def test_ci_invalidated_after_tag_blocks_release_and_can_resume(self):
        self.github.invalidate_ci_at = 4
        with self.assertRaisesRegex(ValueError, 'CI is not successful'):
            self.execute(publish=True)
        self.assertIsNotNone(self.github.tag)
        self.assertIsNone(self.github.release)
        self.github.invalidate_ci_at = None
        self.github.runs[RELEASE.WORKFLOWS[0]][0].update(status='completed', conclusion='success')
        self.assertEqual(self.execute(publish=True)['mode'], 'PUBLISHED')

    def test_tag_collision_and_lightweight_tag_are_rejected(self):
        self.github.matching_tag()
        self.github.tag["target"] = "e" * 40
        self.blocked()
        self.github.tag["target"] = self.target
        self.github.tag["type"] = "commit"
        self.blocked()

    def test_existing_release_without_tag_or_with_wrong_notes_is_rejected(self):
        self.github.matching_release()
        self.blocked()
        self.github.matching_tag()
        self.github.release["body"] = "wrong notes"
        self.blocked()

    def test_existing_release_target_or_draft_mismatch_is_rejected(self):
        self.github.matching_tag()
        self.github.matching_release()
        self.github.release["target_commitish"] = "main"
        self.blocked()
        self.github.release["target_commitish"] = self.target
        self.github.release["draft"] = True
        self.blocked()

    def test_publish_then_repeat_is_a_no_op(self):
        self.assertEqual(self.execute(publish=True)["mode"], "PUBLISHED")
        self.assertEqual([route for route, _ in self.github.writes], ["git/tags", "git/refs", "releases"])
        self.github.writes.clear()
        self.assertEqual(self.execute(publish=True)["mode"], "ALREADY_PUBLISHED")
        self.assertEqual(self.github.writes, [])

    def test_interruption_after_tag_is_resumable_without_replacing_tag(self):
        self.github.fail_release_once = True
        with self.assertRaisesRegex(RuntimeError, "injected failure"):
            self.execute(publish=True)
        original_tag = copy.deepcopy(self.github.tag)
        self.assertIsNotNone(original_tag)
        self.github.writes.clear()
        self.assertEqual(self.execute(publish=True)["mode"], "PUBLISHED")
        self.assertEqual(self.github.tag, original_tag)
        self.assertEqual([route for route, _ in self.github.writes], ["releases"])

    def test_cli_refuses_publication_outside_main_push(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(sys, "argv", [str(SCRIPT), "--expected-main-sha", self.main, "--publish"]), redirect_stderr(io.StringIO()):
            self.assertEqual(RELEASE.main(), 1)

    def test_api_permission_failure_is_not_mistaken_for_absence(self):
        github = RELEASE.GitHub(self.root)
        with patch.object(RELEASE, "command", side_effect=RuntimeError("gh: Forbidden (HTTP 403)")):
            with self.assertRaises(RuntimeError):
                github.api("test", missing=True)
        with patch.object(RELEASE, "command", side_effect=RuntimeError("gh: Not Found (HTTP 404)")):
            self.assertIsNone(github.api("test", missing=True))

    def test_empty_or_missing_current_consumer_lifecycle_ci_blocks_publication(self):
        self.github.runs[".github/workflows/v041-consumer-acceptance.yml"] = []
        self.blocked()


if __name__ == "__main__":
    unittest.main()
