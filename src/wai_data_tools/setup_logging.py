"""This module is responsible for configuration of the logging."""
import datetime
import logging
import logging.config
import os
from pathlib import Path
from typing import Optional


def setup_logging(logging_dir: Optional[str] = None, logging_config_file: Optional[str] = None) -> None:
    """Initializes and configures the logger.

    Args:
        logging_dir: Optional path to store logs, if None given the logs will be stored in the working directory
        logging_config_file: Optional path to config file for logger.
                             If None given, a lightweight default configuration will be used.
    """
    if logging_dir is None:
        logging_dir = Path(os.getcwd())
    logging_dir = Path(logging_dir)
    logging_dir.mkdir(exist_ok=True)

    log_filename = datetime.datetime.now().strftime("wildlife_log_%H_%M_%d_%m_%Y.log")
    log_filepath = str(logging_dir / log_filename)

    if logging_config_file is None:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.FileHandler(log_filepath), logging.StreamHandler()],
        )
    else:
        logging.config.fileConfig(logging_config_file, defaults={"logfilename": log_filepath})

    logger = logging.getLogger(__name__)
    logger.info("Configured to logger to log content to directory %s with config %s", logging_dir, logging_config_file)
