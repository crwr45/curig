# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from typing import Any

import jsonpath


class PathableDict(dict):
    """Subclass of dict that provides some json path functionality
    for addressing values in nested objects.

    All keys must be strings.

    A key starting with a '$.' will be treated as a path.
    This means that a path must begin from the object root.

    Path syntax from https://jg-rp.github.io/python-jsonpath/syntax/
    Only absolute paths are tested, use other features of jsonpath at your own risk.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> Any:
        if key[0:2] == "$.":
            return self._get_path_(key)
        return super().__getitem__(key)

    def _get_path_(self, path: str) -> Any:
        match = jsonpath.match(path, self)
        if match is not None:
            return match.value
        raise KeyError(f"no match found for path {path}")

    def get_path(self, path: str, default: Any = None) -> Any:
        """Get the value at `path`.
        If any step of the path does not exist then return `default` instead."""
        try:
            return self._get_path_(path)
        except KeyError:
            return default
