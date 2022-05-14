"""Module with IO functionality."""

import logging
import pathlib
from pathlib import Path
from typing import Any, Dict, Union

import imageio
import numpy as np
import pandas as pd

# This hotfix is added since imageio checks compability by file extension name instead of probing.
from imageio.plugins.ffmpeg import FfmpegFormat

FfmpegFormat.can_read = lambda x, y: True


def load_frames(
    frame_dir: pathlib.Path,
    df_frames: pd.DataFrame,
) -> Dict[int, Dict[str, Union[str, np.ndarray]]]:
    """Load frame files from a directory.

    Args:
        frame_dir: Path to directory where frames are stored in a target
            class folder or background class folder
        df_frames: Dataframe with frame information.

    Returns:
        Dictionary where key is frame index and value is a dictionary
        with the target class and frame image
    """
    logger = logging.getLogger(__name__)

    logger.debug("Loading frames at %s", frame_dir)

    frame_filepaths = frame_dir.rglob("*.jpeg")

    frames_dict = {}

    df_video_frames = df_frames[frame_dir.name == df_frames["video_name"]]

    for frame_filepath in frame_filepaths:

        frame_img = imageio.imread(frame_filepath)

        _, frame_index = frame_filepath.stem.split("___")

        frame_index = int(frame_index)

        target = df_video_frames.loc[df_video_frames["frame_ind"] == frame_index, "target"].item()

        logger.debug("Frame %s target class is %s", frame_filepath.name, target)

        frames_dict[frame_index] = {"image": frame_img, "target": target}
    return frames_dict


def save_frames(
    video_name: str,
    dst_root_dir: pathlib.Path,
    frames_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]],
):
    """Save frames to new file structure.

    Args:
        video_name: Path to directory containing source frame images
        dst_root_dir: Path to root destination directory to save frame
            images in
        frames_dict: Dictionary where key is frame index and value is a
            dictionary with the label class and frame image
    """
    logger = logging.getLogger(__name__)

    dst_video_path = dst_root_dir / video_name
    dst_video_path.mkdir(exist_ok=True, parents=True)

    logger.debug("Saving frames to %s", dst_video_path)

    for frame_ind, f_dict in frames_dict.items():
        frame_filename = f"{video_name}___{frame_ind}.jpeg"
        total_path = dst_video_path / frame_filename
        imageio.imwrite(total_path, f_dict["image"])


def get_video_reader(video_filepath: Path) -> Any:
    """Get a imageio reader object for the provided video file. Assumes ffmpeg encoding.

    Args:
        video_filepath: Path to ffmpeg compatible video file

    Returns:
        reader object for parsing video
    """
    return imageio.get_reader(video_filepath, "FFMPEG")
