# stdlib
from pathlib import Path

# local
from dupcleaner.models import FileHierarchyLoader


def test_dup_found():
    h = FileHierarchyLoader.load(Path("tests/fixtures/ref1"))
    dup = Path("tests/fixtures/dup1/test_1.txt")
    res = h.contains(dup)
    assert len(res) == 1
    assert res[0].path.as_posix() == "tests/fixtures/ref1/test_1.txt"
