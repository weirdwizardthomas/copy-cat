import logging
import sched
import time

from folder import Folder, File

logger = logging.getLogger(__name__)



def synchronize_replica(source: Folder, replica: Folder) -> None:
    logger.debug(f'{source.path} --> {replica.path}')


def start_synchronisation(interval: float, source: Folder, replica: Folder) -> None:
    scheduler = sched.scheduler(time.time, time.sleep)

    def periodic_function() -> None:
        synchronize_replica(source=source, replica=replica)
        scheduler.enter(interval, 1, periodic_function)

    periodic_function()
    scheduler.run()
