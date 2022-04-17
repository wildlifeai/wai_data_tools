"""This module is responsible for configuration of the logging."""
import datetime
import logging
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    logging_dir: Optional[Path] = None, logging_config_file: Optional[Path] = None
) -> None:
    """Initializes and configures the logger.

    Args:
        logging_dir: Optional path to store logs, if not given the logs will be stored in the working directory
        logging_config_file: Optional path to config file for logger. If not given a lightweight default configuration will be used.
    """
    if logging_dir is None:
        logging_dir = Path(os.getcwd())

    logging_dir.mkdir(exist_ok=True)

    if logging_config_file:
        logging.basicConfig(filename=logging_config_file)
    else:
        logging_filename = str(
            logging_dir
            / datetime.datetime.now().strftime("wildlife_log_%H_%M_%d_%m_%Y.log")
        )

        logging.basicConfig(
            encoding="utf-8",
            level=logging.INFO,
            handlers=[logging.FileHandler(logging_filename), logging.StreamHandler()],
        )
