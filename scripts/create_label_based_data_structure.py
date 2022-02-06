"""Script for creating a label based file structure for Weta Watcher data by copying video files from the raw file structure from Weta watcher.

Raw data from Weta Watcher is organized in a file structure based on sheet name
in the google sheet document.
"""
import argparse
import pathlib

from wai_data_tools.label_based_file_structure import (
    copy_files_to_label_based_file_structure,
)
from wai_data_tools.read_excel import (
    read_excel_to_dataframe,
    stack_rows_from_dataframe_dictionary,
)
from wai_data_tools.setup_logging import setup_logging


def create_label_based_file_structure(
    excel_file_path: pathlib.Path,
    raw_data_root_dir: pathlib.Path,
    dst_root_dir: pathlib.Path,
) -> None:
    """Copy the raw data .mjpg files from the Weta Watcher raw data file structure to a new file structure based on labels.

    Args:
        excel_file_path: Path to the excel file with label information
        raw_data_root_dir: Path to the root directory containing the raw Weta Watcher file structure.
        dst_root_dir: Path to the root directory destination to store the label based file structure.
    """
    content = read_excel_to_dataframe(excel_file_path=excel_file_path)
    dataframe = stack_rows_from_dataframe_dictionary(dataframe_dict=content)

    dst_root_dir.mkdir(exist_ok=True)

    copy_files_to_label_based_file_structure(
        file_dataframe=dataframe, src_dir=raw_data_root_dir, dst_dir=dst_root_dir
    )


def main() -> None:
    """Entrypoint."""
    setup_logging()

    parser = argparse.ArgumentParser("Create label based file structure")

    parser.add_argument(
        "excel_file_path",
        type=str,
        help="Path to the excel file with label information",
    )
    parser.add_argument(
        "raw_data_root_dir",
        type=str,
        help="Path to the root directory containing the raw Weta Watcher file structure",
    )
    parser.add_argument(
        "new_root_dir",
        type=str,
        help="Path to the new root directory to store the label based file structure",
    )

    args = parser.parse_args()

    excel_file_path = pathlib.Path(args.excel_file_path)
    raw_data_root_dir = pathlib.Path(args.raw_data_root_dir)
    dst_root_dir = pathlib.Path(args.new_root_dir)

    create_label_based_file_structure(
        excel_file_path=excel_file_path,
        raw_data_root_dir=raw_data_root_dir,
        dst_root_dir=dst_root_dir,
    )


if __name__ == "__main__":
    main()
