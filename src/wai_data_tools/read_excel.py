
import logging
from pathlib import Path
from typing import Dict, Union
import shutil

import pandas as pd

import setup_logging


def read_excel_to_dataframe(excel_file_path: Path) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an excel file to a pandas dataframe.
    :param excel_file_path: Path to excel file path
    :return: content of excel file stored in pandas DataFrame
    """

    logging.info("Reading excel datafile %s to dataframe", excel_file_path.name)
    return pd.read_excel(excel_file_path, sheet_name=None)


def append_rows_from_dataframe_dictionary(dataframe_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Appends the rows from all entries in a dictionary of dataframes to one dataframe.
    :param dataframe_dict: Dictionary with dataframes, most likely from reading an excel document with multiple sheets.
    :return: Dataframe with content from all entries in dictionary
    """

    logging.info("Merging all rows from dataframes in dictionary to one dataframe")
    merged_dataframe = pd.DataFrame()
    for sheet_name, sheet_content in dataframe_dict.items():
        # Column for the sheet the data was in the file is added for traceability
        sheet_content["folder"] = sheet_name
        merged_dataframe = merged_dataframe.append(sheet_content)
    return merged_dataframe


def copy_files_to_label_folder(file_dataframe: pd.DataFrame, data_dir: Path, base_dir: Path):
    """
    Copies data files into folders based on the object label.
    :param file_dataframe: Dataframe with information about data files
    :param data_dir: Directory where data is stored, should contain the WW01, WW02, ... folders.
    :param base_dir: Directory to store the new label folders
    """

    logging.info("Setting up label based folder structure at %s", base_dir)

    labels = file_dataframe["label"].unique()
    for label in labels:
        label_dir = base_dir / label
        label_dir.mkdir(exist_ok=True)

    for ind, df_row in file_dataframe.iterrows():
        filename = df_row["filename"]
        folder = df_row["folder"]
        label = df_row["label"]

        src = data_dir / folder / filename
        dst = base_dir / label / filename
        shutil.copy(str(src), str(dst))


def filter_raw_data_to_label_folders(excel_file_path: Path,
                                     raw_data_dir: Path,
                                     new_data_dir: Path):
    """
    Filters the raw data .mjpg files from the WW0X folders to a new folder structure based on labels.
    :param excel_file_path: Path to the excel file with label information
    :param raw_data_dir: Path to the directory containing the WW0X folders.
    :param new_data_dir: Directory to place the label folders
    """

    content = read_excel_to_dataframe(excel_file_path=excel_file_path)
    dataframe = append_rows_from_dataframe_dictionary(dataframe_dict=content)

    copy_files_to_label_folder(file_dataframe=dataframe, data_dir=raw_data_dir, base_dir=new_data_dir)


def main():
    setup_logging.setup_logging()
    pass


if __name__ == "__main__":
    main()
