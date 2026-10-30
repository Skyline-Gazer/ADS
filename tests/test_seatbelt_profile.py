import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GEN = Path(__file__).resolve().parent.parent / "templates" / "host-security" / "gen_project_sandbox.py"


def generate(target, *extra):
    return subprocess.run([sys.executable, str(GEN), target, *extra], capture_output=True, text=True, check=True).stdout


class SeatbeltProfileTests(unittest.TestCase):
    def test_generates_deny_default_with_project_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp) / "proj"
            proj.mkdir()
            real = os.path.realpath(proj)
            out = generate(str(proj))
        self.assertIn("(version 1)", out)
        self.assertIn("(deny file-read-data)", out)
        self.assertIn("(deny file-read-metadata)", out)
        self.assertIn("(deny file-write*)", out)
        self.assertIn(f'(allow file-read-data (subpath "{real}"))', out)
        self.assertIn(f'(allow file-write* (subpath "{real}"))', out)
        # resolution-only metadata grant: no listing of $HOME
        self.assertIn('(allow file-read-metadata (subpath "/"))', out)
        self.assertNotIn(f'(allow file-read-data (subpath "{os.path.realpath(Path.home())}"))', out)

    def test_private_dirs_explicitly_denied(self):
        out = generate("/tmp/whatever", "/Users/demo/Desktop/Oneplus")
        for private in ("/Documents", "/Downloads", "/Music", "/.ssh", "/Library/Keychains", "/Users/demo/Desktop/Oneplus"):
            self.assertIn(private, out)
        self.assertIn("(subpath \"/Volumes\")", out)
        self.assertIn("(subpath \"/private/var/log\")", out)

    def test_omp_state_and_scratch_write_scoped(self):
        out = generate("/tmp/whatever")
        for d in ("agent", "cache", "run", "logs", "extensions"):
            self.assertIn(f'.omp/{d}', out)
        self.assertIn('(subpath "/private/tmp/ads-agent-tmp")', out)
        self.assertIn('(subpath "/tmp")', out)  # tmp denied before scratch grant
        self.assertIn('(allow file-write* (subpath "/dev/null"))', out)
        self.assertIn('(literal "/")', out)  # dyld root requirement


if __name__ == "__main__":
    unittest.main()
