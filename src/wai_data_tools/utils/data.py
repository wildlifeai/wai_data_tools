"""Data transformation functionality."""
import logging
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


def calculate_frames_in_timespan(t_start: float, t_end: float, fps: float) -> np.ndarray:
    """Calculate the frames in the given timespan. Will include one more frame at each end if possible.

    Args:
        t_start: start of time interval in seconds
        t_end: end of time interval in seconds
        fps: frames per second

    Returns:
        array with frame indices
    """
    logger = logging.getLogger(__name__)

    logger.debug("Calculating start and end frame.")

    t_frame = 1 / fps

    frame_start = t_start / t_frame

    if frame_start % 1 > 0:
        logger.debug("Remainder when calculating the index for start frame is not zero. Performing floor operation.")
        frame_start = np.floor(frame_start)

    frame_end = t_end / t_frame

    if frame_end % 1 > 0:
        logger.debug("Remainder when calculating the index for end frame is not zero. Performing ceiling operation.")
        frame_end = np.ceil(frame_end)

    logger.debug("Frames with label start at frame %s and ends at %s", frame_start, frame_end)

    return np.arange(frame_start, frame_end)
