import click
from .config import read_config


def schema_from_inis(filenames=["config.default.ini", "config.ini"]):
    """Decorate a click command to load options from a config file."""

    if isinstance(filenames, str):
        filenames = [filenames]

    config = read_config(filenames)

    def decorator(func):
        for section, options in config.items():
            for variable_name, d in options.items():
                option_name = (
                    f"{f'{section}.' if section != 'DEFAULT' else ''}{variable_name}"
                )

                bool_option_name = None
                if d["type"] == "bool":
                    no_option_name = f"no-{option_name}"
                    if d["value"]:
                        bool_option_name = {"yes": option_name, "no": no_option_name}
                    else:
                        bool_option_name = {"yes": no_option_name, "no": option_name}

                func = click.option(
                    f"--{option_name}"
                    if bool_option_name is None
                    else f"--{bool_option_name['yes']}/--{bool_option_name['no']}",
                    option_name.replace(".", "__"),
                    type=__builtins__[d["type"]] if d["type"] != "NoneType" else None,
                    default=d["value"],
                    help=f"\n{d['description'] or ''}".replace("\n", "\b\n"),
                )(func)

        return func

    return decorator
