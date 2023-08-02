import logging
from pathlib import Path

import command_line_arguments
import log
from folder import Folder, File
from folder_synchronisation import start_synchronisation

if __name__ == '__main__':
    arguments = command_line_arguments.get_arguments()

    log.setup_logging(file_name=arguments.log)
    logger = logging.getLogger(__name__)

    replica_folder = Folder(path=Path(arguments.replica))
    source_folder = Folder(path=Path(arguments.source))

    start_synchronisation(interval=arguments.interval / 1000, source=source_folder, replica=replica_folder)
