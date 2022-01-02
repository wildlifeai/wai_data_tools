"""
Module for loading config file.
"""

from pathlib import Path
from typing import Dict, Any

import yaml


def load_config(config_filepath: Path) -> Dict[str, Any]:
    """
    Loads a config YAML file and returns content.
    :param config_filepath: path to config file.
    :return: Content of config file
    """
    with config_filepath.open(mode="r") as f:
        content = yaml.safe_load(f)
        return content
