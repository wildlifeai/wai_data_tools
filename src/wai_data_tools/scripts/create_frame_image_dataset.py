"""Script for constructing a image dataset by splitting the raw .mjpg video files for the Weta Watcher project into .jpg frame images."""

import logging
import pathlib

import click

from wai_data_tools import config, movie_to_images
from wai_data_tools.setup_logging import setup_logging


def create_frame_image_dataset(
    excel_filepath: pathlib.Path,
    config_filepath: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Copy all frames for all .mjpg video files in a directory to a new directory and stores them as .jpg files.

    Args:
      excel_filepath: Path to the excel file with label information
      config_filepath: Path to configuration file
      src_video_dir: Path to the source directory containing video files
      dst_frame_dir: Path to the destination root directory to save frame images
    """
    dataset_config = config.load_config(config_filepath=config_filepath)
    label_config_list = dataset_config["labels"]
    for label_config in label_config_list:
        label_name = label_config["name"]
        logging.info("Processing video files for label %s", label_name)

        movie_to_images.split_video_files_to_frame_files(
            src_video_dir=src_video_dir / label_name,
            excel_path=excel_filepath,
            dst_frame_dir=dst_frame_dir,
            label_config=label_config,
        )


@click.command()
@click.option(
    "--excel_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
)
@click.option(
    "--config_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the configuration file",
)
@click.option(
    "--src_video_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the source directory containing video files",
)
@click.option(
    "--dst_frame_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the destination root directory to save frame images",
)
def main(
    excel_filepath: pathlib.Path,
    config_filepath: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_frame_dir: pathlib.Path,
) -> None:
    """Entrypoint."""
    setup_logging()
    create_frame_image_dataset(
        excel_filepath=excel_filepath,
        config_filepath=config_filepath,
        src_video_dir=src_video_dir,
        dst_frame_dir=dst_frame_dir,
    )


if __name__ == "__main__":
    main()
