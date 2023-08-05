import logging
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Self

from sortedcontainers import SortedList

from copy_cat.file import File, checksum
from copy_cat.util import quote_path

logger = logging.getLogger(__name__)


@dataclass
class Folder:
    path: Path

    files: Optional[SortedList[File]] = None
    subfolders: Optional[SortedList[Self]] = None

    def __init__(self, path: Path, is_root: bool = False):
        self.path = path

        if is_root:
            self.create()

        self.subfolders = SortedList([], key=lambda folder: folder.path)
        self.files = SortedList([], key=lambda file: file.path)

    def create(self):
        if not self.path.exists():
            logger.info(f'Created folder {quote_path(self.path)}')

        self.path.mkdir(parents=True, exist_ok=True)

    def add_file(self, file: File) -> None:
        file.path = self.path / file.path
        file.create()
        self.files.add(file)

    def add_subfolder(self, folder: Self) -> None:
        folder.path = self.path / folder.path
        folder.create()
        self.subfolders.add(folder)

    def list_tree(self, depth: int = 0) -> str:
        result = '  ' * depth + '* ' + self.path.name + '\n'
        result += ''.join('  ' * (depth + 1) + '- ' + file.path.name + '\n' for file in self.files)
        result += ''.join(folder.list_tree(depth + 1) for folder in self.subfolders)
        return result

    # todo sync with filesystem ?
    def synchronize(self, replica_root: Path) -> None:
        for index, file in enumerate(self.files):
            replica = Folder._get_replica_path(replica_root=replica_root, source=file.path)
            replica_checksum = checksum(replica)
            if not file.checksum and replica_checksum:
                self._remove_file(file, index, replica)
                continue

            if file.checksum == replica_checksum:
                logger.info(f'{quote_path(file.path)} matches {quote_path(replica)}. Skipping.')
                continue

            Folder._copy_file(source=file.path, replica=replica)

        for folder in self.subfolders:
            folder.synchronize(replica_root=replica_root)

    def _remove_file(self, file: File, index: int, replica: Path) -> None:
        logger.info(f'File {quote_path(file.path)} deleted. Deleting {quote_path(replica)}')
        os.remove(replica)
        self.files.pop(index)

    @staticmethod
    def _get_replica_path(replica_root: Path, source: Path) -> Path:
        return replica_root.joinpath(*source.parts[1:])

    @staticmethod
    def _copy_file(source: Path, replica: Path) -> None:
        logger.info(f'Copying {quote_path(source)} to {quote_path(replica)}.')
        replica.parent.mkdir(parents=True, exist_ok=True)  # might be faster to check if it exists?
        shutil.copyfile(source, replica)
