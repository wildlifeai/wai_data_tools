"""Tests for video_filtering script module."""
import pathlib
from unittest.mock import MagicMock

import cv2
import numpy as np
import pytest

from wai_data_tools.utils import video_filtering


@pytest.mark.parametrize(
    argnames="iterable,expected",
    argvalues=[
        ([0, 1, 2, 3], [[0, 1], [1, 2], [2, 3]]),
        ([0, 1], [[0, 1]]),
        ([0], [[0, None]]),
    ],
)
def test_pairwise(iterable, expected):
    """Test case for pairwise."""
    result = video_filtering.pairwise(iterable=iterable)
    for result_tuple, expected_tuple in zip(result, expected):
        assert result_tuple[0] == expected_tuple[0]
        assert result_tuple[1] == expected_tuple[1]


@pytest.mark.usefixtures("monkeypatch")
def test_convert_video_to_frames(monkeypatch):
    """Test case for convert_video_to_frames."""
    src_file = pathlib.Path("/a/path/to/movie.file")
    mocked_video_reader_read = MagicMock(
        side_effect=[
            (True, np.ones((2, 2))),
            (True, np.ones((2, 2))),
            (False, np.ones((2, 2))),
            (True, np.ones((2, 2))),
            (False, np.ones((2, 2))),
        ]
    )
    monkeypatch.setattr(
        target=cv2.VideoCapture, name="read", value=mocked_video_reader_read  # pylint: disable=no-member
    )
    result = video_filtering.convert_video_to_frames(src_file=src_file)
    assert len(result) == 3


@pytest.mark.parametrize(
    argnames="frames,expected_diff_length",
    argvalues=[
        ([10 * np.ones(1), 20 * np.ones(1), 70 * np.ones(1), 100 * np.ones(1)], 1),
        ([10 * np.ones(1), 70 * np.ones(1), 120 * np.ones(1), 100 * np.ones(1)], 2),
        ([10 * np.ones(1), 70 * np.ones(1), 120 * np.ones(1), 70 * np.ones(1)], 3),
    ],
)
def test_check_frames_difference(frames, expected_diff_length):
    """Test case for check_frames_difference."""
    result = video_filtering.check_frames_differences(frames=frames)
    assert np.sum(result) == expected_diff_length


@pytest.mark.usefixtures("monkeypatch")
def test_video_process_content(monkeypatch):
    """Test case for video_process_content."""
    monkeypatch.setattr(target=video_filtering, name="convert_video_to_frames", value=MagicMock())

    returned_frame_diffs = [0, 0, 1]

    monkeypatch.setattr(
        target=video_filtering, name="check_frames_differences", value=MagicMock(side_effect=[returned_frame_diffs])
    )

    expected = False
    result = video_filtering.video_process_content(pathlib.Path("/path/to/file"))
    assert result == expected
