"""This module is responsible for conversion of the videos to frame by frame format."""
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

import imageio
import numpy as np
import pandas as pd
import tqdm

# This hotfix is added since imageio checks compability by file extension name instead of probing.
from imageio.plugins.ffmpeg import FfmpegFormat

from wai_data_tools import file_handling

FfmpegFormat.can_read = lambda x, y: True


def get_video_reader(video_filepath: Path) -> Any:
    """Get a imageio reader object for the provided video file. Assumes ffmpeg encoding.

    Args:
        video_filepath: Path to ffmpeg compatible video file

    Returns:
        reader object for parsing video
    """
    return imageio.get_reader(video_filepath, "FFMPEG")


def calculate_frames_in_timespan(t_start: np.ndarray, t_end: np.ndarray, fps: float) -> np.ndarray:
    """Calculate the frames in the given timespan. Will include one more frame at each end if possible.

    Args:
        t_start: start of time interval
        t_end: end of time interval
        fps: frames per second

    Returns:
        array with frame indices
    """
    logging.debug("Calculating start and end frame.")

    t_frame = 1 / fps

    frame_start = t_start / t_frame

    if frame_start % 1 > 0:
        logging.debug("Remainder when calculating the index for start frame is not zero. Performing floor operation.")
        frame_start = np.floor(frame_start)

    frame_end = t_end / t_frame

    if frame_end % 1 > 0:
        logging.debug("Remainder when calculating the index for end frame is not zero. Performing ceiling operation.")
        frame_end = np.ceil(frame_end)

    logging.debug("Frames with label start at frame %s and ends at %s", frame_start, frame_end)

    return np.arange(frame_start, frame_end)


def read_frames_in_video(
    video_reader: Any, frames_with_target: np.ndarray, sampling_frequency: int = 1
) -> Dict[int, Dict[str, Union[np.ndarray, bool]]]:
    """Read the frames in a video by iterating a video reader object.

    Args:
        video_reader: imageio reader for the video to filter.
        frames_with_target: array with frame indices for frames that
            should be marked as containing a target class.
        sampling_frequency: How often in video to read frame in video,
            i.e. sampling frequency of 2 is every second frame and
            sampling frequency 4 is every fourth frame. Default is 1.

    Returns:
        a dict of dicts where the key in root dict is the frame index
        and values is dicts with frame information. Each frame
        information dict follows schema: {"image": numpy array for frame
        image,
         "contains_target": boolean if label is present in image}
    """
    logging.debug("Filtering frames in video to label and non label frames")
    frames_dict = {}
    for frame_ind, frame_img in enumerate(video_reader):
        if frame_ind % sampling_frequency != 0:
            continue

        contains_label = frame_ind in frames_with_target

        frame_information_dict = {"image": frame_img, "contains_target": contains_label}
        frames_dict[frame_ind] = frame_information_dict
    return frames_dict


def split_video_file_to_frame_files(
    video_filepath: Path,
    video_row: pd.Series,
    label_config: Dict[str, Union[int, bool, str]],
) -> Dict[int, Dict[str, Union[np.ndarray, bool]]]:
    """Split a video file into separate frames in the form of .jpeg files.

    Args:
        video_filepath: Path to .mjpg video file
        video_row: Series with video information
        label_config: Label configuration

    Returns:
        Dictionary where key is frame index and value is dict with frame array and target flag.
    """
    is_target = label_config["is_target"]
    sampling_frequency = label_config["sampling_frequency"]

    logging.debug("Splitting video file to frame files...")

    reader = get_video_reader(video_filepath=video_filepath)
    meta = reader.get_meta_data()

    if is_target:
        target_frames = calculate_frames_in_timespan(
            t_start=video_row["start"],
            t_end=video_row["end"],
            fps=meta["fps"],
        )
    else:
        target_frames = []

    frames_dict = read_frames_in_video(
        video_reader=reader,
        frames_with_target=target_frames,
        sampling_frequency=sampling_frequency,
    )
    return frames_dict


def split_video_files_to_frame_files(
    src_video_dir: Path,
    dst_frame_dir: Path,
    video_dataframe: pd.DataFrame,
    label_config: Dict[str, Union[int, bool, str]],
) -> pd.DataFrame:
    """Splits video files in source directory, calculates frame information and stores result in destination directory.

    Args:
        src_video_dir: Path to directory where video files is stored
        dst_frame_dir: Path to directory to store new data
        video_dataframe: Dataframe with video information
        label_config: Label configuration

    Returns:
        Dataframe with frame information
    """
    label_name = label_config["name"]
    logging.info("Filtering dataframe based on label %s", label_name)
    label_dataframe = video_dataframe[video_dataframe["label"] == label_name]

    frame_rows = []

    for _, video_row in tqdm.tqdm(list(label_dataframe.iterrows())):

        video_filename = video_row["filename"]
        folder = video_row["folder"]

        video_filepath = src_video_dir / folder / video_filename

        try:
            frames_dict = split_video_file_to_frame_files(
                video_filepath=video_filepath,
                video_row=video_row,
                label_config=label_config,
            )
        except FileNotFoundError:
            logging.debug("Could not find file: %s", video_filepath.name)
            continue

        frame_rows.extend(create_frame_information_rows(video_row=video_row, frames_dict=frames_dict))

        file_handling.save_frames(video_name=video_filepath.stem, dst_root_dir=dst_frame_dir, frames_dict=frames_dict)

    label_frame_df = pd.DataFrame(data=frame_rows)
    return label_frame_df


def create_frame_information_rows(
    video_row: pd.Series, frames_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]]
) -> List[pd.Series]:
    """Creates frame information rows from video row.

    Args:
        video_row: Series with video information
        frames_dict: Dictionary with frame information

    Returns:
        List with rows describing frame information
    """
    frame_rows = []
    for frame_ind, frame_dict in frames_dict.items():
        new_row = video_row.copy()
        new_row["frame_ind"] = frame_ind
        new_row["target"] = video_row["label"] if frame_dict["contains_target"] else "background"
        new_row["video_name"] = new_row["filename"].replace(".mjpg", "")
        new_row["file_name"] = f"{new_row['video_name']}___{new_row['frame_ind']}.jpeg"

        new_row = new_row[["video_name", "frame_ind", "file_name", "target", "label"]]

        frame_rows.append(new_row)
    return frame_rows
