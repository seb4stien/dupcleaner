# stdlib
from pathlib import Path
from typing import Dict, List

# dependencies
from pydantic import BaseModel

# local
from dupcleaner.utils import image_sha1_digest, sha1_digest


class File(BaseModel):
    path: Path
    size: int
    sha1: str = ""


class FileHierarchy(BaseModel):
    files: Dict[str, List[File]] = {}

    def contains(self, path: Path, mode="raw"):
        founds = []
        size = path.stat().st_size
        if path.name in self.files:
            for file in self.files[path.name]:
                if path.as_posix() == file.path.as_posix():
                    raise RuntimeError(f"{path.as_posix()} is both in ref and dup.")

                if mode == "raw":
                    if file.size == size:
                        if file.sha1 == "":
                            file.sha1 = sha1_digest(file.path.as_posix())
                        if file.sha1 == sha1_digest(path.as_posix()):
                            founds.append(file)
                elif mode == "image":
                    if file.sha1 == "":
                        file.sha1 = image_sha1_digest(file.path.as_posix())
                    if file.sha1 == image_sha1_digest(path.as_posix()):
                        founds.append(file)
                else:
                    raise RuntimeError(f"Unsupported mode: {mode}")
        return founds


class FileHierarchyLoader:
    @staticmethod
    def load(path: Path):
        h = FileHierarchy()
        for file_path in path.rglob("*"):
            if not file_path.is_file():
                continue

            stat = file_path.stat()

            new_file = File(path=file_path, size=stat.st_size)

            if file_path.name not in h.files:
                h.files[file_path.name] = [new_file]
            else:
                h.files[file_path.name].append(new_file)
        return h
