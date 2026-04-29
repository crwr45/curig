# Curig

## Usage

### Python

As a library, it can be configured with defaults and schema validation for loading config from environment variables:

```python
from curig.config import ConfigLoader
from curig.util import build_url

default = build_url(
    {
        "db": {
            "username": "postgres",
            "password": "postgres",
            "hostname": "localhost",
            "port": 5432,
            "database": "mlib",
        }
    }
)

DEFAULTS = {
    "EXAMPLE_CONFIG": {"default": default},
    'CONFIG_VAR_NAME': {
        'default': 'data:application/json;base64,eyJoZWxsbyI6ICJ3b3JsZCJ9',
        'schema': 'file:///config/schema/config.json'
    },
    'ANOTHER_ENV_VAR': {
        'default': file:///config/defaults/config.yaml
    }
}

CONFIG = cfg.load(env_var="EXAMPLE_CONFIG")
```

### CLI
As a command line tool it can load individual config files, and extract particular values from within nested config:

```shell
python3 -m curig.load -i -p '$.document.url' example_configs/conf.yml
```
