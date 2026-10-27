import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GEN = Path(__file__).resolve().parent.parent / "templates" / "host-security" / "gen_project_sandbox.py"


class SeatbeltProfileTests(unittest.TestCase):
    def test_generates_profile_with_project_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp) / "proj"
            proj.mkdir()
            real = Path(os.path.realpath(proj))
            out = subprocess.run(
                [sys.executable, str(GEN), str(proj)], capture_output=True, text=True, check=True
            ).stdout
        self.assertIn("(version 1)", out)
        self.assertIn(f'(require-not (subpath "{real}"))', out)
        self.assertIn('(subpath "/private/tmp/ads-agent-tmp")', out)

    def test_private_dirs_explicitly_denied(self):
        out = subprocess.run(
            [sys.executable, str(GEN), "/tmp/whatever"], capture_output=True, text=True, check=True
        ).stdout
        for private in ("/Documents", "/Downloads", "/Music", "/.ssh", "/Library/Keychains"):
            self.assertIn(f'(subpath "', out)
            self.assertIn(private, out)

    def test_write_containment_present(self):
        out = subprocess.run(
            [sys.executable, str(GEN), "/tmp/whatever"], capture_output=True, text=True, check=True
        ).stdout
        self.assertGreaterEqual(out.count("(deny file-write*"), 2)
        self.assertIn(f'(require-not (subpath "{Path("/tmp/whatever").resolve()}"))', out)


if __name__ == "__main__":
    unittest.main()
