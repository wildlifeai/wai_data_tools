"""
Module with IO functionality.
"""

import logging
import pathlib
from typing import Dict, Union

import imageio
import numpy as np


def load_frames(frame_dir: pathlib.Path) -> Dict[int, Dict[str, Union[str, np.ndarray]]]:
    """
    Loads frame files from a directory.
    :param frame_dir: Path to directory where frames are stored in a target class folder or background class folder
    :return: Dictionary where key is frame index and value is a dictionary with the target class and frame image
    """

    logging.debug("Loading frames at %s", frame_dir)

    frame_filepaths = frame_dir.rglob("*.jpeg")

    frames_dict = {}

    for frame_filepath in frame_filepaths:

        frame_img = imageio.imread(frame_filepath)

        frame_index = int(frame_filepath.stem.split("___")[-1])

        target = frame_filepath.parent.stem

        logging.debug("Frame %s target class is %s", frame_filepath.name, target)

        frames_dict[frame_index] = {"img": frame_img,
                                    "target": target}
    return frames_dict


def save_frames(video_name: str,
                dst_root_dir: pathlib.Path,
                frames_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]]):
    """
    Saves frames to new file structure.
    :param video_name: Path to directory containing source frame images
    :param dst_root_dir: Path to root destination directory to save frame images in
    :param frames_dict: Dictionary where key is frame index and value is a dictionary with the label class
                        and frame image
    """
    dst_video_path = dst_root_dir / video_name

    logging.debug("Saving frames to %s", dst_video_path)

    for frame_ind, f_dict in frames_dict.items():
        frame_filename = f"{video_name}___{frame_ind}.jpeg"

        label_dir = dst_video_path / f_dict["target"]
        label_dir.mkdir(exist_ok=True, parents=True)
        total_path = label_dir / frame_filename
        imageio.imwrite(total_path, f_dict["img"])
