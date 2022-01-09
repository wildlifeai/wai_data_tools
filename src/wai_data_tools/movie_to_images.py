
import logging
import pathlib
from pathlib import Path
from typing import Any, List, Dict, Union

import imageio
import numpy as np
import pandas as pd
import tqdm

from wai_data_tools import read_excel


def get_video_reader(video_filepath: Path) -> Any:
    """
    Gets a imageio reader object for the provided video file. Assumes ffmpeg encoding.
    :param video_filepath: Path to ffmpeg compatible video file
    :return: reader object for parsing video
    """
    return imageio.get_reader(video_filepath, 'FFMPEG')


def calculate_frames_in_timespan(t_start: np.ndarray, t_end: np.ndarray, fps: float) -> np.ndarray:
    """
    Calculates the frames in the given timespan. Will include one more frame at each end if possible.
    :param t_start: start of time interval
    :param t_end: end of time interval
    :param fps: frames per second
    :return: array with frame indices
    """

    logging.info("Calculating start and end frame.")

    t_frame = 1 / fps

    frame_start = t_start / t_frame

    if frame_start % 1 > 0:
        logging.info("Remainder when calculating the index for start frame is not zero. Performing floor operation.")
        frame_start = np.floor(frame_start)

    frame_end = t_end / t_frame

    if frame_end % 1 > 0:
        logging.info("Remainder when calculating the index for end frame is not zero. Performing ceiling operation.")
        frame_end = np.ceil(frame_end)

    logging.info("Frames with label start at frame %s and ends at %s", frame_start, frame_end)

    return np.arange(frame_start, frame_end)


def read_frames_in_video(video_reader: Any,
                         frames_with_target: np.ndarray,
                         sampling_frequency: int = 1) -> Dict[int, Dict[str, Union[np.ndarray, bool]]]:
    """
    Reads the frames in a video by iterating a video reader object.
    :param video_reader: imageio reader for the video to filter.
    :param frames_with_target: array with frame indices for frames that should be marked as containing a target class.
    :param sampling_frequency: How often in video to read frame in video, i.e. sampling frequency of 2 is every
                               second frame and sampling frequency 4 is every fourth frame. Default is 1.
    :return: a dict of dicts where the key in root dict is the frame index and values is dicts with frame information.
             Each frame information dict follows schema:
             {"image": numpy array for frame image,
              "contains_target": boolean if label is present in image}
    """

    logging.info("Filtering frames in video to label and non label frames")
    frames_dict = {}
    for frame_ind, frame_img in enumerate(video_reader):
        if frame_ind % sampling_frequency != 0:
            continue
        if frame_ind in frames_with_target:
            contains_label = True
        else:
            contains_label = False

        frame_information_dict = {
            "image": frame_img,
            "contains_target": contains_label
        }
        frames_dict[frame_ind] = frame_information_dict
    return frames_dict


def split_video_file_to_frame_files(video_filepath: Path,
                                    excel_dataframe: pd.DataFrame,
                                    label_config: Dict[str, Union[int, bool, str]]
                                    ) -> Dict[int, Dict[str, Union[np.ndarray, bool]]]:
    """
    Splits a video file into separate frames in the form of .jpeg files.
    :param video_filepath: Path to .mjpg video file
    :param excel_dataframe: Dataframe with file information
    :param label_config: Label configuration
    """

    label_name = label_config["name"]
    is_target = label_config["is_target"]
    sampling_frequency = label_config["sampling_frequency"]

    logging.info("Splitting video file to frame files...")

    reader = get_video_reader(video_filepath=video_filepath)
    meta = reader.get_meta_data()

    logging.info("Filtering dataframe based on label %s", label_name)
    excel_dataframe = excel_dataframe[excel_dataframe["label"] == label_name]
    video_row = excel_dataframe[excel_dataframe["filename"] == video_filepath.name]
    if video_row.shape[0] > 1:
        raise ValueError("More than 1 entry found that matches the query in the dataframe")

    if is_target:
        target_frames = calculate_frames_in_timespan(t_start=video_row["start"].values,
                                                     t_end=video_row["end"].values,
                                                     fps=meta["fps"])
    else:
        target_frames = []

    frames_dict = read_frames_in_video(video_reader=reader,
                                       frames_with_target=target_frames,
                                       sampling_frequency=sampling_frequency)
    return frames_dict


def save_frames(frames_dict: Dict[int, Dict[str, Union[np.ndarray, bool]]],
                src_video_filestem: str,
                label_name: str,
                dst_frame_dir: pathlib.Path) -> None:
    """
    Saves frames in a frame list to a destination root directory. folder location will depend on label presence.
    :param frames_dict: List of dict containing where each dict contains frame array and target presence information.
    :param src_video_filestem: filename stem of source video
    :param label_name: Target class label name
    :param dst_frame_dir: destination root directory to save frames
    """
    logging.info("Saving frames")

    for frame_ind, frame_dict in frames_dict.items():
        frame_img = frame_dict["image"]
        if frame_dict["contains_target"]:
            label_folder_name = label_name
        else:
            label_folder_name = f"no_{label_name}"

        output_filename = f"{src_video_filestem}___{frame_ind}.jpeg"
        output_label_dir = dst_frame_dir / src_video_filestem / label_folder_name
        output_label_dir.mkdir(parents=True, exist_ok=True)
        imageio.imwrite(output_label_dir / output_filename, frame_img)


def split_video_files_to_frame_files(src_video_dir: Path,
                                     excel_path: Path,
                                     dst_frame_dir: Path,
                                     label_config: Dict[str, Union[int, bool, str]]) -> None:
    """
    Copies frames in all .mjpg video files in a source directory into a new directory as .jpg files.
    :param src_video_dir: Path to directory where video files is stored
    :param excel_path: Path to excel file where file information is stored
    :param dst_frame_dir: Path to directory to store new data
    :param label_config: Label configuration
    """

    logging.info("Reading and formatting excel dataframe")
    excel_df_dict = read_excel.read_excel_to_dataframe(excel_file_path=excel_path)
    excel_df = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=excel_df_dict)

    logging.info("Reading video files and saving frames to destination")
    video_filepaths = src_video_dir.glob("*.mjpg")
    for video_filepath in tqdm.tqdm(list(video_filepaths)):
        frames_dict = split_video_file_to_frame_files(video_filepath=video_filepath,
                                                      excel_dataframe=excel_df,
                                                      label_config=label_config)

        save_frames(frames_dict=frames_dict,
                    src_video_filestem=video_filepath.stem,
                    label_name=label_config["name"],
                    dst_frame_dir=dst_frame_dir)
