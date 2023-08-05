import logging
from pathlib import Path

from copy_cat import command_line_arguments
from copy_cat.folder import Folder, File
from copy_cat.folder_synchronisation import start_synchronisation
from copy_cat.configuration import setup_logging

if __name__ == '__main__':
    arguments = command_line_arguments.get_arguments()

    setup_logging(file_name=arguments.log)
    logger = logging.getLogger(__name__)

    replica_root = Path(arguments.replica)

    source_folder = Folder(path=Path(arguments.source), is_root=True)

    source_folder.add_file(File(Path('file1')))
    source_folder.add_subfolder(Folder(Path('government secrets')))

    source_folder.subfolders[0].add_subfolder(Folder(Path('nuke codes')))
    source_folder.subfolders[0].subfolders[0].add_file(File(Path('head1.key')))

    start_synchronisation(interval=arguments.interval / 1000, source=source_folder, replica_root=replica_root)
