from __future__ import annotations

import logging
import os
import sys
from typing import cast

import structlog
from structlog.typing import Processor

from app.config import settings


def configure_logging(json_format: bool | None = None) -> None:
    use_json = settings.LOG_JSON
    if json_format is not None:
        use_json = json_format
    if json_format is None:
        use_json = (
            use_json
            or os.getenv("CI", "false").lower() == "true"
            or not sys.stderr.isatty()
        )

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if use_json:
        processors: list[Processor] = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=cast(list[Processor], processors),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
