"""
Centralized logging using Loguru.
Import logger from here everywhere in the project.
"""

import sys
from loguru import logger
from config.settings import LOGS_DIR

# Remove default logger
logger.remove()

# Console — colored output
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> → {message}",
    level="DEBUG"
)

# File — full logs with rotation
logger.add(
    LOGS_DIR / "app.log",
    rotation="10 MB",       # new file after 10MB
    retention="7 days",     # keep 7 days of logs
    compression="zip",      # compress old logs
    format="{time} | {level} | {name}:{line} → {message}",
    level="INFO"
)

# Export
__all__ = ["logger"]