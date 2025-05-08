# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Charlie Wheeler-Robinson

from jsonschema import validate, exceptions
from os import environ
import yaml


from .dict import PathableDict
from .url import ConfigURL


class ConfigLoader:
    """Load config"""

    def __init__(self, defaults={}):
        """
        defaults is a dict in the following format
        {
            'ENV_VAR': {
                'schema': 'URL for a schema which will be used to validate the config conforms',
                'default': 'a default URL for when the env var is unset'
            }
        }
        """
        self._defaults = defaults

    def load(self, env_var=None, fobj=None, schema=None):
        if env_var is not None:
            config = self.from_env(env_var, schema)
        else:
            config = ConfigLoader.from_file(fobj, schema)
        return PathableDict(config)

    def from_env(self, env_var, schema=None):
        default = self._default(env_var)
        url = ConfigURL(environ.get(env_var, default))
        config = dict(yaml.safe_load(url.data))
        schema = schema or self._schema(env_var)
        if schema is not None:
            try:
                validate(config, yaml.safe_load(ConfigURL(schema).data))
            except exceptions.SchemaError as exc:
                raise exc
            except exceptions.ValidationError as exc:
                raise exc
        return config

    @staticmethod
    def from_file(fobj, schema=None):
        data = fobj.read()
        config = dict(yaml.safe_load(data))
        if schema is not None:
            try:
                validate(config, yaml.safe_load(ConfigURL(schema).data))
            except exceptions.SchemaError as exc:
                raise exc
            except exceptions.ValidationError as exc:
                raise exc
        return config

    def _default_get(self, env_var, value):
        """get default for env var for value"""
        return self._defaults.get(env_var, {}).get(value, None)

    def _default(self, env_var):
        return self._default_get(env_var, "default")

    def _schema(self, env_var):
        return self._default_get(env_var, "schema")
