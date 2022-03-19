"""This module is responsible for configuration of the logging."""
import datetime
import logging
import pathlib


def setup_logging(logging_dir: pathlib.Path) -> None:
    """Sets up logging.

    Args:
        logging_dir: Path to directory to store log files
    """
    logging_dir.mkdir(exist_ok=True)

    logging_filename = str(logging_dir / datetime.datetime.now().strftime("wildlife_log_%H_%M_%d_%m_%Y.log"))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler(logging_filename), logging.StreamHandler()],
    )
