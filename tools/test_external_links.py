import io
from unittest.mock import patch
import urllib.error

import pytest

from tools.check_external_links import check_url, collect_urls


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_collects_unique_links_and_excludes_templates_and_hidden_files(tmp_path):
    (tmp_path / "README.md").write_text("[a](https://example.com/a) [b](https://example.com/a)")
    (tmp_path / "docs" / "TEMPLATE").mkdir(parents=True)
    (tmp_path / "docs" / "TEMPLATE" / "README.md").write_text("[placeholder](https://invalid.test/)")
    (tmp_path / ".cache").mkdir()
    (tmp_path / ".cache" / "README.md").write_text("[cache](https://cache.test/)")
    assert collect_urls(tmp_path) == ["https://example.com/a"]


@pytest.mark.parametrize("status,outcome", [(404, "broken"), (410, "broken"), (403, "unverified"),
                                           (429, "unverified"), (503, "unverified")])
def test_access_limit_and_server_failure_are_not_reported_as_deleted(status, outcome):
    error = urllib.error.HTTPError("https://example.com/", status, "test", {}, io.BytesIO())
    with patch("urllib.request.urlopen", side_effect=error):
        result = check_url("https://example.com/")
    assert (result.outcome, result.status) == (outcome, status)


def test_head_not_supported_falls_back_to_get():
    error = urllib.error.HTTPError("https://example.com/", 405, "test", {}, io.BytesIO())
    with patch("urllib.request.urlopen", side_effect=[error, Response()]) as request:
        assert check_url("https://example.com/").outcome == "ok"
    assert [call.args[0].method for call in request.call_args_list] == ["HEAD", "GET"]


def test_proxy_denial_is_unverified():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Tunnel connection failed: 403 Forbidden")):
        assert check_url("https://example.com/").outcome == "unverified"


def test_credentials_in_url_are_rejected_without_a_request():
    with patch("urllib.request.urlopen") as request:
        assert check_url("https://user:password@example.com/").outcome == "broken"
        request.assert_not_called()


def test_malformed_url_is_reported_without_crashing():
    with patch("urllib.request.urlopen") as request:
        assert check_url("https://[invalid/").outcome == "broken"
        request.assert_not_called()
