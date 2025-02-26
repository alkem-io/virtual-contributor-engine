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
    f_handler = logging.FileHandler(
        os.path.join(os.path.expanduser(env.local_path), "app.log")
    )

    c_handler.setLevel(env.log_level)
    f_handler.setLevel(logging.WARNING)

    c_format = logging.Formatter(
        '{"time": "%(asctime)s", "name": %(name)r, "level": "%(levelname)s", "message": %(message)r}',
        "%m-%d %H:%M:%S",
    )
    f_format = logging.Formatter(
        '{"time": "%(asctime)s", "name": %(name)r, "level": "%(levelname)s", "message": %(message)r}',
        "%m-%d %H:%M:%S",
    )

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info(f"log level {os.path.basename(__file__)}: {env.log_level}")

    return logger
