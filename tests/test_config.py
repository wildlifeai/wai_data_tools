"""Tests for config module."""
from unittest.mock import MagicMock

import pytest
import yaml

from wai_data_tools.utils import config_utils


@pytest.mark.usefixtures("monkeypatch")
def test_load_config(monkeypatch: pytest.MonkeyPatch):
    """Test cases for load_config function.

    Args:
        monkeypatch: MonkeyPatch fixture for mocking yaml load function
    """
    mocked_yaml_safe_load = MagicMock(return_value={"test": "dict"})
    monkeypatch.setattr(target=yaml, name="safe_load", value=mocked_yaml_safe_load)
    content = config_utils.load_config(config_filepath=MagicMock())
    assert isinstance(content, dict)
