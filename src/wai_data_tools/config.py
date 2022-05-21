"""Module for loading config file."""
import pathlib
from typing import Any, Dict

import yaml


def load_config(config_file: pathlib.Path) -> Dict[str, Any]:
    """Load a config YAML file and returns content.

    Args:
        config_file: Path to config file

    Returns:
        Content of config file
    """
    with config_file.open(mode="r") as file:
        content = yaml.safe_load(file)
        return content
