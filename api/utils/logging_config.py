import logging
import sys
from loguru import logger
from datetime import datetime
import os

class InterceptHandler(logging.Handler):
    """
    Default handler from expressions in Loguru documentation.
    See: https://loguru.readthedocs.io/en/stable/overview.html#intercepting-standard-logging-messages
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    file_log_name = f"logs/server_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    # Remove all existing sinks
    logger.remove()

    # Console sink
    logger.add(
        sys.stdout, 
        colorize=True, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        enqueue=True
    )

    # File sink
    logger.add(
        file_log_name,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        encoding="utf-8",
        enqueue=True
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Specific libraries configuration (redirecting them to loguru)
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(name)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False

    return logger
