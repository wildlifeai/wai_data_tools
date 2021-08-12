import logging
import datetime
from pathlib import Path


def setup_logging():
    """
    Configures the logging.
    """
    logging_dir = Path(r'C:\git\wildlife_ai_file_filter\logs')

    logging.basicConfig(filename=str(logging_dir / datetime.now().strftime('wildlife_log_%H_%M_%d_%m_%Y.log')),
                        encoding='utf-8',
                        level=logging.DEBUG)
