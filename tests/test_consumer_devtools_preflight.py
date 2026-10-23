"""Tests for the consumer latest-stable tool preflight template."""
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import Mock, patch
import contextlib
import io
import subprocess

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "templates"
    / "consumer-devtools"
    / "check-consumer-devtools.py"
)
SPEC = spec_from_file_location("consumer_devtools_check", SCRIPT)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ConsumerDevtoolsPreflightTests(TestCase):
    def test_latest_stable_reads_github_release_metadata(self):
        payload = b'{"tag_name":"v1.2.3","draft":false,"prerelease":false,"html_url":"https://github.com/example/tool/releases/tag/v1.2.3"}'
        response = BytesIO(payload)
        with patch.object(MODULE.urllib.request, "urlopen", return_value=response) as opened:
            version, url = MODULE.latest_stable("example/tool")
        self.assertEqual(version, "1.2.3")
        self.assertIn("releases/tag/v1.2.3", url)
        self.assertIn("/repos/example/tool/releases/latest", opened.call_args.args[0].full_url)

    def test_latest_stable_rejects_prerelease(self):
        response = BytesIO(b'{"tag_name":"v2.0.0-rc.1","draft":false,"prerelease":true}')
        with patch.object(MODULE.urllib.request, "urlopen", return_value=response):
            with self.assertRaises(ValueError):
                MODULE.latest_stable("example/tool")

    def test_full_rtk_rejects_rtk_oss_binary(self):
        with patch.object(MODULE.shutil, "which", return_value="/tmp/rtk-oss"):
            with self.assertRaisesRegex(ValueError, "full RTK is required"):
                MODULE.installed_version("rtk")

    def test_missing_tools_report_latest_version_and_request_consent(self):
        git_branch = subprocess.CompletedProcess([], 0, stdout="feat/task\n", stderr="")
        with (
            patch.object(MODULE.subprocess, "run", return_value=git_branch),
            patch.object(MODULE, "latest_stable", side_effect=[
                ("1.2.3", "https://example/codegraph/releases/latest"),
                ("4.5.6", "https://example/rtk/releases/latest"),
            ]),
            patch.object(MODULE.shutil, "which", return_value=None),
        ):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = MODULE.main()
        self.assertEqual(result, 1)
        self.assertIn("latest stable=1.2.3", output.getvalue())
        self.assertIn("latest stable=4.5.6", output.getvalue())
        self.assertEqual(output.getvalue().count("Ask the user before installing."), 2)

    def test_production_checkout_is_blocked_before_version_checks(self):
        branch = subprocess.CompletedProcess([], 0, stdout="main\n", stderr="")
        with patch.object(MODULE.subprocess, "run", return_value=branch), patch.object(
            MODULE, "latest_stable"
        ) as latest:
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                result = MODULE.main()
        self.assertEqual(result, 2)
        self.assertIn("development branch", error.getvalue())
        latest.assert_not_called()


if __name__ == "__main__":
    main()
