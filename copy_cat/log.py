import logging
from pathlib import Path

from copy_cat.configuration import LOGGING_MESSAGE_FORMAT, LOGGING_DATE_FORMAT


def setup_logging(file_name: Path) -> None:
    logging.basicConfig(filename=file_name,
                        filemode='a',
                        format=LOGGING_MESSAGE_FORMAT,
                        datefmt=LOGGING_DATE_FORMAT,
                        level=logging.DEBUG)
