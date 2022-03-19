"""Script for creating label based file structure.

Script for creating a label based file structure for Weta Watcher data by copying video files
from the raw file structure from Weta watcher. Raw data from Weta Watcher is organized in a file
structure based on sheet name in the google sheet document.
"""


import logging
import pathlib
import shutil

import pandas as pd
import tqdm


def create_label_based_file_structure(
    src_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Copy the raw data .mjpg files from raw data file structure to a new file structure based on labels.

    Args:
        src_root_dir: Path to the root directory for frame dataset.
        dst_root_dir: Path to the root directory destination to store the label based file structure.
    """
    df_frames = pd.read_csv(src_root_dir / "frame_information.csv")
    dataset_dir = src_root_dir / "dataset"

    logging.info("Setting up label based folder structure at %s...", dst_root_dir)

    labels = df_frames["label"].unique()
    for label in labels:
        label_dir = dst_root_dir / label
        label_dir.mkdir(exist_ok=True, parents=True)

    logging.info("Copying data files to new file structure...")

    for _, df_row in tqdm.tqdm(list(df_frames.iterrows())):
        video_name = df_row["video_name"]
        file_name = df_row["file_name"]
        label = df_row["label"]

        src = dataset_dir / video_name / file_name
        dst = dst_root_dir / label / file_name
        shutil.copy(str(src), str(dst))
