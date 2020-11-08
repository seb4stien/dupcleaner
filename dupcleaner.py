#!/usr/bin/env python3

# stdlib
from pathlib import Path
import time

# dependencies
import click

# local
from dupcleaner.models import FileHierarchyLoader


@click.command()
@click.option("--ref", type=Path, required=True, help="Reference path")
@click.option("--dup", type=Path, required=True, help="Potential duplicates path")
@click.option("--force", is_flag=True, help="WARNING: auto-delete files")
def cli(ref: Path, dup: Path, force: bool):
    t0 = int(time.time())
    click.secho(f"Loading files from {ref} in memory.")
    ref_hierarchy = FileHierarchyLoader.load(ref)
    click.secho(f"  Done in {int(time.time()) - t0}s")

    for dup_path in dup.rglob("*"):
        if not dup_path.is_file():
            continue

        potential_refs = ref_hierarchy.contains(dup_path)

        if len(potential_refs) > 0:
            click.secho(
                f"\n{dup_path} seems to be a duplicate (same name, size and sha1) of:"
            )

        idx = 1
        for potential_ref in potential_refs:
            click.secho(f"  {idx}: {potential_ref}")
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


if __name__ == "__main__":
    cli()
