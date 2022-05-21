"""Script for creating an image classification dataset for Edge Impulse from raw video dataset."""


import logging
import pathlib
import shutil

from wai_data_tools.scripts.convert_to_upload_format import (
    convert_file_structure_to_upload_format,
)
from wai_data_tools.scripts.create_frame_image_dataset import create_frame_image_dataset
from wai_data_tools.scripts.preprocess_images import preprocess_images


def create_edge_impulse_dataset(
    excel_file: pathlib.Path,
    config_file: pathlib.Path,
    src_video_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Create image dataset for image classification in edge impulse from raw video files.

    Args:
        excel_file: Path to the excel file with label information
        config_file: Path to configuration file
        src_video_dir: Path to the source directory containing video files
        dst_root_dir: Path to the destination root directory to store dataset and intermediate data
    """
    logger = logging.getLogger(__name__)

    logger.info("Creating Edge Impulse dataset")

    intermediate_frame_dir = dst_root_dir / "inter-frame"

    intermediate_frame_dir.mkdir(exist_ok=True, parents=True)

    create_frame_image_dataset(
        excel_file=excel_file,
        config_file=config_file,
        src_video_dir=src_video_dir,
        dst_frame_dir=intermediate_frame_dir,
    )

    preprocess_images(
        config_file=config_file,
        src_root_dir=intermediate_frame_dir,
        dst_root_dir=intermediate_frame_dir,
    )

    convert_file_structure_to_upload_format(
        src_root_dir=intermediate_frame_dir, dst_root_dir=dst_root_dir, config_file=config_file
    )

    logger.info("Removing intermediate frame data")
    shutil.rmtree(intermediate_frame_dir)
