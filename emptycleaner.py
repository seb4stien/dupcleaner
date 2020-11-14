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
def cli(path: Path):
    for dirpath, dirnames, filenames in os.walk(path.as_posix(), topdown=False):
        if not dirnames and not filenames:
            click.secho(f"Removing {dirpath}")
            os.rmdir(dirpath)


if __name__ == "__main__":
    cli()
