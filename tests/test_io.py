"""Tests for io module."""
import pathlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from wai_data_tools import io


@pytest.mark.parametrize(
    argnames="frame_dir, df_frames, expected",
    argvalues=[
        (
            Path("./test_path/A"),
            pd.DataFrame(
                {"video_name": ["A", "A", "C"], "frame_ind": [1, 2, 3], "target": ["class", "background", "background"]}
            ),
            {1: {"image": np.array([0]), "target": "class"}, 2: {"image": np.array([0]), "target": "background"}},
        )
    ],
)
def test_load_frames(frame_dir, df_frames, expected):
    """Test case for load_frames function.

    Args:
        frame_dir: Path to frame directory
        df_frames: Dataframe with frame information
        expected: Expected outcome
    """
    mocked_rglob = MagicMock(
        return_value=[
            pathlib.Path("file___1.jpeg"),
            pathlib.Path("file___2.jpeg"),
        ]
    )

    mocked_imread = MagicMock(return_value=np.array([0]))

    with patch.object(pathlib.Path, "rglob", mocked_rglob):
        with patch("imageio.imread", mocked_imread):
            result = io.load_frames(frame_dir=frame_dir, df_frames=df_frames)

    assert len(result) == len(expected)
    for frame_ind, result_frame_dict in result.items():
        assert frame_ind in expected
        assert np.equal(result_frame_dict["image"], expected[frame_ind]["image"])
        assert result_frame_dict["target"] == expected[frame_ind]["target"]


@pytest.mark.parametrize(
    argnames=["video_name", "dst_root_dir", "frames_dict"],
    argvalues=[
        [
            "A",
            pathlib.Path("dst_dir"),
            {1: {"image": np.array([0]), "target": "class"}, 2: {"image": np.array([0]), "target": "background"}},
        ]
    ],
)
def test_save_frames(video_name, dst_root_dir, frames_dict):
    """Test case for save_frames function.

    Args:
        video_name: Name of video
        dst_root_dir: Path to destination root directory
        frames_dict: Frames dictionary to save
    """
    with patch.object(pathlib.Path, "mkdir") as mkdir_mock:
        with patch("imageio.imwrite") as imwrite_mock:
            io.save_frames(video_name=video_name, dst_root_dir=dst_root_dir, frames_dict=frames_dict)
            assert imwrite_mock.call_count == len(frames_dict)
            assert mkdir_mock.call_count == 1
