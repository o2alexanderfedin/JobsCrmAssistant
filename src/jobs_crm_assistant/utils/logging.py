"""Logging configuration for the application."""
import sys
from typing import Dict, Union

from loguru import logger


def setup_logging(
    level: Union[str, int] = "INFO",
    format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
) -> None:
    """Configure application logging.

    Args:
        level: The logging level to use
        format: The format string for log messages
    """
    # Remove default handler
    logger.remove()

    # Add custom handler
    config: Dict = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": format,
                "level": level,
                "colorize": True,
            }
        ],
    }

    logger.configure(**config)


# Configure default logging
setup_logging()
