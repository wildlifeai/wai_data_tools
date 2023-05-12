"""Tests for read_excel module."""
from typing import Dict

import pandas as pd
import pytest

from wai_data_tools.utils import read_excel


@pytest.mark.parametrize(
    argnames="dataframe_dict",
    argvalues=[
        {
            "sheet_1": pd.DataFrame({"col_1": [1, 2], "col_2": [1, 2]}),
        },
        {
            "sheet_1": pd.DataFrame({"col_1": [1, 2], "col_2": [1, 2]}),
            "sheet_2": pd.DataFrame({"col_1": [3, 4], "col_2": [3, 4]}),
        },
        {
            "sheet_1": pd.DataFrame({"col_1": [1, 2], "col_2": [1, 2]}),
            "sheet_2": pd.DataFrame({"col_1": [3, 4], "col_2": [3, 4]}),
            "sheet_3": pd.DataFrame({"col_1": [1, 2], "col_2": [5, 6]}),
        },
    ],
)
def test_stack_rows_from_dataframe_dictionary(dataframe_dict: Dict[str, pd.DataFrame]) -> None:
    """Test case for stack_rows_from_dataframe_dictionary.

    Args:
        dataframe_dict: Dictionary with dataframes. Key is sheet name and value is dataframe for sheet.
    """
    result_dataframe = read_excel.stack_rows_from_dataframe_dictionary(dataframe_dict=dataframe_dict)

    assert sorted(result_dataframe["folder"].unique()) == sorted(list(dataframe_dict.keys()))
    expected_n_rows = sum([len(sheet_df) for sheet_df in dataframe_dict.values()])
    assert len(result_dataframe) == expected_n_rows
