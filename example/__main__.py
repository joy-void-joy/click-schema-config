from typing import Any

import pprint
import click
from click_schema_config import schema_from_inis


@click.command()
@schema_from_inis()
def main(**kwargs: Any):
    pprint.pprint(kwargs)


if __name__ == "__main__":
    main()
