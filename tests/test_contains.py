# stdlib
from pathlib import Path

# dependencies
import pytest

# local
from dupcleaner.models import FileHierarchyLoader


def test_dup_found():
    ref = FileHierarchyLoader.load(Path("tests/fixtures/ref1"))
    dup = Path("tests/fixtures/dup1/test_1.txt")

    assert len(ref.contains(dup)) == 1


def test_nodup_notfound():
    ref = FileHierarchyLoader.load(Path("tests/fixtures/ref1"))
    dup = Path("tests/fixtures/unknown.txt")

    assert len(ref.contains(dup)) == 0


def test_dup_is_ref():
    ref = FileHierarchyLoader.load(Path("tests/fixtures/ref1"))
    dup = Path("tests/fixtures/ref1/test_1.txt")

    with pytest.raises(RuntimeError):
        ref.contains(dup)
