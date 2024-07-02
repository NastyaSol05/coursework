import json
import math
import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd  # type: ignore
import pytest

from src.utils import filter_by_regex, list_to_json, nan_to_none, read_file, read_file_as_pd, read_json, replace_nan


def test_read_json() -> None:
    """Тест функции loads_json"""

    mock_json_data = {"ключ1": "поддельное значение1", "ключ2": "поддельное значение2"}

    mock_open = unittest.mock.mock_open(read_data=json.dumps(mock_json_data))

    with unittest.mock.patch("builtins.open", mock_open), unittest.mock.patch("os.stat") as mock_stat:
        mock_stat.return_value.st_size = 2

        data = read_json("data.json")

    assert data == mock_json_data


@patch("pandas.read_excel")
def test_read_xlsx(read_xlsx: Any) -> None:
    read_xlsx.return_value = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    result_xlsx = read_file("data.xls")
    expected_result = [{"col1": 1, "col2": 4}, {"col1": 2, "col2": 5}, {"col1": 3, "col2": 6}]
    assert result_xlsx == expected_result


@patch("pandas.read_excel")
def test_read_file_as_pd(read_xlsx: Any) -> None:
    read_xlsx.return_value = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    result_xlsx = read_file_as_pd("data.xls")
    expected_result = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    assert result_xlsx.equals(expected_result)


@pytest.mark.parametrize(
    "regex, expected",
    [
        (
            "Переводы",
            [{"Категория": "Переводы", "Описание": "Константин Л."}, {"Категория": "Переводы", "Описание": "Петр П."}],
        ),
        ("Магазин", [{"Категория": "Покупки", "Описание": "Магазин"}]),
        ("123", []),
    ],
)
def test_filter_by_regex(regex: str, expected: str) -> None:
    data = [
        {"Категория": "Переводы", "Описание": "Константин Л."},
        {"Категория": "Покупки", "Описание": "Магазин"},
        {"Категория": "Переводы", "Описание": "Петр П."},
        {"Категория": "Константин", "Описание": "Авиабилет"},
    ]
    assert filter_by_regex(data, regex) == expected


def test_replace_nan() -> None:
    assert replace_nan(float("nan")) is None


def test_nan_to_none() -> None:
    data = [{"key1": math.nan}]
    expected = [{"key1": None}]
    assert nan_to_none(data) == expected


def test_list_to_json() -> None:
    """Тест функции loads_json"""

    data = [{"ключ1": math.nan, "ключ2": "поддельное значение2"}]
    expected = '[{"ключ1": null, "ключ2": "поддельное значение2"}]'
    '[{"ключ1": null, "ключ2": "поддельное значение2"}]'
    assert list_to_json(data) == expected
