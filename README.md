# click-schema-config
click-schema-config allows you to add settings from a config file. Those will be automatically pulled into your program description without having to repeat them. Comments will be used as helper text for click.

# Usage
The folder test right now contains te following example:

Example of a config.default.ini:
```ini
testqwlj =

[test1]
; Wow, multilines
; Talk about eye candy
var1="value1"
var2: int = 2
var3 = True

[test2]
var1 = "value1" # Comment

; This is a comment
123j = None
```
Note that you can type values directly.

```python
import pprint
import click
from click_schema_config import schema_from_inis


@click.command()
@schema_from_inis(filenames=["config.default.ini"])
def main(**kwargs):
    pprint.pprint(kwargs)


if __name__ == "__main__":
    main()
```

This will result in:
```sh
python TODO.py --help

Usage: TODO.py [OPTIONS]

Options:
  --test2.123j TEXT               This is a comment
  --test2.var1 TEXT
  --test1.var3 / --no-test1.var3
  --test1.var2 INTEGER
  --test1.var1 TEXT               Wow, multilines Talk about eye candy
  --testqwlj TEXT
  --help                          Show this message and exit.
```

You can of course override using the options:
```sh
python TODO.py --test2.123j hey

{'test1__var1': 'value1',
 'test1__var2': 2,
 'test1__var3': True,
 'test2__123j': 'hey',
 'test2__var1': 'value1',
 'testqwlj': None}
```
# Rationale
[TODO]

# Install
[TODO once pushed to pypi]

# TODO
[TODO]
