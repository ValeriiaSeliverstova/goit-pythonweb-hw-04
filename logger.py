# logger.py
# Централізоване налаштування логування для всього застосунку

import os
import logging
from typing import Optional

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(levelname)s: %(message)s")

_configured = False


def configure_logging(
    level: Optional[str] = None, format: Optional[str] = None
) -> None:
    global _configured
    if _configured:
        return

    logging.basicConfig(
        level=(level or LOG_LEVEL),
        format=(format or LOG_FORMAT),
    )
    _configured = True


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:  # Optional[str] (typing) або str, або None
    return logging.getLogger(
        name
    )  # Повертає об'єкт логера з вказаним ім'ям або кореневий логер, якщо ім'я не вказано. з методами (debug, info, warning, error, critical)
