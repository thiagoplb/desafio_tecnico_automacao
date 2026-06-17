import logging
import sys

APP_LOGGER_NAME = "b2bflow"
LOG_FILE = "app.log"


def configure_logging() -> None:
    logger = logging.getLogger(APP_LOGGER_NAME)
    if logger.handlers:
        return
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{APP_LOGGER_NAME}.{name}")
