#!/usr/bin/env python3

# stdlib
from pathlib import Path
import time
from typing import List

# dependencies
import click

# local
from dupcleaner.models import FileHierarchyLoader


@click.command()
@click.option("--ref", type=Path, required=True, multiple=True, help="Reference path")
@click.option("--dup", type=Path, required=True, help="Potential duplicates path")
@click.option("-f", "--force", is_flag=True, help="WARNING: auto-delete files")
@click.option("-v", "--verbose", is_flag=True, help="Verbose mode")
@click.option("-m", "--mode", type=click.Choice(["raw", "image"]), default="raw", help="Comparaison mode")
def cli(ref: List[Path], dup: Path, force: bool, verbose: bool, mode: str):
    hierarchies = []

    for _ref in ref:
        t0 = int(time.time())
        click.secho(f"Loading files from {_ref} in memory.")
        hierarchies.append(FileHierarchyLoader.load(_ref))
        click.secho(f"  Done in {int(time.time()) - t0}s")

    for dup_path in dup.rglob("*"):
        if not dup_path.is_file():
            continue

        if verbose:
            click.secho(f"Looking for {dup_path}")

        for ref_hierarchy in hierarchies:
            potential_refs = ref_hierarchy.contains(dup_path, mode=mode)

            if len(potential_refs) > 0:
                click.secho(f"\ndup: {dup_path}")

            idx = 1
            for potential_ref in potential_refs:
                click.secho(f"  ref_{idx}: {potential_ref.path.as_posix()}")
                idx += 1

            if len(potential_refs) > 0:
                if force:
                    confirmation = True
                else:
                    confirmation = click.confirm(
                        f"Do you want to delete {dup_path}", default=False
                    )

                if confirmation:
                    dup_path.unlink()
                    break


if __name__ == "__main__":
    cli()
