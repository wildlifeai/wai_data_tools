"""Module for loading config file."""

from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_filepath: Path) -> Dict[str, Any]:
    """Load a config YAML file and returns content.

    Args:
        config_filepath: path to config file.

    Returns:
        Content of config file
    """
    with config_filepath.open(mode="r") as f:
        content = yaml.safe_load(f)
        return content
