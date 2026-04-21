# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from base64 import urlsafe_b64encode
import json
from unittest.mock import patch, mock_open

import pytest

from curig.url import ConfigURL, JSON_PREFIX

data = {"foo": "bar"}
mime_data = {"mimes": ["application/json", "text/plain"]}
url = f"data:{JSON_PREFIX},{urlsafe_b64encode(json.dumps(data).encode(encoding='utf-8')).decode(encoding='utf-8')}"


class CaseData:
    def __init__(self, scheme, data, fname=None):
        self.scheme = scheme
        self.data = json.dumps(data)
        self.fname = fname
        if scheme == "file":
            self.url = f"file://{fname}"
        elif scheme == "data":
            self.url = f"data:{JSON_PREFIX},{urlsafe_b64encode(self.data.encode(encoding='utf-8')).decode(encoding='utf-8')}"


CASES = [
    CaseData(s, d, f)
    for s, d, f in [
        ("data", data, None),
        ("file", data, "/config/example_configs/conf.json"),
        ("data", mime_data, None),
        ("file", mime_data, "/conf.json"),
    ]
]


class TestURL:
    @pytest.mark.parametrize("case", CASES)
    def test_url(self, case: CaseData):
        with patch("builtins.open", mock_open(read_data=case.data)) as mock_file:
            c = ConfigURL(case.url)
            assert c._file_content is None
            assert c.data == case.data
            if case.scheme == "file":
                mock_file.assert_called_once_with(case.fname, encoding="utf-8")
                assert c._file_content == case.data

    @pytest.mark.parametrize(
        "url, err",
        [
            (url.replace("data:", "data:error"), ValueError),
            (url.replace("data:", "data2:"), ValueError),
            (url.replace("data:", "file:"), FileNotFoundError),
            ("file://conf.json", ValueError),
            ("https://www.google.com", ValueError),
        ],
    )
    def test_url_errors(self, url, err):
        with pytest.raises(err):
            c = ConfigURL(url)
            c.data
