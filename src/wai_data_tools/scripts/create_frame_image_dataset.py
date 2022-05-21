"""Script for constructing a image dataset by splitting the raw video files into frame images."""

import logging
import pathlib

import pandas as pd

from wai_data_tools import config, movie_to_images, read_excel


def create_frame_image_dataset(
    excel_file: pathlib.Path,
    config_file: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Copy all frames for all .mjpg video files in a directory to a new directory and stores them as jpg files.

    Args:
        excel_file: Path to the excel file with label information
        config_file: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_frame_dir: Path to the destination root directory to save frame images
    """
    logger = logging.getLogger(__name__)

    logger.info("Reading and formatting excel dataframe")
    content = read_excel.read_excel_to_dataframe(excel_file=excel_file)
    dataframe = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=content)

    dataset_config = config.load_config(config_file=config_file)
    label_config_list = dataset_config["labels"]
    frame_df = None
    for label_config in label_config_list:
        label_name = label_config["name"]
        logger.info("Processing video files for label %s", label_name)

        label_frame_df = movie_to_images.split_video_files_to_frame_files(
            src_video_dir=src_video_dir,
            video_dataframe=dataframe,
            dst_frame_dir=dst_frame_dir / "dataset",
            label_config=label_config,
        )

        if frame_df is not None:
            frame_df = pd.concat([frame_df, label_frame_df], ignore_index=True)
        else:
            frame_df = label_frame_df

    frame_df.to_csv(dst_frame_dir / "frame_information.csv")
