"""Tests for file_handling module."""
import pathlib
from pathlib import Path

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

    def mock_imread(*_, **__):
        return np.zeros(1)

    monkeypatch.setattr(target=imageio, name="imread", value=mock_imread)

    def mock_rglob(*_, **__):
        files = [
            pathlib.Path("file___1.jpeg"),
            pathlib.Path("file___2.jpeg"),
        ]
        return files

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

    def mock_mkdir(*_, **__):
        pass

    monkeypatch.setattr(target=pathlib.Path, name="mkdir", value=mock_mkdir)

    def mock_imwrite(*_, **__):
        pass

    monkeypatch.setattr(target=imageio, name="imwrite", value=mock_imwrite)

    file_handling.save_frames(video_name=video_name, dst_root_dir=dst_root_dir, frames_dict=frames_dict)
