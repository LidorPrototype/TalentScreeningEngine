import logging
import json
import sys
from datetime import datetime
from logging import LogRecord
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "line": record.lineno,
            "function": record.funcName,
            "module": record.module,
            "path": record.pathname,
            "process": record.process,
            "thread": record.threadName,
            "logger": record.name,
        }

        # Include exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def _get_logger(name: str = "global") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = JsonFormatter()
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False  # Prevent double logging

    return logger


global_logger = _get_logger()
