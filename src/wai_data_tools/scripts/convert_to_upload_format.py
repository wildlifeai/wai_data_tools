"""Script for converting file structure to a format that is easier to upload to edge impulse."""
import logging
import pathlib
import shutil

import pandas as pd
import tqdm


def convert_file_structure_to_upload_format(src_root_dir: pathlib.Path, dst_root_dir: pathlib.Path) -> None:
    """Copy contents of a source file structure and stores it in a destination directoryin upload friendly format.

    Args:
        src_root_dir: Source root directory to read files from.
        dst_root_dir: Destination root directory to store new file structure.
    """
    df_frames = pd.read_csv(src_root_dir / "frame_information.csv")
    src_dataset_dir = src_root_dir / "dataset"

    logging.info("Creating new file structure for uploading to Edge Impulse")

    for _, frame_row in tqdm.tqdm(list(df_frames.iterrows())):

        target_name = frame_row["contains_target"]

        dst_target_dir = dst_root_dir / target_name
        dst_target_dir.mkdir(exist_ok=True, parents=True)

        video_name = frame_row["filename"].split(".")[0]

        frame_filename = f"{video_name}___{frame_row['frame_ind']}.jpeg"

        src_frame_filepath = src_dataset_dir / video_name / frame_filename

        dst_frame_filepath = dst_target_dir / frame_filename

        shutil.copy(str(src_frame_filepath), str(dst_frame_filepath))
