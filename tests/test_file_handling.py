"""Tests for file_handling module."""
import pathlib
from pathlib import Path
from unittest.mock import MagicMock

import imageio
import numpy as np
import pandas as pd

from wai_data_tools import file_handling


def test_load_frames(monkeypatch):
    """Test case for load_frames function.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    frame_dir = Path("./test_path/A")

    df_frames = pd.DataFrame(
        {"video_name": ["A", "A", "C"], "frame_ind": [1, 2, 3], "target": ["class", "background", "background"]}
    )

    expected = {1: {"image": np.array([0]), "target": "class"}, 2: {"image": np.array([0]), "target": "background"}}

    mock_imread = MagicMock(return_value=np.zeros(1))

    monkeypatch.setattr(target=imageio, name="imread", value=mock_imread)

    mock_rglob = MagicMock(return_value=[pathlib.Path("file___1.jpeg"), pathlib.Path("file___2.jpeg")])

    monkeypatch.setattr(target=pathlib.Path, name="rglob", value=mock_rglob)

    result = file_handling.load_frames(frame_dir=frame_dir, df_frames=df_frames)

    assert len(result) == len(expected)
    for frame_ind, result_frame_dict in result.items():
        assert frame_ind in expected
        assert np.equal(result_frame_dict["image"], expected[frame_ind]["image"])
        assert result_frame_dict["target"] == expected[frame_ind]["target"]


def test_save_frames(monkeypatch):
    """Test case for save_frames function.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    video_name = "A"
    dst_root_dir = pathlib.Path("dst_dir")
    frames_dict = {1: {"image": np.array([0]), "target": "class"}, 2: {"image": np.array([0]), "target": "background"}}

    mock_mkdir = MagicMock()

    monkeypatch.setattr(target=pathlib.Path, name="mkdir", value=mock_mkdir)

    mock_imwrite = MagicMock()

    monkeypatch.setattr(target=imageio, name="imwrite", value=mock_imwrite)

    file_handling.save_frames(video_name=video_name, dst_root_dir=dst_root_dir, frames_dict=frames_dict)

    assert mock_mkdir.call_count == 1
    assert mock_imwrite.call_count == len(frames_dict)


def test_get_video_reader(monkeypatch):
    """Test case for get_video_reader function.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    video_filepath = pathlib.Path("videofile.mjpg")
    expected = "reader"

    mock_get_reader = MagicMock(return_value=expected)

    monkeypatch.setattr(target=imageio, name="get_reader", value=mock_get_reader)

    result = file_handling.get_video_reader(video_filepath=video_filepath)

    assert mock_get_reader.call_count == 1
    assert result == expected
