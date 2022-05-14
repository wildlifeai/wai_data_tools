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


@pytest.mark.parametrize(
    argnames="n_frames, frames_with_target, sampling_frequency",
    argvalues=[(10, np.arange(10), 1), (10, np.arange(10), 2), (10, np.arange(2, 10), 4)],
)
def test_read_frames_in_video(n_frames: int, frames_with_target: np.ndarray, sampling_frequency: int):
    """Test case for read_frames_in_video function.

    Args:
        n_frames: Number of frames to use for constructing mocked video reader
        frames_with_target: Array with frame indices that contains target class
        sampling_frequency: Sampling frequency to use when constructing frame dict
    """
    mocked_img = np.zeros((2, 2))
    mocked_video_reader = [mocked_img] * n_frames

    result_frame_dicts = movie_to_images.read_frames_in_video(
        video_reader=mocked_video_reader,
        frames_with_target=frames_with_target,
        sampling_frequency=sampling_frequency,
    )

    expected_frame_dicts = {
        frame_ind: {"image": mocked_img, "contains_target": frame_ind in frames_with_target}
        for frame_ind in np.arange(0, n_frames, sampling_frequency)
    }

    assert len(result_frame_dicts) == len(expected_frame_dicts)
    for result_frame_ind, expected_frame_ind in zip(result_frame_dicts, expected_frame_dicts):
        assert result_frame_ind == expected_frame_ind

        result_frame_dict = result_frame_dicts[result_frame_ind]
        expected_frame_dict = expected_frame_dicts[expected_frame_ind]

        assert np.allclose(result_frame_dict["image"], expected_frame_dict["image"])
        assert result_frame_dict["contains_target"] == expected_frame_dict["contains_target"]
