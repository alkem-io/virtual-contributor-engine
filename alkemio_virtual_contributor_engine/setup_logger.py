import logging
import sys
import io
import os
from alkemio_virtual_contributor_engine.config import env


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(env.log_level)

    c_handler = logging.StreamHandler(
        io.TextIOWrapper(sys.stdout.buffer, line_buffering=True)
    )
    c_handler.setLevel(env.log_level)

    c_format = logging.Formatter(
        '{"time": "%(asctime)s", "name": %(name)r, '
        '"level": "%(levelname)s", "message": %(message)r}',
        "%m-%d %H:%M:%S",
    )
    c_handler.setFormatter(c_format)

    logger.addHandler(c_handler)

    logger.info(f"log level {os.path.basename(__file__)}: {env.log_level}")

    return logger
