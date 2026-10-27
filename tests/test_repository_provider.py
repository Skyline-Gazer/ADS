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
            lambda c: c["git"].update(development_branch="main"),
            lambda c: c["git"]["github_mirror"].update(branches=["main", "dev"]),
            lambda c: c["git"]["github_mirror"].update(direction="github-to-cnb"),
            lambda c: c["git"]["github_mirror"].update(tags="all"),
            lambda c: c["review"].update(npc="work-mode"),
            lambda c: c["review"].update(max_fix_rounds=True),
            lambda c: c["review"].update(max_fix_rounds=5),
            lambda c: c["release"].update(force_push=True),
            lambda c: c["release"].update(approval_required=False),
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

class ModeBProviderTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((EXAMPLE.parent / 'mode-b.json.example').read_text())
        self.cfg['review']['release_app_id'] = 12345
        self.cfg['review']['ci_app_id'] = 6789

    def test_mode_b_separates_authority(self):
        self.assertEqual(validate(self.cfg)['git']['release_provider'], 'github')

    def test_no_activation_from_unobserved_app_or_reversed_mirror(self):
        mutations = [lambda c: c['review'].update(release_app_id=0),
                     lambda c: c['review'].update(release_app_id=True),
                     lambda c: c['git'].update(release_provider='cnb'),
                     lambda c: c['release'].update(copy_direction='cnb-to-github'),
                     lambda c: c['release'].update(enabled='true'),
                     lambda c: c['git'].update(github_repository='../private'),
                     lambda c: c['git'].update(transfer_prefix='feat/'),
                     lambda c: c['review'].update(max_fix_rounds=4)]
        for change in mutations:
            cfg = copy.deepcopy(self.cfg)
            change(cfg)
            with self.assertRaises(ProviderError):
                validate(cfg)
