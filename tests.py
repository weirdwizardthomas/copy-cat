import os
import shutil
from pathlib import Path

from copy_cat.file import File
from copy_cat.folder import Folder

_source_path = Path('source')
_replica_path = Path('replica')


def _safe_delete(path: Path) -> None:
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path=path)
    else:
        os.remove(path=path)

    assert not path.exists()


def _files_content_match(file_1: Path, file_2: Path) -> bool:
    with file_1.open('r') as file_1, file_2.open('r') as file_2:
        return file_1.read() == file_2.read()


def test_changes_write_to_filesystem():
    try:
        source_folder = Folder(path=_source_path, is_root=True)
        assert source_folder.path.exists()
    finally:
        _safe_delete(_source_path)


def test_folder_synchronisation():
    try:
        source_folder = Folder(path=_source_path, is_root=True)
        source_folder.synchronize(replica_root=_replica_path)
        assert _replica_path.exists()
    finally:
        _safe_delete(_source_path)
        _safe_delete(_replica_path)


def test_file_creation():
    try:
        source_folder = Folder(path=_source_path, is_root=True)
        file = File(path=Path('file_1'))
        source_folder.add_file(file)

        assert file.path.exists()

        source_folder.synchronize(replica_root=_replica_path)

        assert file.path.exists()

        replica_file = Folder._get_replica_path(replica_root=_replica_path, source=file.path)
        assert replica_file.exists()

    finally:
        _safe_delete(_source_path)
        _safe_delete(_replica_path)


def test_file_modification():
    try:
        file = File(path=Path('file_1'))

        source_folder = Folder(path=_source_path, is_root=True)
        source_folder.add_file(file)

        with file.path.open('w') as f:
            f.write('hello')

        source_folder.synchronize(replica_root=_replica_path)

        replica_path = Folder._get_replica_path(replica_root=_replica_path, source=file.path)

        assert _files_content_match(file_1=file.path, file_2=replica_path)

        with file.path.open('w+') as f:
            f.write('there')

        assert not _files_content_match(file_1=file.path, file_2=replica_path)

        source_folder.synchronize(replica_root=_replica_path)

        assert _files_content_match(file_1=file.path, file_2=replica_path)

    finally:
        _safe_delete(_source_path)
        _safe_delete(_replica_path)


def test_file_deletion():
    try:
        source_folder = Folder(path=_source_path, is_root=True)
        file = File(path=Path('file_1'))
        source_folder.add_file(file)

        assert file.path.exists()

        source_folder.synchronize(replica_root=_replica_path)

        assert file.path.exists()

        replica_file = Folder._get_replica_path(replica_root=_replica_path, source=file.path)

        os.remove(file.path)
        assert not file.path.exists()

        source_folder.synchronize(replica_root=_replica_path)
        assert not replica_file.exists()

    finally:
        _safe_delete(_source_path)
        _safe_delete(_replica_path)


def test_nested_folder():
    try:
        source_folder = Folder(path=_source_path, is_root=True)
        nested_folder = Folder(path=Path('nested'))
        file = File(path=Path('file_1'))

        source_folder.add_subfolder(folder=nested_folder)
        source_folder.subfolders[0].add_file(file=file)

        assert file.path.exists()

        source_folder.synchronize(replica_root=_replica_path)

        replica_file = Folder._get_replica_path(replica_root=_replica_path, source=file.path)

        assert replica_file.exists()
    finally:
        _safe_delete(_source_path)
        _safe_delete(_replica_path)
