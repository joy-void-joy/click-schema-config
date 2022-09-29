import pprint
import click
from click_schema_config import schema_from_inis


@click.command()
@schema_from_inis(filenames=["config.default.ini"])
def main(**kwargs):
    pprint.pprint(kwargs)


if __name__ == "__main__":
    main()
