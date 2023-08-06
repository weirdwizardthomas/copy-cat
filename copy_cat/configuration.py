import logging
from pathlib import Path

LOGGING_DATE_FORMAT = '%H:%M:%S'
LOGGING_MESSAGE_FORMAT = '[%(asctime)s,%(msecs)d] [%(levelname)s] %(name)s: %(message)s'
LOGGING_LEVEL = logging.DEBUG


def setup_logging(file_name: Path) -> None:
    logging.basicConfig(format=LOGGING_MESSAGE_FORMAT,
                        datefmt=LOGGING_DATE_FORMAT,
                        level=LOGGING_LEVEL,
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler(filename=file_name, mode='a')
                        ])
