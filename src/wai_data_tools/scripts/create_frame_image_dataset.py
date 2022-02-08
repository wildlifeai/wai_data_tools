"""
Script for constructing a image dataset by splitting the raw .mjpg video files for the Weta Watcher project
into .jpg frame images.
"""

import pathlib
import logging

import click

from wai_data_tools.setup_logging import setup_logging
from wai_data_tools import movie_to_images
from wai_data_tools import config


@click.command()
@click.option("--excel_filepath", type=pathlib.Path, help="Path to the excel file with label information")
@click.option("--config_filepath", type=pathlib.Path, help="Path to the configuration file")
@click.option("--src_video_dir", type=pathlib.Path, help="Path to the source directory containing video files")
@click.option("--dst_frame_dir", type=pathlib.Path, help="Path to the destination root directory to save frame images")
def create_frame_image_dataset(excel_filepath: pathlib.Path,
                               config_filepath: pathlib.Path,
                               src_video_dir: pathlib.Path,
                               dst_frame_dir: pathlib.Path) -> None:
    """
    Copies all frames for all .mjpg video files in a directory to a new directory and stores them as .jpg files.
    :param excel_filepath: Path to the excel file with label information
    :param config_filepath: Path to configuration file
    :param src_video_dir: Path to the source directory containing video file
    :param dst_frame_dir: Path to the destination root directory to save frame images
    :return:
    """

    dataset_config = config.load_config(config_filepath=config_filepath)
    label_config_list = dataset_config["labels"]
    for label_config in label_config_list:
        label_name = label_config["name"]
        logging.info("Processing video files for label %s", label_name)

        movie_to_images.split_video_files_to_frame_files(src_video_dir=src_video_dir / label_name,
                                                         excel_path=excel_filepath,
                                                         dst_frame_dir=dst_frame_dir,
                                                         label_config=label_config)


def main() -> None:
    setup_logging()
    create_frame_image_dataset()


if __name__ == "__main__":
    main()
