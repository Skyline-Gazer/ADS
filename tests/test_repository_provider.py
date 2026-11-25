"""Test project-specific provider contracts without network or dependencies."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_repository_provider import ProviderError, load, validate, main

EXAMPLE = Path(__file__).resolve().parents[1] / "templates/git-provider/.ads-project.json.example"

class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(EXAMPLE.read_text())

    def test_cnb(self):
        self.assertEqual(validate(self.cfg)["git"]["primary"], "cnb")

    def test_cnb_review_feedback_choices(self):
        for choice in ("host-on-demand", "cnb-code-review"):
            with self.subTest(choice=choice):
                self.cfg["review"]["auto"] = choice
                self.assertEqual(validate(self.cfg)["review"]["auto"], choice)
        self.cfg["review"]["auto"] = "silently-approve"
        with self.assertRaises(ProviderError):
            validate(self.cfg)

    def test_cnb_primary_lite_without_mirror(self):
        self.cfg["git"]["github_mirror"] = {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}
        self.cfg["review"]["auto"] = "host-on-demand"
        self.assertEqual(validate(self.cfg)["git"]["primary"], "cnb")

    def test_lite_custom_development_branch(self):
        for primary in ("cnb", "github"):
            with self.subTest(primary=primary):
                cfg = copy.deepcopy(self.cfg)
                cfg["git"]["primary"] = primary
                cfg["git"]["development_branch"] = "develop"
                cfg["git"]["production_branch"] = "main"
                cfg["git"]["github_mirror"] = {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}
                cfg["review"].update(auto="host-on-demand", npc="disabled")
                self.assertEqual(validate(cfg)["git"]["development_branch"], "develop")

    def test_lite_main_only_without_mirror(self):
        for primary in ("cnb", "github"):
            with self.subTest(primary=primary):
                cfg = copy.deepcopy(self.cfg)
                cfg["git"]["primary"] = primary
                cfg["git"]["development_branch"] = "main"
                cfg["git"]["production_branch"] = "main"
                cfg["git"]["github_mirror"] = {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}
                cfg["review"].update(auto="host-on-demand", npc="disabled")
                self.assertEqual(validate(cfg)["git"]["development_branch"], "main")

    def test_mode_a_mirror_rejects_same_dev_and_prod_branch(self):
        self.cfg["git"]["development_branch"] = "main"
        self.cfg["git"]["production_branch"] = "main"
        self.cfg["git"]["github_mirror"] = {
            "enabled": True,
            "direction": "cnb-to-github",
            "branches": ["main"],
            "tags": "approved-releases-only",
        }
        with self.assertRaisesRegex(ProviderError, "distinct development and production"):
            validate(self.cfg)

    def test_cnb_npc_optionality(self):
        for npc in ("disabled", "on-demand-read-only"):
            with self.subTest(npc=npc):
                cfg = copy.deepcopy(self.cfg)
                cfg["review"]["npc"] = npc
                self.assertEqual(validate(cfg)["review"]["npc"], npc)
        for bad_npc in ("work-mode", "auto-write", ""):
            with self.subTest(bad_npc=bad_npc):
                cfg = copy.deepcopy(self.cfg)
                cfg["review"]["npc"] = bad_npc
                with self.assertRaises(ProviderError):
                    validate(cfg)

    def test_cnb_github_composition_mode_a(self):
        self.cfg["git"]["issue_provider"] = "github"
        self.cfg["git"]["github_mirror"] = {
            "enabled": True,
            "direction": "cnb-to-github",
            "branches": ["main"],
            "tags": "approved-releases-only",
        }
        self.assertEqual(validate(self.cfg)["git"]["issue_provider"], "github")

    def test_unified_core_and_conditional_provider_contracts(self):
        root = Path(__file__).resolve().parents[1]
        provider_doc = (root / "docs" / "git-provider.md").read_text(encoding="utf-8")
        cnb_review_doc = (root / "docs" / "cnb-review.md").read_text(encoding="utf-8")
        quality_doc = (root / "QUALITY.md").read_text(encoding="utf-8")
        update_doc = (root / "docs" / "how-to-update.md").read_text(encoding="utf-8")

        for state in ("DETECTED", "CONFIGURED", "UNCONFIGURED", "VERIFIED", "BLOCKED"):
            self.assertIn(state, provider_doc)
        self.assertIn("CNB Primary — Lite", provider_doc)
        self.assertIn("CNB Primary — Strict Opt-in", provider_doc)
        self.assertIn("CNB platform Skills", provider_doc)
        self.assertIn("False-success traps", cnb_review_doc)
        self.assertIn("Explicit strict Git governance", cnb_review_doc)
        self.assertIn("current-sha-review-gate", cnb_review_doc)
        self.assertIn("--review-head", cnb_review_doc)
        self.assertIn("--current-head", cnb_review_doc)
        self.assertIn("discovered and actually executed", quality_doc)
        self.assertIn("material verification limitation", quality_doc)
        self.assertIn("actual previously verified ADS pin", update_doc)
        for skill in ("bootstrap", "adopt", "deliver", "recover"):
            self.assertTrue((root / "skills" / skill / "SKILL.md").is_file(), skill)

    def test_github_compatibility(self):
        self.cfg["git"]["primary"] = "github"
        self.cfg["git"]["github_mirror"] = {"enabled": False, "direction": "disabled", "branches": [], "tags": "disabled"}
        self.cfg["review"].update(auto="host-on-demand", npc="disabled")
        self.assertEqual(validate(self.cfg)["git"]["primary"], "github")

    def test_missing_is_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".ads-project.json"
            self.assertIsNone(load(p))
            self.assertEqual(main(["--path", str(p)]), 2)
            self.assertFalse(p.exists())

    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".ads-project.json"
            p.write_text(json.dumps(self.cfg))
            before = p.read_bytes()
            self.assertEqual(main(["--path", str(p)]), 0)
            self.assertEqual(main(["--path", str(p)]), 0)
            self.assertEqual(p.read_bytes(), before)

    def test_fail_closed(self):
        cases = [
            lambda c: c["git"].update(development_branch=""),
            lambda c: c["git"].update(development_branch="../main"),
            lambda c: c["git"].update(development_branch="dev//bad"),
            lambda c: c["git"].update(development_branch="dev.lock"),
            lambda c: c["git"].update(development_branch="a.lock/b"),
            lambda c: c["git"].update(development_branch="feature/.hidden"),
            lambda c: c["git"].update(production_branch="main/"),
            lambda c: c["git"].update(production_branch="release./v1"),
            lambda c: c["git"]["github_mirror"].update(enabled=1),
            lambda c: c["git"]["github_mirror"].update(branches=["main", "dev"]),
            lambda c: c["git"]["github_mirror"].update(direction="github-to-cnb"),
            lambda c: c["git"]["github_mirror"].update(tags="all"),
            lambda c: c["review"].update(npc="work-mode"),
            lambda c: c["review"].update(max_fix_rounds=True),
            lambda c: c["review"].update(max_fix_rounds=5),
            lambda c: c["release"].update(force_push=True),
            lambda c: c["release"].update(force_push=0),
            lambda c: c["release"].update(approval_required=False),
            lambda c: c["release"].update(approval_required=1),
            lambda c: c.update(gh_token="secret"),
        ]
        for mutate in cases:
            cfg = copy.deepcopy(self.cfg)
            mutate(cfg)
            with self.assertRaises(ProviderError):
                validate(cfg)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".ads-project.json"
            p.write_text("{")
            with self.assertRaises(ProviderError):
                load(p)

if __name__ == "__main__":
    unittest.main()
