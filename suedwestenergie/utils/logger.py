"""Logging utilities for production error handling"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Function to set up a logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file (optional, defaults to logs/app.log)
        level: Logging level (default INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "app.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Application logger
app_logger = setup_logger("suedwestenergie_app", level=logging.INFO)


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context information
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    app_logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_info(message: str, context: str = ""):
    """
    Log an info message
    
    Args:
        message: The message to log
        context: Additional context
    """
    log_msg = f"{context}: {message}" if context else message
    app_logger.info(log_msg)


def log_warning(message: str, context: str = ""):
    """
    Log a warning message
    
    Args:
        message: The message to log
        context: Additional context
    """
    log_msg = f"{context}: {message}" if context else message
    app_logger.warning(log_msg)