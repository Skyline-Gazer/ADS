"""Real Git compatibility rehearsal; runtime tools are tested separately in CI."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("v041_consumer", ROOT / "scripts/test-v041-consumer.py")
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ConsumerCompatibilityTests(unittest.TestCase):
    def test_v04_candidate_v04_preserves_consumer_source_and_history(self):
        candidate = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
        with tempfile.TemporaryDirectory() as directory:
            result = MODULE.pin_roundtrip(ROOT, candidate, Path(directory))
        self.assertEqual(result["state"], "PASS")
        self.assertEqual([stage["ads_sha"] for stage in result["stages"]],
                         [MODULE.STABLE, candidate, MODULE.STABLE])
        self.assertEqual(len({stage["consumer_sha"] for stage in result["stages"]}), 3)
        self.assertEqual(result["private_remote_access"], "NOT_TESTED")

    def test_nonimmutable_candidate_is_rejected_before_creating_consumer(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            with self.assertRaises(ValueError):
                MODULE.pin_roundtrip(ROOT, "dev", scratch)
            self.assertFalse((scratch / "pin-consumer").exists())


if __name__ == "__main__":
    unittest.main()
