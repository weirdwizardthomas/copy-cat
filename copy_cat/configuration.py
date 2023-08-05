# todo use yaml?
import logging
from pathlib import Path

LOGGING_DATE_FORMAT = '%H:%M:%S'
LOGGING_MESSAGE_FORMAT = '[%(asctime)s,%(msecs)d] [%(levelname)s] %(name)s: %(message)s'


def setup_logging(file_name: Path) -> None:
    logging.basicConfig(filename=file_name,
                        filemode='a',
                        format=LOGGING_MESSAGE_FORMAT,
                        datefmt=LOGGING_DATE_FORMAT,
                        level=logging.DEBUG)
