import logging
from logging.handlers import TimedRotatingFileHandler
import sys
from pathlib import Path
from datetime import datetime

from app.core.config import settings

# Create logs directory if it doesn't exist
settings.LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = settings.LOG_DIR / "dms.log"

file_handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)

file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

logging.basicConfig(
    level=settings.LOG_LEVEL,
    handlers=[file_handler, console_handler]
)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    return logger