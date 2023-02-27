from pathlib import Path
import logging
from typing import TextIO


def GenerateLogger(filename : Path) -> logging.Logger:
    logger: logging.Logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter("%(asctime)s - (%(filename)s:%(lineno)d) - %(levelname)s\n%(message)s")
    formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    formatter.default_msec_format = '%s.%03d'

    ch: logging.StreamHandler[TextIO] = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh: logging.FileHandler = logging.FileHandler(filename, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger