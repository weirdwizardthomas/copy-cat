from pathlib import Path

from copy_cat import command_line_arguments
from copy_cat.configuration import setup_logging
from copy_cat.folder import Folder
from copy_cat.folder_synchronisation import start_synchronisation

if __name__ == '__main__':
    arguments = command_line_arguments.get_arguments()

    setup_logging(file_name=arguments.log)

    replica_root = Path(arguments.replica)
    source_folder = Folder(path=Path(arguments.source), is_root=True)

    start_synchronisation(interval=arguments.interval / 1000, source=source_folder, replica_root=replica_root)
