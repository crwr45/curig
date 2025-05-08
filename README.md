Dependencies:

```
python-jsonpath
jsonschema
PyYAML
```

## Usage
As a command line tool it can load individual config files, and extract particular values from within nested config:

```
python3 -m curig.load -i -p '$.document.url' example_configs/conf.yml
```

As a library, it can be configured with defaults and schema validation for loading config from environment variables:

```
from curig.config import ConfigLoader

defaults = {
    'CONFIG_VAR_NAME': {
        'default': 'data:application/json;base64,eyJoZWxsbyI6ICJ3b3JsZCJ9',
        'schema': 'file:///config/schema/config.json'
    },
    'ANOTHER_ENV_VAR': {
        'default': file:///config/defaults/config.yaml
    }
}
cfg = ConfigLoader(defaults)
config = cfg.load('CONFIG_VAR_NAME')
```

## Recipes

b64 encoded config can be generated using:

```
from base64 import urlsafe_b64encode
import json

data = <CONFIG>

encoded = urlsafe_b64encode(json.dumps(data).encode(encoding='utf-8')).decode(encoding='utf-8')
url = 'data:application/json;base64,' + encoded
```
