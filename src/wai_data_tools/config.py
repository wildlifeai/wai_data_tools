"""Module for loading config file."""
import pathlib
from typing import Any, Dict

import yaml


def load_config(config_filepath: pathlib.Path) -> Dict[str, Any]:
    """Load a config YAML file and returns content.

    Args:
        config_filepath: Path to config file

    Returns:
        Content of config file
    """
    with config_filepath.open(mode="r") as file:
        content = yaml.safe_load(file)
        return content
