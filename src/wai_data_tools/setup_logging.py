"""This module is responsible for configuration of the logging."""
import datetime
import logging
import logging.config
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    logging_dir: Optional[str] = None, logging_config_file: Optional[str] = None
) -> None:
    """Initializes and configures the logger.

    Args:
        logging_dir: Optional path to store logs, if default given the logs will be stored in the working directory
        logging_config_file: Optional path to config file for logger. If default given a lightweight default configuration will be used.
    """
    if logging_dir == "default":
        logging_dir = Path(os.getcwd())
        print(logging_dir)
    logging_dir = Path(logging_dir)

    logging_dir.mkdir(exist_ok=True)

    if logging_config_file == "default":
        logging_filename = str(
            logging_dir
            / datetime.datetime.now().strftime("wildlife_log_%H_%M_%d_%m_%Y.log")
        )

        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.FileHandler(logging_filename), logging.StreamHandler()],
        )
    else:
        logging.config.fileConfig(logging_config_file)
