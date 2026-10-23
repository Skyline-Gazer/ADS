"""Tests for the consumer remote latest-release probe template."""
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch
import json

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "templates"
    / "consumer-devtools"
    / "check-latest-releases.py"
)
SPEC = spec_from_file_location("consumer_latest_release_check", SCRIPT)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ConsumerLatestReleaseCheckTests(TestCase):
    def test_returns_stable_release_metadata(self):
        payload = json.dumps({
            "tag_name": "v2.3.4",
            "draft": False,
            "prerelease": False,
            "html_url": "https://github.com/example/tool/releases/tag/v2.3.4",
            "published_at": "2026-10-20T10:00:00Z",
        }).encode()
        with patch.object(MODULE.urllib.request, "urlopen", return_value=BytesIO(payload)) as opened:
            result = MODULE.latest_stable("example/tool")
        self.assertEqual(result["version"], "2.3.4")
        self.assertIn("/repos/example/tool/releases/latest", opened.call_args.args[0].full_url)

    def test_refuses_prerelease_metadata(self):
        payload = b'{"tag_name":"v2.3.4-rc.1","draft":false,"prerelease":true}'
        with patch.object(MODULE.urllib.request, "urlopen", return_value=BytesIO(payload)):
            with self.assertRaises(ValueError):
                MODULE.latest_stable("example/tool")


if __name__ == "__main__":
    main()
