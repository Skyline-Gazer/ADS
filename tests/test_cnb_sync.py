"""Offline real-Git fixture acceptance for one-way GitHub mirror."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from scripts.sync_cnb_release import MirrorError, manifest, synchronize

def git(cwd, *args):
    cp = subprocess.run(["git", "-C", str(cwd), *args], text=True, capture_output=True)
    if cp.returncode:
        raise RuntimeError(f"git failed: {args[0]}: {cp.stderr}")
    return cp.stdout.strip()

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.cnb = root / "cnb.git"
        self.github = root / "github.git"
        self.work = root / "work"
        git(root, "init", "--bare", str(self.cnb))
        git(root, "init", "--bare", str(self.github))
        git(root, "init", "-b", "main", str(self.work))
        git(self.work, "config", "user.email", "test@example.invalid")
        git(self.work, "config", "user.name", "ADS Test")
        git(self.work, "remote", "add", "origin", str(self.cnb))
        git(self.work, "remote", "add", "github", str(self.github))
        (self.work / "file.txt").write_text("first\n")
        git(self.work, "add", ".")
        git(self.work, "commit", "-m", "baseline")
        self.first = git(self.work, "rev-parse", "HEAD")
        git(self.work, "push", "origin", "main")
        git(self.work, "push", "github", "main")
        (self.work / "file.txt").write_text("second\n")
        git(self.work, "commit", "-am", "feature")
        self.second = git(self.work, "rev-parse", "HEAD")
        git(self.work, "tag", "-a", "v1.0.0", "-m", "release")
        git(self.work, "push", "origin", "main", "refs/tags/v1.0.0")
        self.m = {
            "release_approved": True, "github_push_effects_approved": True,
            "main_sha": self.second, "tag_name": "v1.0.0",
            "tag_target_sha": self.second
        }
        self.previous = Path.cwd()
        import os
        os.chdir(self.work)
        self.addCleanup(os.chdir, self.previous)

    def test_dry_run_does_not_mutate_github(self):
        result = synchronize(self.m, "origin", "github", execute=False)
        self.assertIn("DRY_RUN_PASS", result)
        self.assertEqual(git(self.github, "rev-parse", "refs/heads/main"), self.first)
        self.assertNotIn("refs/tags/v1.0.0", git(self.github, "show-ref"))

    def test_sync_is_exact_and_idempotent(self):
        self.assertIn("SYNC_VERIFIED", synchronize(self.m, "origin", "github", execute=True))
        self.assertIn("SYNC_VERIFIED", synchronize(self.m, "origin", "github", execute=True))
        self.assertEqual(git(self.github, "rev-parse", "refs/heads/main"), self.second)
        self.assertEqual(git(self.github, "rev-parse", "refs/tags/v1.0.0^{}"), self.second)
        self.assertNotIn("refs/heads/dev", git(self.github, "show-ref"))

    def test_github_divergence_blocks(self):
        git(self.work, "checkout", "-b", "other", self.first)
        (self.work / "file.txt").write_text("unrelated\n")
        git(self.work, "commit", "-am", "other change")
        git(self.work, "push", "github", "other:main")
        with self.assertRaisesRegex(MirrorError, "not an ancestor"):
            synchronize(self.m, "origin", "github", execute=True)

    def test_existing_tag_collision_blocks_before_main_update(self):
        git(self.work, "tag", "-f", "v1.0.0", self.first)
        git(self.work, "push", "github", "refs/tags/v1.0.0")
        git(self.work, "tag", "-d", "v1.0.0")
        git(self.work, "fetch", "origin", "refs/tags/v1.0.0:refs/tags/v1.0.0")
        with self.assertRaisesRegex(MirrorError, "collision"):
            synchronize(self.m, "origin", "github", execute=True)
        self.assertEqual(git(self.github, "rev-parse", "refs/heads/main"), self.first)

    def test_rejects_bad_manifest(self):
        path = self.work / "manifest.json"
        path.write_text(json.dumps(dict(self.m, github_push_effects_approved=False)))
        with self.assertRaisesRegex(MirrorError, "approvals"):
            manifest(path)
        path.write_text(json.dumps(dict(self.m, tag_name="refs/tags/*")))
        with self.assertRaisesRegex(MirrorError, "tag"):
            manifest(path)
        path.write_text(json.dumps(dict(self.m, extra_field="secret")))
        with self.assertRaises(MirrorError):
            manifest(path)

if __name__ == "__main__":
    unittest.main()
