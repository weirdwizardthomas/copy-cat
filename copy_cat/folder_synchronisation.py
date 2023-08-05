import logging
import sched
import time
from pathlib import Path

from copy_cat.folder import Folder
from copy_cat.util import quote_path

logger = logging.getLogger(__name__)


def start_synchronisation(interval: float, source: Folder, replica_root: Path) -> None:
    logger.info(f'Starting synchronisation of folder {quote_path(source.path)} to folder {quote_path(replica_root)}.')
    logger.info(f'Synchronisation interval: {interval} [s].')

    scheduler = sched.scheduler(time.time, time.sleep)

    def periodic_function() -> None:
        source.synchronize(replica_root=replica_root)
        scheduler.enter(interval, 1, periodic_function)

    periodic_function()
    scheduler.run()
