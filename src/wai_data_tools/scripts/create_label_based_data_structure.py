"""Script for creating a label based file structure for Weta Watcher data by copying video files from the raw file structure from Weta watcher.

Raw data from Weta Watcher is organized in a file structure based on sheet name
in the google sheet document.
"""


import pathlib

import click

from wai_data_tools.label_based_file_structure import (
    copy_files_to_label_based_file_structure,
)
from wai_data_tools.read_excel import (
    read_excel_to_dataframe,
    stack_rows_from_dataframe_dictionary,
)
from wai_data_tools.setup_logging import setup_logging


def create_label_based_file_structure(
    excel_filepath: pathlib.Path,
    raw_data_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Copies the raw data .mjpg files from the Weta Watcher raw data file structure to a new file structure based on labels.

    Args:
      excel_filepath: Path to the excel file with label information
      raw_data_root_dir: Path to the root directory containing the raw Weta Watcher file structure.
      dst_root_dir: Path to the root directory destination to store the label based file structure.
      excel_filepath: pathlib.Path:
      raw_data_root_dir: pathlib.Path:
      dst_root_dir: pathlib.Path:
    """
    content = read_excel_to_dataframe(excel_file_path=excel_filepath)
    dataframe = stack_rows_from_dataframe_dictionary(dataframe_dict=content)

    copy_files_to_label_based_file_structure(
        file_dataframe=dataframe, src_dir=raw_data_root_dir, dst_dir=dst_root_dir
    )


@click.command()
@click.option(
    "--excel_filepath",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the excel file with label information",
)
@click.option(
    "--raw_data_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the root directory containing the raw Weta Watcher file structure.",
)
@click.option(
    "--dst_root_dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the root directory destination to store the label based file structure.",
)
def main(
    excel_filepath: pathlib.Path,
    raw_data_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Entrypoint."""
    setup_logging()
    create_label_based_file_structure(
        excel_filepath=excel_filepath,
        raw_data_root_dir=raw_data_root_dir,
        dst_root_dir=dst_root_dir,
    )


if __name__ == "__main__":
    main()
