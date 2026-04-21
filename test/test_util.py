# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

import yaml
import pytest

from curig.url import ConfigURL, YAML_PREFIX
from curig.util import build_url


@pytest.mark.parametrize(
    "data",
    [
        {"foo": "bar"},
        {"nested": {"a": 1, "b": [1, 2, 3]}},
        ["item1", "item2"],
        "plain string",
        42,
        None,
    ],
)
def test_build_url_roundtrip(data):
    url = build_url(data)
    assert yaml.safe_load(ConfigURL(url).data) == data


def test_build_url_scheme(data={"key": "value"}):
    url = build_url(data)
    assert url.startswith(f"data:{YAML_PREFIX}")


def test_build_url_is_base64(data={"x": 1}):
    url = build_url(data)
    _, encoded = url.split(f"data:{YAML_PREFIX}")
    import base64

    decoded = base64.urlsafe_b64decode(encoded.encode()).decode()
    assert yaml.safe_load(decoded) == data
