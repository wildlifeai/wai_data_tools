"""Module for loading config file."""

from pathlib import Path
from typing import Any, Dict, List, Union

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


def get_classes(label_config_list: List[Dict[str, Union[int, str, bool]]]) -> List[str]:
    """Get the specified classes from the label configuration list.

    Args:
        label_config_list: List of configurations for labels in the
            dataset. Will append background class regardless

    Returns:
        List of class names
    """
    return classes
