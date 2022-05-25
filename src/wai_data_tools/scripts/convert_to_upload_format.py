"""Script for converting file structure to a format that is easier to upload to edge impulse."""
import logging
import pathlib
import shutil

import pandas as pd
import tqdm

from wai_data_tools import config
from wai_data_tools.data import calc_test_split_indices


def convert_file_structure_to_upload_format(
    src_root_dir: pathlib.Path, dst_root_dir: pathlib.Path, config_filepath: pathlib.Path
) -> None:
    """Copy contents of a source file structure and stores it in a destination directoryin upload friendly format.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file structure.
        config_filepath: Path to config file.
    """
    logger = logging.getLogger(__name__)

    logger.info("Reading frame information")
    df_frames = pd.read_csv(src_root_dir / "frame_information.csv")
    src_dataset_dir = src_root_dir / "dataset"

    logger.info("Reading config")
    config_dict = config.load_config(config_filepath=config_filepath)

    test_split_size = config_dict["data_split"]["test_size"]

    logger.info("Creating new file structure for uploading to Edge Impulse")

    video_names = df_frames["video_name"].unique()

    test_file_inds = calc_test_split_indices(n_files=len(video_names), test_split_size=test_split_size)

    test_video_names = video_names[test_file_inds]

    for _, frame_row in tqdm.tqdm(list(df_frames.iterrows())):

        target_name = frame_row["target"]
        video_name = frame_row["video_name"]

        if video_name in test_video_names:
            split_dir = "test"
        else:
            split_dir = "train"

        dst_target_dir = dst_root_dir / split_dir
        dst_target_dir.mkdir(exist_ok=True, parents=True)

        src_frame_filename = frame_row["file_name"]
        dst_frame_filename = f"{target_name}.{src_frame_filename}"

        src_frame_filepath = src_dataset_dir / video_name / src_frame_filename

        dst_frame_filepath = dst_target_dir / dst_frame_filename

        shutil.copy(str(src_frame_filepath), str(dst_frame_filepath))
