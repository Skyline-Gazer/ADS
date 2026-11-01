"""A01: a stale CI step demands retired RTK/CodeGraph; repair the step, do not revive it.

Runs the fixture's workflow command in a temp copy. This is not a Markdown substring check.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "a01-stale-ci"
BOUNDARY = ROOT / "templates" / "consumer-devtools" / "check-production-boundary.py"
WORKFLOW = Path(".github/workflows/legacy-required.yml")
RUN_LINE = re.compile(r"^(\s*)-\s+run:\s+python3\s+(\S+)\s*$", re.M)
FORBIDDEN = (
    "RTK.md",
    ".ads-devtools.json",
    ".claude/settings.json",
    "codegraph.json",
    "contract.toml",
    ".codegraph",
)


def workflow_script(root: Path) -> str:
    text = (root / WORKFLOW).read_text(encoding="utf-8")
    match = RUN_LINE.search(text)
    if not match:
        raise AssertionError("workflow has no single python3 run step")
    return match.group(2)


def run_workflow_step(root: Path) -> subprocess.CompletedProcess[str]:
    script = root / workflow_script(root)
    env = None
    if script.name == "stale_ci.py":
        # Optional RTK/CodeGraph may exist on a real dev host. The retired step
        # must miss them because its own PATH is empty, not because this machine is.
        search = root.parent / "stale-ci-path"
        search.mkdir(exist_ok=True)
        env = os.environ.copy()
        env["PATH"] = str(search)
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def repair_stale_ci(root: Path) -> None:
    """Retarget the required step at the current goal. Do not recreate the toolchain."""
    path = root / WORKFLOW
    text = path.read_text(encoding="utf-8")
    if "python3 scripts/stale_ci.py" not in text:
        raise RuntimeError("fixture is not the retired harness")
    path.write_text(text.replace("python3 scripts/stale_ci.py", "python3 scripts/goal_check.py", 1), encoding="utf-8")
    revived = [rel for rel in FORBIDDEN if (root / rel).exists()]
    if revived:
        raise RuntimeError("repair revived " + ",".join(revived))


def files(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


class A01StaleHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        shutil.copytree(FIXTURE, self.root)

    def test_unrepaired_step_demands_retired_toolchain(self):
        self.assertEqual(workflow_script(self.root), "scripts/stale_ci.py")
        decoy = self.root.parent / "host-tools"
        decoy.mkdir()
        for name in ("rtk", "codegraph"):
            binary = decoy / name
            binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            binary.chmod(0o755)
        seen = subprocess.run(
            [sys.executable, str(self.root / "scripts" / "stale_ci.py")],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PATH": str(decoy)},
        )
        self.assertEqual(seen.returncode, 42, seen.stderr)
        self.assertIn("missing_bins=\n", seen.stderr)
        result = run_workflow_step(self.root)
        self.assertEqual(result.returncode, 42, result.stderr)
        self.assertIn("RETIRED_CAPABILITY_REQUIRED", result.stderr)
        self.assertIn("ACTION_DEMANDED=restore_v042_mandatory_toolchain", result.stderr)
        self.assertIn("missing_bins=rtk,codegraph", result.stderr)
        self.assertIn("RTK.md", result.stderr)
        self.assertIn("contract.toml", result.stderr)

    def test_repair_reruns_goal_without_adding_toolchain_files(self):
        before = files(self.root)
        repair_stale_ci(self.root)
        self.assertEqual(files(self.root), before)
        self.assertEqual(workflow_script(self.root), "scripts/goal_check.py")
        result = run_workflow_step(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "GOAL_OK")
        for rel in FORBIDDEN:
            self.assertFalse((self.root / rel).exists(), rel)
        boundary = subprocess.run(
            [sys.executable, str(BOUNDARY), "--root", str(self.root), "--target-branch", "main"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(boundary.returncode, 0, boundary.stderr)
        self.assertIn("PASS:", boundary.stdout)

    def test_repaired_goal_reads_yaml_contract(self):
        repair_stale_ci(self.root)
        (self.root / "contract.yaml").write_text("site_contract: toml-restored\n", encoding="utf-8")
        result = run_workflow_step(self.root)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("GOAL_FAIL site_contract", result.stderr)

    def test_reviving_toolchain_fails_goal_and_production_boundary(self):
        (self.root / "RTK.md").write_text("Use RTK for all shell commands.\n", encoding="utf-8")
        (self.root / ".ads-devtools.json").write_text('{"version_policy":"latest-stable"}\n', encoding="utf-8")
        claude = self.root / ".claude"
        claude.mkdir()
        (claude / "settings.json").write_text('{"hooks":{"command":"rtk"}}\n', encoding="utf-8")
        (self.root / "codegraph.json").write_text('{"exclude":[]}\n', encoding="utf-8")
        (self.root / "contract.toml").write_text('site_contract = "toml"\n', encoding="utf-8")
        stale = run_workflow_step(self.root)
        self.assertEqual(stale.returncode, 42, stale.stderr)
        self.assertIn("missing_bins=rtk,codegraph", stale.stderr)
        self.assertIn("missing_files=\n", stale.stderr)
        goal = subprocess.run(
            [sys.executable, str(self.root / "scripts" / "goal_check.py")],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(goal.returncode, 1, goal.stdout)
        self.assertIn("GOAL_FAIL revived=", goal.stderr)
        boundary = subprocess.run(
            [sys.executable, str(BOUNDARY), "--root", str(self.root), "--target-branch", "main"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(boundary.returncode, 1, boundary.stdout)
        self.assertIn("RTK.md", boundary.stderr)
        self.assertIn(".ads-devtools.json", boundary.stderr)
        self.assertIn("codegraph.json", boundary.stderr)


if __name__ == "__main__":
    unittest.main()
