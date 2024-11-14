import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configure logging for the bot"""
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Create formatters and handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.DEBUG)

    # File handler
    file_handler = RotatingFileHandler(
        logs_dir / 'bot.log',
        maxBytes=5000000,
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG)

    # Get the loggers
    loggers = [
        logging.getLogger(),  # Root logger
        logging.getLogger('AnimeCogs'),
        logging.getLogger('AnimeBaseCog'),
        logging.getLogger('discord'),
        logging.getLogger('discord.http'),
    ]

    # Configure each logger
    for logger in loggers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    # Test logging setup
    test_logger = logging.getLogger('AnimeCogs')
    test_logger.debug("Logging setup complete")
    return test_logger