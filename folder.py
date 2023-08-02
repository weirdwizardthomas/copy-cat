import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from sortedcontainers import SortedList

logger = logging.getLogger(__name__)


@dataclass
class File:
    path: Path
    parent: 'Folder' = field(init=False)


# todo root folder class?

@dataclass
class Folder:
    path: Path
    parent: Optional['Folder'] = field(init=False)
    # todo use sortedcontainers  https://stackoverflow.com/questions/1109804/does-python-have-a-sorted-list
    files: Optional[SortedList[File]] = None
    subfolders: Optional[SortedList['Folder']] = None

    def __init__(self, path: Path, files: Optional[list[File]] = None, subfolders: Optional[list['Folder']] = None):
        self.path = path
        self.files = SortedList(files or [], key=lambda file: file.path)
        self.subfolders = SortedList(subfolders or [], key=lambda folder: folder.path)

    def __post_init__(self):
        self.path.mkdir(parents=True, exist_ok=True)
        logger.info(f'Created {self.path}.')

    def add_file(self, file: File) -> None:
        file.parent = self
        self.files.add(file)

    def add_subfolder(self, folder: 'Folder') -> None:
        folder.parent = self
        self.subfolders.add(folder)

    def list_tree(self, depth=0) -> str:
        result = '  ' * depth + '* ' + self.path.name + '\n'
        result += ''.join('  ' * (depth + 1) + '- ' + file.path.name + '\n' for file in self.files)
        result += ''.join(folder.list_tree(depth + 1) for folder in self.subfolders)
        return result

