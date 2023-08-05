import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from copy_cat.const import CHUNK_SIZE
from copy_cat.util import quote_path

logger = logging.getLogger(__name__)


def checksum(path: Path) -> Optional[str]:
    if not path.exists():
        # strong assumption that source would always exist - otherwise two missing files will have the same checksum
        return None
    md5_hash = hashlib.md5()

    with open(path, 'rb') as file:
        # Read the file in chunks to efficiently handle large files
        while chunk := file.read(CHUNK_SIZE):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


@dataclass
class File:
    path: Path

    def create(self):
        self.path.touch(exist_ok=True)
        logger.info(f'Created file {quote_path(self.path)}')

    @property
    def checksum(self) -> str:
        return checksum(self.path)
