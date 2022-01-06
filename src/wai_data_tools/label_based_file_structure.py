import logging
import shutil
from pathlib import Path

import pandas as pd


def copy_files_to_label_folder(file_dataframe: pd.DataFrame, src_dir: Path, dst_dir: Path) -> None:
    """
    Copies files into label based file structure.
    :param file_dataframe: Dataframe with information about file locations and assigned labels
    :param src_dir: Root directory where raw data is stored, should contain the WW01, WW02, ... folders.
    :param dst_dir: Root directory for label based file structure
    """

    logging.info("Setting up label based folder structure at %s", dst_dir)

    labels = file_dataframe["label"].unique()
    for label in labels:
        label_dir = dst_dir / label
        label_dir.mkdir(exist_ok=True)

    for ind, df_row in file_dataframe.iterrows():
        filename = df_row["filename"]
        folder = df_row["folder"]
        label = df_row["label"]

        src = src_dir / folder / filename
        dst = dst_dir / label / filename
        shutil.copy(str(src), str(dst))
