# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

import pytest

from jsonpath import (
    JSONPathSyntaxError,
)

from curig.dict import PathableDict

d = {
    "foo": "bar",
    "list": [0, 1, 2, "three"],
    "dict": {
        "a": 1,
        "b": 2,
        "c": 3,
        "nested_list": [0, 1, 2, "three"],
        "nested_dict": {
            "a": 1,
            "b": 2,
            "c": 3,
        },
    },
    "one hundred": "100",
    "100": "one hundred",
}


class TestDict:
    @pytest.mark.parametrize("key", d.keys())
    def test_works_enough_like_dict(self, key):
        pd = PathableDict(d)
        assert pd[key] == d[key]

    @pytest.mark.parametrize(
        "path, val",
        [
            ("$", d),
            ("$.foo", d["foo"]),
            ("$.list", d["list"]),
            ("$.list[1]", d["list"][1]),
            ("$.list[3]", d["list"][3]),
            ("$.dict", d["dict"]),
            ("$.dict.a", d["dict"]["a"]),
            ("$.dict.nested_list", d["dict"]["nested_list"]),
            ("$.dict.nested_list[0]", d["dict"]["nested_list"][0]),
            ("$.dict.nested_dict.a", d["dict"]["nested_dict"]["a"]),
            ('$["one hundred"]', d["one hundred"]),
            ('$["100"]', d["100"]),
            ('$["1000"]', None),
            ("$.missing", None),
        ],
    )
    def test_get_path(self, path, val):
        pd = PathableDict(d)
        assert pd.get_path(path) == val

    @pytest.mark.parametrize(
        "path, err",
        [
            ("$.100", JSONPathSyntaxError),
            ("$.1000", JSONPathSyntaxError),
            (1, TypeError),
        ],
    )
    def test_get_path_errors(self, path, err):
        pd = PathableDict(d)
        with pytest.raises(err):
            pd.get_path(path)

    @pytest.mark.parametrize(
        "path, val",
        [
            ("$.foo", d["foo"]),
            ("$.list", d["list"]),
            ("$.list[1]", d["list"][1]),
            ("$.list[3]", d["list"][3]),
            ("$.dict", d["dict"]),
            ("$.dict.a", d["dict"]["a"]),
            ("$.dict.nested_list", d["dict"]["nested_list"]),
            ("$.dict.nested_list[0]", d["dict"]["nested_list"][0]),
            ("$.dict.nested_dict.a", d["dict"]["nested_dict"]["a"]),
        ],
    )
    def test_path(self, path, val):
        pd = PathableDict(d)
        assert pd[path] == val

    @pytest.mark.parametrize(
        "path, err",
        [
            ("$.100", JSONPathSyntaxError),
            ("$.1000", JSONPathSyntaxError),
            ("$.missing", KeyError),
            ("missing", KeyError),
            (1, TypeError),
        ],
    )
    def test_path_errors(self, path, err):
        pd = PathableDict(d)
        with pytest.raises(err):
            pd[path]
