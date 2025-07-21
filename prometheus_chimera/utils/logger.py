import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(config):
    """Configures the root logger for the PROMETHEUS-CHIMERA system."""
    log_dir = os.path.dirname(config['log_file'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_level = getattr(logging, config.get('level', 'INFO').upper(), logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
    )

    file_handler = RotatingFileHandler(
        config['log_file'],
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(log_format)

    root_logger = logging.getLogger("PROMETHEUS-CHIMERA")
    root_logger.setLevel(log_level)

    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        root_logger.addHandler(console_handler)

    return root_logger
