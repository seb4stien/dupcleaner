# stdlib
from functools import lru_cache
import hashlib

# dependencies
from PIL import Image

@lru_cache(maxsize=1024)
def sha1_digest(posix_path: str):
    BLOCKSIZE = 1024 * 1024

    hasher = hashlib.sha1()
    with open(posix_path, mode="rb") as fhn:
        buffer = fhn.read(BLOCKSIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = fhn.read(BLOCKSIZE)
    return hasher.hexdigest()


@lru_cache(maxsize=1024)
def image_sha1_digest(posix_path: str):
    hasher = hashlib.sha1()
    hasher.update(Image.open(posix_path).tobytes())

    return hasher.hexdigest()
