
from pathlib import Path
from typing import Dict, Union

import pandas as pd
import matplotlib.pyplot as plt


def read_excel_to_dataframe(excel_file_path: Path) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Reads an excel file to a pandas dataframe.
    :param excel_file_path: Path to excel file path
    :return: content of excel file stored in pandas DataFrame
    """

    return pd.read_excel(excel_file_path, sheet_name=None)


def append_rows_from_dataframe_dictionary(dataframe_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Appends the rows from all entries in a dictionary of dataframes to one dataframe.
    :param dataframe_dict: Dictionary with dataframes, most likely from reading an excel document with multiple sheets.
    :return: Dataframe with content from all entries in dictionary
    """

    merged_dataframe = pd.DataFrame()
    for sheet_name, sheet_content in dataframe_dict.items():
        sheet_content["folder"] = sheet_name
        merged_dataframe = merged_dataframe.append(sheet_content)
    return merged_dataframe


excel_file_path = Path(r"C:\Users\david\Desktop\wildlife.ai\ww_labels.xlsx")

content = read_excel_to_dataframe(excel_file_path=excel_file_path)
dataframe = append_rows_from_dataframe_dictionary(dataframe_dict=content)

# remove nothing label
filtered_df = dataframe[dataframe["label"] != "nothing"]

filtered_df["label"].value_counts().plot(kind="barh")
plt.show()
