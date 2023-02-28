"""Tests for movie_to_images.py module."""

import numpy as np
import pytest

from wai_data_tools import movie_to_images


@pytest.mark.parametrize(
    argnames="t_start, t_end, fps, expected_frames",
    argvalues=[
        (0, 10, 1, np.arange(0, 10)),
        (0, 10, 2, np.arange(0, 20)),
        (0, 20, 2, np.arange(0, 40)),
        (1, 20, 2, np.arange(2, 40)),
        (0.25, 10, 1, np.arange(0, 10)),  # if start time does not line up with frame, floor should be used
        (0, 9.75, 1, np.arange(0, 10)),  # if end time does not line up with frame, ceil should be used
    ],
)
def test_calculate_frames_in_timespan(t_start: float, t_end: float, fps: float, expected_frames: int) -> None:
    """Test case for calculate_frames_in_timespan function.

    Args:
        t_start: start of time interval in seconds
        t_end: end of time interval in seconds
        fps: frames per second
        expected_frames: expected number of frames
    """
    result_frames = movie_to_images.calculate_frames_in_timespan(
        t_start=t_start,
        t_end=t_end,
        fps=fps,
    )

    assert np.allclose(result_frames, expected_frames)
