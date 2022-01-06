
import logging
from pathlib import Path
from typing import Dict, Union

import pandas as pd


def read_excel_to_dataframe(excel_file_path: Path) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an excel file to a pandas dataframe.
    :param excel_file_path: Path to excel file path
    :return: content of excel file stored in pandas DataFrame
    """

    logging.info("Reading excel datafile %s to dataframe", excel_file_path.name)
    return pd.read_excel(excel_file_path, sheet_name=None)


def stack_rows_from_dataframe_dictionary(dataframe_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Stacks the rows from dataframes in a dictionary to one single dataframe.
    The dictionary key will be added as an extra row to the dataframe.
    Typically used for the content from excel/google sheets documents with multiple sheets.
    :param dataframe_dict: Dictionary with dataframes.
    :return: Dataframe with rows stacked from all dataframes in dictionary
    """

    logging.info("Merging all rows from dataframes in dictionary to one dataframe")
    merged_dataframe = pd.DataFrame()
    for sheet_name, sheet_content in dataframe_dict.items():
        # Column for the sheet the data was in the file is added for traceability
        sheet_content["folder"] = sheet_name
        merged_dataframe = merged_dataframe.append(sheet_content)
    return merged_dataframe


