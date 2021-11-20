
import logging
from pathlib import Path
from typing import Any, Tuple, List

import imageio
import numpy as np
import pandas as pd

import setup_logging
import read_excel


def get_video_reader(video_filepath: Path) -> Any:
    """
    Gets a imageio reader object for the provided video file. Assumes ffmpeg encoding.
    :param video_filepath: Path to ffmpeg compatible video file
    :return: reader object for parsing video
    """
    return imageio.get_reader(video_filepath, 'ffmpeg')


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


def filter_images_in_video(video_reader: Any,
                           frames_with_label: np.ndarray) -> Tuple[List[Tuple[int, np.ndarray]],
                                                                   List[Tuple[int, np.ndarray]]]:
    """
    Filters the images in a video based on frames with label and frames without it.
    :param video_reader: imageio reader for the video you want to filter.
    :param frames_with_label: array with frame indices for frames that contain the label.
    :return: a list with indices and images for frames with label and a list with indices
             and images for frames that don't contain the label.
    """

    logging.info("Filtering frames in video to label and non label frames")
    label_list = []
    no_label_list = []
    for frame_ind, frame_img in enumerate(video_reader):
        if frame_ind in frames_with_label:
            label_list.append((frame_ind, frame_img))
        else:
            no_label_list.append((frame_ind, frame_img))
    return label_list, no_label_list


def split_video_file_to_frame_files(video_filepath: Path,
                                    excel_dataframe: pd.DataFrame,
                                    new_dir: Path):
    """
    Splits a video file into separate frames and saves them as .jpeg files
    :param video_filepath: Path to .mjpg video file
    :param excel_dataframe: Dataframe with file information
    :param new_dir: Path to directory to store new data
    """

    logging.info("Splitting video file to frame files...")

    reader = get_video_reader(video_filepath=video_filepath)
    meta = reader.get_meta_data()

    video_row = excel_dataframe[excel_dataframe["filename"] == video_filepath.name]
    if video_row.shape[0] > 1:
        raise ValueError("More than 1 entry found that matches the query in the dataframe")

    label_frames = calculate_frames_in_timespan(t_start=video_row["start"].values,
                                                t_end=video_row["end"].values,
                                                fps=meta["fps"])

    label_list, no_label_list = filter_images_in_video(video_reader=reader, frames_with_label=label_frames)

    logging.info("Saving label frames")
    for frame_ind, frame_img in label_list:
        output_filename = f"{video_filepath.stem}___{frame_ind}.jpeg"
        output_label_dir = new_dir / video_filepath.stem / "label"
        output_label_dir.mkdir(parents=True, exist_ok=True)
        imageio.imwrite(output_label_dir / output_filename, frame_img)

    logging.info("Saving non label frames")
    for frame_ind, frame_img in no_label_list:
        output_filename = f"{video_filepath.stem}___{frame_ind}.jpeg"
        output_label_dir = new_dir / video_filepath.stem / "no_label"
        output_label_dir.mkdir(parents=True, exist_ok=True)
        imageio.imwrite(output_label_dir / output_filename, frame_img)


def split_video_files_to_frame_files(video_dir: Path,
                                     excel_path: Path,
                                     new_dir: Path,
                                     label: str):
    """
    Splits video files into .jpeg files for each frame
    :param video_dir: Path to directory where video files is stored
    :param excel_path: Path to excel file where file information is stored
    :param new_dir: Path to directory to store new data
    :param label: Label to use when filtering the dataframe
    """

    logging.info("Reading and formatting excel dataframe")
    excel_df_dict = read_excel.read_excel_to_dataframe(excel_file_path=excel_path)
    excel_df = read_excel.append_rows_from_dataframe_dictionary(dataframe_dict=excel_df_dict)

    logging.info("Filtering dataframe based on label %s", label)
    single_label_df = excel_df[excel_df["label"] == label]

    video_filepaths = video_dir.glob("*.mjpg")
    for video_filepath in video_filepaths:
        logging.info("Now processing file %s", video_filepath.name)
        split_video_file_to_frame_files(video_filepath=video_filepath,
                                        excel_dataframe=single_label_df,
                                        new_dir=new_dir)


def main():
    setup_logging.setup_logging()
    new_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\curated-datasets\rat")
    excel_path = Path(r"C:\Users\david\Desktop\wildlife.ai\raw-data\ww_labels.xlsx")
    video_dir = Path(r"C:\Users\david\Desktop\wildlife.ai\raw-data-label-sorted\rat")

    split_video_files_to_frame_files(video_dir=video_dir,
                                     excel_path=excel_path,
                                     new_dir=new_dir,
                                     label="rat")


if __name__ == "__main__":
    main()
