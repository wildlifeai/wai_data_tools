"""Tests for preprocessing module."""
from typing import Dict, Tuple

import pytest

from wai_data_tools import preprocessing


@pytest.mark.parametrize(argnames="transforms_config", argvalues=[{"img_size": (56, 56)}, {"img_size": (200, 100)}, {}])
def test_compose_transforms(transforms_config: Dict[str, Tuple[int, int]]) -> None:
    """Test case for compose_transforms.

    Args:
        transforms_config: Configuration for preprocessing transforms.
    """
    sequential_transforms = preprocessing.compose_transforms(transforms_config=transforms_config)
    assert len(sequential_transforms.transforms) == len(transforms_config) + 2
