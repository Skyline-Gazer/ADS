"""Hermetic tests for the probe instrument (NOT real macOS TUI enforcement)."""
from pathlib import Path
import tempfile
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from host_filesystem_probe import measure  # noqa: E402


class SyntheticWorkspaceBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.ws = root / "workspace"
        self.out = root / "synthetic-private"
        self.ws.mkdir()
        self.out.mkdir()
        self.inside = self.ws / "ADS_ALLOWED_PROBE.txt"
        self.inside.write_text("ADS_ALLOWED_PROBE_V1\n", encoding="utf8")
        self.outside = self.out / "ADS_DENIED_PROBE.txt"
        self.outside.write_text("SYNTHETIC_ONLY", encoding="utf8")
        self.link = self.ws / "ADS_OUTSIDE_LINK"
        self.link.symlink_to(self.outside)

    def test_unsandboxed_reads_are_detected_not_marked_safe(self):
        result = measure(self.inside, self.outside, self.link)
        self.assertEqual(result["verdict"], "UNSAFE")
        self.assertEqual(result["inside_read"], "PASS")
        self.assertEqual(result["vectors"]["python_read"], "UNSAFE")
        self.assertEqual(result["vectors"]["directory_listing"], "UNSAFE")
        self.assertEqual(result["vectors"]["symlink_read"], "UNSAFE")
        self.assertEqual(result["tui_or_mcp_coverage"], "NOT_TESTED")

    def test_missing_outside_fixture_is_not_proof_of_denial(self):
        self.outside.unlink()
        result = measure(self.inside, self.outside, None)
        self.assertNotEqual(result["verdict"], "VERIFIED_BOUNDED_PROBE")
        self.assertEqual(result["vectors"]["python_read"], "NOT_TESTED")

    def test_missing_inside_control_fails(self):
        self.inside.unlink()
        self.assertEqual(measure(self.inside, self.outside, None)["verdict"], "BLOCKED")

    def test_refuse_non_fixture_paths(self):
        with self.assertRaises(ValueError):
            measure(self.inside, self.out / "Music", None)
        with self.assertRaises(ValueError):
            measure(self.inside, self.outside, self.ws / "unexpected")

    def test_no_interference_with_fixtures(self):
        before = self.outside.read_bytes()
        measure(self.inside, self.outside, self.link)
        self.assertEqual(self.outside.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
