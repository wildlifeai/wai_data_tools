"""This module is an entrypoint."""
import logging
import shutil
from pathlib import Path

import pandas as pd
import tqdm


def copy_files_to_label_based_file_structure(
    file_dataframe: pd.DataFrame, src_dir: Path, dst_dir: Path
) -> None:
    """Copy files to label based file structure.

    Args:
        file_dataframe: Dataframe with information about file locations
            and assigned labels
        src_dir: Root directory where raw data is stored, should contain
            the WW01, WW02, ... folders.
        dst_dir: Root directory for label based file structure
    """
    logging.info("Setting up label based folder structure at %s...", dst_dir)

    labels = file_dataframe["label"].unique()
    for label in labels:
        label_dir = dst_dir / label
        label_dir.mkdir(exist_ok=True, parents=True)

    logging.info("Copying data files to new file structure...")

    for ind, df_row in tqdm.tqdm(list(file_dataframe.iterrows())):
        filename = df_row["filename"]
        folder = df_row["folder"]
        label = df_row["label"]

        src = src_dir / folder / filename
        dst = dst_dir / label / filename
        shutil.copy(str(src), str(dst))
