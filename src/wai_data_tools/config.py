"""
Module for loading config file.
"""

from pathlib import Path
from typing import Dict, Any, List, Union

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


def get_classes(label_config_list: List[Dict[str, Union[int, str, bool]]]) -> List[str]:
    """
    Gets the specified classes from the label configuration list.
    :param label_config_list: List of configurations for labels in the dataset. Will append background class regardless
    :return: List of class names
    """

    return classes
