from typing import Any
from unittest.mock import patch

import pandas as pd  # type: ignore

from src.decorators import report_to_file


@report_to_file("report.csv")
def generate_report() -> pd.DataFrame:
    data = {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
    df = pd.DataFrame(data)
    return df


@patch("pandas.DataFrame.to_csv")
@patch("pandas.DataFrame.to_excel")
@patch("pandas.DataFrame.to_string")
def test_report_to_file(mock_to_string: Any, mock_to_excel: Any, mock_to_csv: Any) -> None:
    # Тест для CSV
    generate_report()
    mock_to_csv.assert_called_once_with("report.csv", encoding="utf-8")

    # Тест для XLSX
    generate_report_with_xlsx = report_to_file("report.xlsx")(generate_report)
    generate_report_with_xlsx()
    mock_to_excel.assert_called_once_with("report.xlsx")

    # Тест для другого формата
    generate_report_with_txt = report_to_file("report.txt")(generate_report)
    generate_report_with_txt()
    mock_to_string.assert_called_once_with("report.txt")
