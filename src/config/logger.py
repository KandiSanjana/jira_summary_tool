"""
Logging configuration module.

This module provides functionality to set up and configure logging for the application,
including both console and file handlers with different formatting and log levels.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from src.config.config import Config


def setup_logging(log_level: str, log_file: Optional[str] = None) -> None:
    """Configure logging with console and file handlers based on configuration.
    
    Sets up two handlers:
    1. Console handler with Rich formatting for better readability
    2. File handler for detailed logging to a file
    
    Args:
        config: Configuration object containing logging settings
        log_file: Optional path to log file. Defaults to 'app.log' in current directory.
        
    Example:
        >>> setup_logging(config)
        >>> logging.info("Application started")
    """
    # Get root logger and set base level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels, handlers will filter
    
    # Remove any existing handlers
    logger.handlers.clear()
    
    # Configure console handler
    _setup_console_handler(logger, log_level)
    
    # Configure file handler
    _setup_file_handler(logger, log_file)
    
    # Log successful configuration
    logger.info("Logging system initialized")


def _setup_console_handler(logger: logging.Logger, log_level: str) -> None:
    """Configure and add console handler with Rich formatting.
    
    Args:
        logger: Logger instance to configure
        config: Configuration object
    """
    console_handler = RichHandler(
        markup=True,
        show_time=False,
        show_path=True,
        rich_tracebacks=True
    )
    
    # Set console log level based on environment
    console_level = logging.INFO if log_level == "production" else logging.DEBUG
    console_handler.setLevel(console_level)
    
    # Simple format for console
    console_fmt = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_fmt)
    
    logger.addHandler(console_handler)


def _setup_file_handler(
    logger: logging.Logger,
    log_file: Optional[str] = None
) -> None:
    """Configure and add file handler for detailed logging.
    
    Args:
        logger: Logger instance to configure
        config: Configuration object
        log_file: Optional path to log file
    """
    # Default log file path
    if not log_file:
        log_file = "app.log"
    
    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure file handler
    file_handler = logging.FileHandler(
        filename=log_file,
        mode='a',  # Append mode to preserve logs
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Detailed format for file logging
    file_fmt = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)
    
    logger.addHandler(file_handler)
