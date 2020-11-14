#!/usr/bin/env python3

"""
Remove empty directories
"""

# stdlib
import os
from pathlib import Path

# dependencies
import click


@click.command()
@click.option("-p", "--path", required=True, type=Path, help="Path to clean")
@click.option(
    "-d",
    "--delete",
    multiple=True,
    type=str,
    help="Files that can be deleted if they are alone in a folder.",
)
def cli(path: Path, delete: str):
    for dirpath, dirnames, filenames in os.walk(path.as_posix(), topdown=False):
        if not dirnames:
            if len(filenames) == 1 and filenames[0] in delete:
                to_delete = os.path.join(dirpath, filenames[0])
                click.secho(f"Removing {to_delete}", fg="yellow")
                os.unlink(to_delete)
                filenames.pop()

            if not filenames:
                click.secho(f"Removing {dirpath}")
                os.rmdir(dirpath)


if __name__ == "__main__":
    cli()
