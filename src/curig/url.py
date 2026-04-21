# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from base64 import urlsafe_b64decode
from typing import Tuple
from urllib.parse import urlparse, unquote

JSON_PREFIX = "application/json;base64"
YAML_PREFIX = "application/yaml;base64"

SUPPORTED_PREFIXES = [JSON_PREFIX, YAML_PREFIX]


class ConfigURL:
    """Parse a config URL and get the data it points to.

    If url has scheme file then get the data from the file."""

    def __init__(self, url: str):
        self._url = url
        self._scheme, self._content = ConfigURL._url_extract(url)
        self._file_content = None

    @property
    def data(self):
        """Access and return the data from the URL
        A file URL will be read at this time if it has not been accessed before.
        """
        if self._scheme == "file":
            if self._file_content is None:
                with open(self._content, encoding="utf-8") as fid:
                    text = fid.read()
                self._file_content = text
            return self._file_content
        return self._content

    @classmethod
    def _url_extract(cls, url: str) -> Tuple[str, str]:
        """
        Parse a URL of allowed types and return the contents.
        A supported base64-encoded data URL will be decoded.
        """
        match urlparse(url):
            case ("file", "", path, "", "", ""):
                return "file", unquote(path)
            case ("data", "", path, "", "", ""):
                for supported in SUPPORTED_PREFIXES:
                    if supported in path:
                        prefix, data = path.split(supported)
                        break
                else:
                    raise ValueError(f"unsupported prefix")

                if prefix == "":
                    return "data", urlsafe_b64decode(data.encode(encoding="utf-8")).decode(
                        encoding="utf-8"
                    )
                else:
                    raise ValueError(f"unsupported prefix on data URL: {prefix}")
            case _:
                raise ValueError(f"unsupported URL")
