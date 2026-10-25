"""Offline assertions for consumer CodeGraph/full RTK license evidence."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

SCRIPT = Path(__file__).resolve().parents[1] / "templates" / "consumer-devtools" / "check-license-compliance.py"
SPEC = spec_from_file_location("license_checker", SCRIPT)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

MIT = """MIT License
Permission is hereby granted, free of charge
THE SOFTWARE IS PROVIDED
"""
APACHE = """Apache License
Version 2.0
"""
BUSL = """Business Source License 1.1
Licensed Work: rtk-engine
Additional Use Grant: You may use the Licensed Work in production, without
charge; this grant does not permit offering the Licensed Work to third parties.
Change Date: 2030-09-09
Change License: Apache License, Version 2.0
"""


class LicenseComplianceTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, contents in [("CG-LICENSE", MIT), ("LICENSE", APACHE),
                               ("LICENSE-ENGINE", BUSL)]:
            (self.root / name).write_text(contents)
        self.evidence = {
            "schema_version": 1, "usage": "internal-development", "osi_only": False,
            "tools": {
                "codegraph": {
                    "version": "1.1.1", "edition": "cli",
                    "distribution_url": "https://registry.npmjs.org/@andysom25/codegraph/-/codegraph-1.1.1.tgz",
                    "installed_distribution_verified": True, "latest_stable_verified": True,
                    "license_file": "CG-LICENSE",
                },
                "rtk": {
                    "version": "0.20.0", "edition": "full",
                    "distribution_url": "https://github.com/rtk-ai/rtk/releases/download/v0.20.0/rtk-x86_64-unknown-linux-gnu.tar.gz",
                    "installed_distribution_verified": True, "latest_stable_verified": True,
                    "license_file": "LICENSE", "engine_license_file": "LICENSE-ENGINE",
                },
            },
        }

    def evaluate(self):
        return MODULE.inspect(self.evidence, self.root)

    def test_internal_dev_and_independent_delivery(self):
        self.assertEqual(self.evaluate()["state"], "PASS_WITH_ATTESTED_PROVENANCE")
        self.evidence["usage"] = "independent-software-delivery"
        self.assertEqual(self.evaluate()["errors"], [])

    def test_commercial_redistribution_requires_review(self):
        for usage in ("tool-redistribution", "hosted-rtk-service"):
            self.evidence["usage"] = usage
            self.assertEqual(self.evaluate()["state"], "BLOCKED")

    def test_osi_only_organization_conflicts_with_full_engine(self):
        self.evidence["osi_only"] = True
        self.assertEqual(self.evaluate()["state"], "BLOCKED")

    def test_wrong_edition_or_missing_provenance_blocks(self):
        self.evidence["tools"]["rtk"]["edition"] = "oss"
        self.assertEqual(self.evaluate()["state"], "BLOCKED")
        self.evidence["tools"]["rtk"]["edition"] = "full"
        self.evidence["tools"]["rtk"]["installed_distribution_verified"] = False
        self.assertEqual(self.evaluate()["state"], "BLOCKED")

    def test_missing_or_changed_license_text_blocks(self):
        self.evidence["tools"]["rtk"]["engine_license_file"] = "missing.txt"
        self.assertEqual(self.evaluate()["state"], "BLOCKED")
        self.evidence["tools"]["rtk"]["engine_license_file"] = "LICENSE-ENGINE"
        (self.root / "LICENSE-ENGINE").write_text(BUSL.replace("does not permit offering", "can offer"))
        self.assertEqual(self.evaluate()["state"], "BLOCKED")

    def test_stale_or_unversioned_distribution_blocks(self):
        self.evidence["tools"]["codegraph"]["latest_stable_verified"] = False
        self.assertEqual(self.evaluate()["state"], "BLOCKED")
        self.evidence["tools"]["codegraph"]["latest_stable_verified"] = True
        self.evidence["tools"]["codegraph"]["distribution_url"] = "https://registry.npmjs.org/@andysom25/codegraph/latest"
        self.assertEqual(self.evaluate()["state"], "BLOCKED")

    def test_rejects_oss_archive_mislabeled_full(self):
        self.evidence["tools"]["rtk"]["distribution_url"] = (
            "https://github.com/rtk-ai/rtk/releases/download/v0.20.0/rtk-oss-x86_64.tar.gz"
        )
        self.assertEqual(self.evaluate()["state"], "BLOCKED")
