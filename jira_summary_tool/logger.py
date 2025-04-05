# logger.py
import logging, sys
from rich.logging import RichHandler

def setup_logging(cfg):
    """Configure logging with console and file handlers based on Config."""
    log_level = logging.getLevelName(cfg.log_level)  # e.g., "DEBUG" or "INFO"
    logger = logging.getLogger()  # root logger
    logger.setLevel(logging.DEBUG)  # capture all levels, handlers will filter
    
    # Console handler with level INFO (or WARNING in prod for less noise)
    console_handler = RichHandler(markup=True)
    console_handler.setLevel(logging.INFO if cfg.mode == "production" else logging.INFO)
    console_fmt = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_fmt)
    
    # File handler with level DEBUG, output to a log file
    file_handler = logging.FileHandler(f"{cfg.output_dir}/app.log", mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                                 datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_fmt)
    
    # Add handlers to root logger
    logger.handlers = []  # reset any default handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.info("Logging is configured.")
