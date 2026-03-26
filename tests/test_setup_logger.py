import logging
from alkemio_virtual_contributor_engine.setup_logger import setup_logger


def test_setup_logger_returns_logger():
    logger = setup_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_setup_logger_has_stream_handler():
    logger = setup_logger("test_stream")
    stream_handlers = [
        h for h in logger.handlers if isinstance(h, logging.StreamHandler)
    ]
    assert len(stream_handlers) >= 1


def test_setup_logger_no_file_handler():
    logger = setup_logger("test_no_file")
    file_handlers = [
        h for h in logger.handlers if isinstance(h, logging.FileHandler)
    ]
    assert len(file_handlers) == 0


def test_setup_logger_json_format():
    logger = setup_logger("test_format")
    handler = logger.handlers[-1]
    fmt = handler.formatter._fmt
    assert '"time"' in fmt
    assert '"level"' in fmt
    assert '"message"' in fmt
