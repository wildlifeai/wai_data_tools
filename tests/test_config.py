"""Tests for config module."""
import pathlib

import pytest

from wai_data_tools import config


@pytest.mark.parametrize("config_filepath", [pathlib.Path("./test_config.yml")])
def test_load_config(config_filepath: pathlib.Path):
    """Test cases for load_config function.

    Args:
        config_filepath: Path to config file
    """
    content = config.load_config(config_filepath=config_filepath)
    assert isinstance(content, dict)
