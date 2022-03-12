"""Module with IO functionality."""

import logging
import pathlib
from typing import Dict, Union

import imageio
import numpy as np
import pandas as pd


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
    logging.debug("Loading frames at %s", frame_dir)

    frame_filepaths = frame_dir.rglob("*.jpeg")

    frames_dict = {}

    df_video_frames = df_frames[frame_dir.name + ".mjpg" == df_frames["filename"]]

    for frame_filepath in frame_filepaths:

        frame_img = imageio.imread(frame_filepath)

        _, frame_index = frame_filepath.stem.split("___")

        frame_index = int(frame_index)

        target = df_video_frames[df_video_frames["frame_ind"] == frame_index]

        logging.debug("Frame %s target class is %s", frame_filepath.name, target)

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
    dst_video_path = dst_root_dir / video_name
    dst_video_path.mkdir(exist_ok=True, parents=True)

    logging.debug("Saving frames to %s", dst_video_path)

    for frame_ind, f_dict in frames_dict.items():
        frame_filename = f"{video_name}___{frame_ind}.jpeg"
        total_path = dst_video_path / frame_filename
        imageio.imwrite(total_path, f_dict["image"])
