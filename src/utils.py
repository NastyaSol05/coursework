import json
import math
import os
import re
from typing import Any

import pandas as pd  # type: ignore

from src.logger import logger


def read_json(path: str) -> Any:
    """Функция, которая  принимает на вход путь до JSON-файла и возвращает список"""
    try:
        file = open(os.path.abspath(path), encoding="utf-8")
        logger.info("open json file")
    except IOError:
        logger.error("can't open json file")
        return []
    else:
        with file:
            logger.info("read json file")
            return json.load(file)


def read_file(filename: str) -> Any:
    """Читает xls файлы"""
    try:
        if os.path.splitext(filename)[1] == ".xls":
            df = pd.read_excel(filename)
            logger.info("read xls file")
            return df.to_dict("records")
    except FileNotFoundError:
        logger.error("can't open json file")
        print("File not found")


def read_file_as_pd(filename: str) -> pd.DataFrame:
    """Читает xls файлы"""
    try:
        if os.path.splitext(filename)[1] == ".xls":
            df = pd.read_excel(filename)
            logger.info("read xls file")
            return df
    except FileNotFoundError:
        logger.error("can't open json file")
        print("File not found")


def filter_by_regex(data: list, regex: str) -> list:
    """функция принимает список с банковскими операциях и строку поиска и возвращает список, где есть данная строка"""
    logger.info("function filter_by_regex started")
    list_regex = []
    pattern = re.compile(rf"\b{regex.lower()}\b")
    for i in data:
        if "Категория" in i and isinstance(i.get("Категория"), str) and re.search(pattern, i.get("Категория").lower()):
            list_regex.append(i)
            continue
        if "Описание" in i and isinstance(i.get("Описание"), str) and re.search(pattern, i.get("Описание").lower()):
            list_regex.append(i)
    return list_regex


def replace_nan(value: float) -> Any:
    """Функция заменяет NaN на None"""
    logger.info("function replace_nan started")
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def nan_to_none(data: list) -> list:
    """Функция заменяет все NaN в словаре на None"""
    logger.info("function nan_to_none started")
    return [{key: replace_nan(value) for key, value in item.items()} for item in data]


def list_to_json(data: list) -> str:
    """Функция конвертирует словать в json"""
    logger.info("function list_to_json started")
    data = nan_to_none(data)
    return json.dumps(data, ensure_ascii=False)
