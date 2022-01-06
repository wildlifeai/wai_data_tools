import logging
import datetime
from pathlib import Path


def setup_logging():
    """
    Configures the logging.
    """
    logging_dir = Path(r'C:\git\wildlife_ai_file_filter\logs')

    logging_dir.mkdir(exist_ok=True)

    logging_filename = str(logging_dir / datetime.datetime.now().strftime('wildlife_log_%H_%M_%d_%m_%Y.log'))

    logging.basicConfig(encoding='utf-8',
                        level=logging.DEBUG,
                        handlers=[
                            logging.FileHandler(logging_filename),
                            logging.StreamHandler()
                        ]
                        )
