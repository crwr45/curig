# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from base64 import urlsafe_b64encode
import json
from unittest.mock import patch, mock_open

import pytest

from curig.config import ConfigLoader

data = {"foo": "bar"}
mime_data = {"mimes": ["application/json", "text/plain"]}


class CaseData:
    def __init__(self, env_var, data):
        self.env_var_base = env_var
        self.data = data
        self._text_data = json.dumps(data)
        self.b64 = urlsafe_b64encode(self._text_data.encode(encoding="utf-8")).decode(
            encoding="utf-8"
        )

    @property
    def data_env_var(self):
        return f"{self.env_var_base}_DATA"

    @property
    def file_env_var(self):
        return f"{self.env_var_base}_FILE"

    @property
    def data_url(self):
        return f"data:application/json;base64,{self.b64}"

    @property
    def file_url(self):
        return "file:///config.json"


CASES = [CaseData(e, d) for e, d in (("SIMPLE", data), ("COMPLEX", mime_data))]
CASE_BY_ENV_VAR = {c.file_env_var: c for c in CASES} | {c.data_env_var: c for c in CASES}

MOCK_ENV = {c.file_env_var: c.file_url for c in CASES} | {c.data_env_var: c.data_url for c in CASES}


class TestConfig:
    @pytest.mark.parametrize("env_var", CASE_BY_ENV_VAR.keys())
    def test_config(self, env_var):
        case = CASE_BY_ENV_VAR[env_var]
        cfg = ConfigLoader()
        with (
            patch("builtins.open", mock_open(read_data=case._text_data)) as mock_file,
            patch.dict("os.environ", MOCK_ENV, clear=True),
        ):
            c = cfg.from_env(env_var)
            assert c == case.data
            if "_FILE" in env_var:
                mock_file.assert_called_once_with("/config.json", encoding="utf-8")

    @pytest.mark.parametrize("env_var", CASE_BY_ENV_VAR.keys())
    def test_config_default(self, env_var):
        defaults = {c.file_env_var: {"default": c.file_url} for c in CASES}
        defaults |= {c.data_env_var: {"default": c.data_url} for c in CASES}
        cfg = ConfigLoader(defaults=defaults)
        case = CASE_BY_ENV_VAR[env_var]
        with (
            patch("builtins.open", mock_open(read_data=case._text_data)) as mock_file,
            patch.dict("os.environ", {}, clear=True),
        ):
            c = cfg.from_env(env_var)
            assert c == case.data
            if "_FILE" in env_var:
                mock_file.assert_called_once_with("/config.json", encoding="utf-8")

    @pytest.mark.skip
    def test_config_schema(self):
        assert True
