from __future__ import annotations

import logging
from pathlib import Path


_BASE_LOGGER_NAME = "geography_game"
_LOG_FILE_PATH = Path(__file__).resolve().parent.parent / "logs" / "game_loop.log"


def _configure_base_logger() -> logging.Logger:
    logger = logging.getLogger(_BASE_LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    _LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(_LOG_FILE_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_game_logger(name: str) -> logging.Logger:
    base_logger = _configure_base_logger()
    if name == _BASE_LOGGER_NAME:
        return base_logger
    return logging.getLogger(f"{_BASE_LOGGER_NAME}.{name}")
