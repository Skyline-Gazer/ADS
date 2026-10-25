"""Source fallback requires true official absence + immutable owner-approved pin."""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from urllib.error import HTTPError

P=Path(__file__).resolve().parents[1]/"templates/consumer-devtools/check-codegraph-channel.py"
S=spec_from_file_location("codegraph_channel",P)
M=module_from_spec(S)
S.loader.exec_module(M)
SHA="b"*40
def missing():
    raise HTTPError(M.NPM,404,"Not Found",None,None)

class SourceFallbackTests(TestCase):
    def test_stable_preferred(self):
        with patch.object(M,"request_json",return_value={"version":"2.1.0"}) as req:
            o=M.observe_channel()
        self.assertEqual(o["channel"],"STABLE")
        self.assertTrue(o["stable_verified"])
        self.assertEqual(req.call_count,1)

    def test_404_only_plus_official_source_pin(self):
        with patch.object(M,"request_json",side_effect=[HTTPError(M.NPM,404,"missing",None,None),
              [],{"object":{"sha":SHA}},{"name":"@andysom25/codegraph","license":"MIT","version":"1.1.1"}]):
            result=M.observe_channel()
        self.assertEqual(result["channel"],"SOURCE_FALLBACK")
        self.assertFalse(result["stable_verified"])
        self.assertTrue(M.evaluate_source_pin(result,SHA)[0])
        self.assertFalse(M.evaluate_source_pin(result,"a"*40)[0])

    def test_no_fallback_on_network_or_http_500(self):
        with patch.object(M,"request_json",side_effect=HTTPError(M.NPM,500,"failure",None,None)):
            with self.assertRaises(ValueError):M.observe_channel()

    def test_no_fallback_when_releases_exist(self):
        with patch.object(M,"request_json",side_effect=[HTTPError(M.NPM,404,"missing",None,None),[{"tag_name":"v1.0.0"}]]):
            with self.assertRaises(ValueError):M.observe_channel()

    def test_unsafe_package_or_sha_rejected(self):
        for val in [{"object":{"sha":"notsha"}},{"object":{"sha":"a"*40}}]:
            with patch.object(M,"request_json",side_effect=[HTTPError(M.NPM,404,"missing",None,None),[],val,
                 {"name":"evil","version":"1.1.1","license":"MIT"}]):
                with self.assertRaises(ValueError):M.observe_channel()
