import json
from datetime import datetime
from typing import Any, Optional

import pandas as pd  # type: ignore

from src.decorators import report_to_file
from src.utils import nan_to_none


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Any:
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
    return json.dumps(
        nan_to_none(filtered_df.to_dict(orient="records")),
        default=lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, datetime) else x,
        ensure_ascii=False,
    )
