"""
Logging configuration for the application.
Centralizes logging setup for consistency across the application.
"""
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    """
    Configure application-wide logging.
    
    Sets up:
    - Rotating file handler with size limits
    - Console handler for development
    - Proper formatting
    - Log level based on environment
    
    Args:
        app: Flask application instance
    """
    # Determine log level based on environment
    if app.config.get('DEBUG'):
        log_level = logging.DEBUG
    elif app.config.get('TESTING'):
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    
    # Create logs directory if it doesn't exist
    log_dir = "./var/log"
    os.makedirs(log_dir, exist_ok=True)
    
    # Define log format
    log_format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    date_format = "%m-%d %H:%M"
    
    # Create formatters
    formatter = logging.Formatter(log_format, datefmt=date_format)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "kayak-trip-planner.log"),
        maxBytes=2_000_000,  # 2MB
        backupCount=5,
        encoding='UTF-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Add our handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Set logging level for werkzeug (Flask's HTTP server)
    logging.getLogger('werkzeug').setLevel(logging.WARNING if not app.config.get('DEBUG') else logging.INFO)
    
    # Set logging level for SQLAlchemy
    if app.config.get('DEBUG'):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    else:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    app.logger.info(f"Logging configured at {log_level} level")
    app.logger.info(f"Log file: {os.path.join(log_dir, 'kayak-trip-planner.log')}")
