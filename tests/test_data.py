"""Tests for data module."""
import numpy as np
import pytest

from wai_data_tools import data


@pytest.mark.parametrize("n_files, test_split_size, expected_indices", [[10, 0.2, np.array([2, 8])]])
def test_calc_test_split_indices(n_files: int, test_split_size: int, expected_indices: np.ndarray):
    """Test cases for calc_test_split_indices function.

    Args:
        n_files: Number of files
        test_split_size: Ratio to allocate to test
        expected_indices: Expected indices to get after call
    """
    seed = 0

    result_indices = data.calc_test_split_indices(n_files=n_files, test_split_size=test_split_size, seed=seed)

    assert np.allclose(result_indices, expected_indices)
