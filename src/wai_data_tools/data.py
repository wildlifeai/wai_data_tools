"""Data transformation functionality."""
import math

import numpy as np


def calc_test_split_indices(n_files: int, test_split_size: float, seed=0) -> np.ndarray:
    """Calculates a split for training and testing files and returning their indices.

    Args:
        n_files: Number of files to split
        test_split_size: Ratio of n_files should be in test split
        seed: Random seed number to use for sampling

    Returns:
        Test data indices
    """
    np.random.seed(seed)

    n_test_files = math.floor(n_files * test_split_size)

    test_file_inds = np.random.choice(n_files, size=n_test_files, replace=False)

    return test_file_inds
