# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from base64 import urlsafe_b64encode
from typing import Any
import yaml

from curig.url import YAML_PREFIX


def build_url(data: Any):
    """
    Build a b64-encoded data URL from a data structure.
    """
    prefix = "data:" + YAML_PREFIX
    encoded = urlsafe_b64encode(yaml.dump(data).encode(encoding="utf-8")).decode(encoding="utf-8")
    return prefix + encoded
