"""Behavior tests for the standalone ADS checker; no third-party dependencies."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "check-ads.py"


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        shutil.copyfile(SOURCE, self.root / "scripts" / "check-ads.py")
        (self.root / "skills" / "bootstrap").mkdir(parents=True)
        (self.root / "skills" / "bootstrap" / "SKILL.md").write_text(
            "---\nname: bootstrap\ndescription: Create a project\n---\n# Bootstrap\n", encoding="utf-8"
        )
        (self.root / "README.md").write_text("# ADS\n[Skill](skills/bootstrap/SKILL.md)\n", encoding="utf-8")

    def check(self):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "check-ads.py")],
            cwd=self.root, capture_output=True, text=True, check=False,
        )

    def test_valid_fixture(self):
        self.assertEqual(self.check().returncode, 0)

    def test_link_titles_and_angle_brackets_are_accepted(self):
        (self.root / "README.md").write_text(
            '[Skill](skills/bootstrap/SKILL.md "Bootstrap")\n'
            "[Skill](<skills/bootstrap/SKILL.md>)\n",
            encoding="utf-8",
        )
        self.assertEqual(self.check().returncode, 0)

    def test_missing_angle_bracket_link_is_rejected(self):
        (self.root / "README.md").write_text("[Missing](<unknown.md>)\n", encoding="utf-8")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing link unknown.md", result.stderr)

    def test_reference_style_links_are_checked(self):
        (self.root / "README.md").write_text(
            "[Skill][ref]\n\n[ref]: skills/bootstrap/SKILL.md\n", encoding="utf-8"
        )
        self.assertEqual(self.check().returncode, 0)
        (self.root / "README.md").write_text("[Missing][ref]\n\n[ref]: unknown.md\n", encoding="utf-8")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing link unknown.md", result.stderr)

    def test_skill_asset_reference_is_checked(self):
        (self.root / "README.md").write_text("Read `skill://bootstrap/SKILL.md`.\n", encoding="utf-8")
        self.assertEqual(self.check().returncode, 0)
        (self.root / "README.md").write_text("Read `skill://bootstrap/templates/AGENTS.md`.\n", encoding="utf-8")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing skill asset skill://bootstrap/templates/AGENTS.md", result.stderr)


    def test_missing_link_is_rejected(self):
        (self.root / "README.md").write_text("[Missing](unknown.md)\n", encoding="utf-8")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing link", result.stderr)

    def test_old_pas_repository_is_rejected(self):
        (self.root / "README.md").write_text("https://github.com/Skyline-Gazer/PAS\n", encoding="utf-8")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale repository link", result.stderr)

    def test_invalid_skill_header_is_rejected(self):
        (self.root / "skills" / "bootstrap" / "SKILL.md").write_text(
            "---\nname: incorrect\ndescription: Wrong name\n---\n", encoding="utf-8"
        )
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid name/description", result.stderr)

    def test_missing_skill_is_rejected(self):
        (self.root / "skills" / "bootstrap" / "SKILL.md").unlink()
        self.assertNotEqual(self.check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
