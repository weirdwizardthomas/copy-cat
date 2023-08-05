# todo use yaml?
import logging
from pathlib import Path

LOGGING_DATE_FORMAT = '%H:%M:%S'
LOGGING_MESSAGE_FORMAT = '[%(asctime)s,%(msecs)d] [%(levelname)s] %(name)s: %(message)s'
LOGGING_LEVEL = logging.DEBUG


def setup_logging(file_name: Path) -> None:
    logging.basicConfig(filename=file_name,
                        filemode='a',
                        format=LOGGING_MESSAGE_FORMAT,
                        datefmt=LOGGING_DATE_FORMAT,
                        level=LOGGING_LEVEL)

    logger = logging.getLogger()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_LEVEL)
    console_handler.setFormatter(logging.Formatter(fmt=LOGGING_MESSAGE_FORMAT, datefmt=LOGGING_DATE_FORMAT))

    # Add the console handler to the logger
    logger.addHandler(console_handler)
