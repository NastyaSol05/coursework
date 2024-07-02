from datetime import datetime
from typing import Optional

import pandas as pd  # type: ignore

from src.decorators import report_to_file


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца"""
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

    if date is None:
        date_timestamp = datetime.now()
    else:
        date_timestamp = pd.to_datetime(date, dayfirst=True)

    three_months_ago = date_timestamp - pd.DateOffset(months=3)
    filtered_df = transactions[
        (transactions["Дата платежа"] >= three_months_ago)
        & (transactions["Дата платежа"] <= date_timestamp)
        & (transactions["Категория"] == category)
    ]
    return filtered_df
