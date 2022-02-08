"""
Script for creating a label based file structure for Weta Watcher data by copying video files from the raw file
structure from Weta watcher. Raw data from Weta Watcher is organized in a file structure based on sheet name
in the google sheet document.
"""

import pathlib

import click

from wai_data_tools.setup_logging import setup_logging

from wai_data_tools.read_excel import (
    read_excel_to_dataframe,
    stack_rows_from_dataframe_dictionary
)
from wai_data_tools.label_based_file_structure import copy_files_to_label_based_file_structure


@click.command()
@click.option("--excel_filepath", type=pathlib.Path, help="Path to the excel file with label information")
@click.option("--raw_data_root_dir",
              type=pathlib.Path,
              help="Path to the root directory containing the raw Weta Watcher file structure.")
@click.option("--dst_root_dir",
              type=pathlib.Path,
              help="Path to the root directory destination to store the label based file structure.")
def create_label_based_file_structure(excel_file_path: pathlib.Path,
                                      raw_data_root_dir: pathlib.Path,
                                      dst_root_dir: pathlib.Path) -> None:
    """
    Copies the raw data .mjpg files from the Weta Watcher raw data file structure
    to a new file structure based on labels.
    :param excel_file_path: Path to the excel file with label information
    :param raw_data_root_dir: Path to the root directory containing the raw Weta Watcher file structure.
    :param dst_root_dir: Path to the root directory destination to store the label based file structure.
    """

    content = read_excel_to_dataframe(excel_file_path=excel_file_path)
    dataframe = stack_rows_from_dataframe_dictionary(dataframe_dict=content)

    dst_root_dir.mkdir(exist_ok=True)

    copy_files_to_label_based_file_structure(file_dataframe=dataframe, src_dir=raw_data_root_dir, dst_dir=dst_root_dir)


def main() -> None:
    setup_logging()
    create_label_based_file_structure()


if __name__ == "__main__":
    main()
