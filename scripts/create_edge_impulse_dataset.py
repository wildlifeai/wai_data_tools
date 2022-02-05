"""
Script for creating an image classification dataset for Edge Impulse from raw video dataset.
"""

import logging
import shutil
import argparse
import pathlib

from wai_data_tools.setup_logging import setup_logging

from scripts.create_label_based_data_structure import create_label_based_file_structure
from scripts.create_frame_image_dataset import create_frame_image_dataset
from scripts.preprocess_images import preprocess_images
from scripts.convert_to_upload_format import convert_file_structure_to_upload_format


def create_edge_impulse_dataset(excel_filepath: pathlib.Path,
                                config_filepath: pathlib.Path,
                                src_video_dir: pathlib.Path,
                                dst_root_dir: pathlib.Path) -> None:
    """
    Create image dataset for image classification in edge impulse from raw video files.
    :param excel_filepath: Path to the excel file with label information
    :param config_filepath: Path to configuration file
    :param src_video_dir: Path to the source directory containing video file
    :param dst_root_dir: Path to the destination root directory to store dataset and intermediate data
    """

    intermediate_video_dir = dst_root_dir / "inter-video"

    intermediate_video_dir.mkdir(exist_ok=True, parents=True)

    create_label_based_file_structure(excel_file_path=excel_filepath,
                                      raw_data_root_dir=src_video_dir,
                                      dst_root_dir=intermediate_video_dir)

    intermediate_frame_dir = dst_root_dir / "inter-frame"

    intermediate_frame_dir.mkdir(exist_ok=True, parents=True)

    create_frame_image_dataset(excel_filepath=excel_filepath,
                               config_filepath=config_filepath,
                               src_video_dir=intermediate_video_dir,
                               dst_frame_dir=intermediate_frame_dir)

    logging.info("Removing intermediate video data")
    shutil.rmtree(intermediate_video_dir)

    preprocess_images(config_filepath=config_filepath,
                      src_root_dir=intermediate_frame_dir,
                      dst_root_dir=intermediate_frame_dir)

    convert_file_structure_to_upload_format(src_root_dir=intermediate_frame_dir,
                                            dst_root_dir=dst_root_dir)

    logging.info("Removing intermediate frame data")
    shutil.rmtree(intermediate_frame_dir)


def main():
    setup_logging()

    parser = argparse.ArgumentParser("Create image dataset for image classification in edge impulse from raw "
                                     "video files.")

    parser.add_argument('excel_filepath', type=str,
                        help='Path to the excel file with label information')
    parser.add_argument('config_filepath', type=str,
                        help='Path to the configuration file')
    parser.add_argument('src_video_dir', type=str,
                        help='Path to the source directory containing video files')
    parser.add_argument('dst_root_dir', type=str,
                        help='Path to the destination root directory to store dataset and intermediate data')

    args = parser.parse_args()

    excel_filepath = pathlib.Path(args.excel_filepath)
    config_filepath = pathlib.Path(args.config_filepath)
    src_video_dir = pathlib.Path(args.src_video_dir)
    dst_root_dir = pathlib.Path(args.dst_root_dir)

    create_edge_impulse_dataset(excel_filepath=excel_filepath,
                                config_filepath=config_filepath,
                                src_video_dir=src_video_dir,
                                dst_root_dir=dst_root_dir)


if __name__ == "__main__":
    main()
