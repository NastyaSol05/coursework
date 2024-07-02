import json
import os
from datetime import datetime
from typing import Any

import pandas as pd  # type: ignore
import requests  # type: ignore
import yfinance as yf  # type: ignore
from dotenv import load_dotenv

from src.logger import logger
from src.utils import read_file, read_json

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_greeting(datetime: datetime) -> str:
    """Получение приветсвенного сообщения"""
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def process_transactions(transactions: pd.DataFrame) -> Any:
    """Получение общей суммы расходов по каждой карте с кешбэком"""
    card_map = {}
    for transaction in transactions:
        card_number = transaction["Номер карты"]
        if not pd.isna(card_number):
            last_digits = card_number[-4:]
            if last_digits not in card_map:
                card_map[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}

            amount = transaction["Сумма операции"]

            card_map[last_digits]["total_spent"] += amount * -1
            card_map[last_digits]["cashback"] = card_map[last_digits]["total_spent"] / 100

    result = []
    for key, value in card_map.items():
        formatted_output = {
            "last_digits": key,
            "total_spent": round(value["total_spent"], 2),
            "cashback": round(value["cashback"], 2),
        }
        result.append(formatted_output)
    return result


def top_transactions(transactions: pd.DataFrame) -> list:
    """Топ-5 транзакций по сумме платежа"""
    sorted_transactions = sorted(transactions, key=lambda x: x["Сумма платежа"], reverse=True)[:5]

    top_transactions_list = []
    for transaction in sorted_transactions:
        top_transaction = {
            "date": transaction["Дата платежа"],
            "amount": round(abs(transaction["Сумма платежа"]), 2),
            "category": transaction["Категория"],
            "description": transaction["Описание"],
        }
        top_transactions_list.append(top_transaction)

    return top_transactions_list


def exchange_rates() -> list:
    """Получение курса валют из файла настроек"""
    settings = read_json("../user_settings.json").get("user_currencies")
    exchange_rates = []
    for currency in settings:
        url = f"https://api.apilayer.com/currency_data/convert?to=RUB&from={currency}&amount=1"

        payload: dict = {}
        headers: dict = {"apikey": API_KEY}

        response = requests.get(url, headers=headers, data=payload)

        if response.ok:
            logger.info("response received")
            result = response.json()
            exchange_rate = {"currency": currency, "rate": round(result.get("result"), 2)}
            exchange_rates.append(exchange_rate)
        else:
            logger.error("can't get operation amount")
            return []
    return exchange_rates


def sp500() -> list:
    """Получение S&P500 из файла настроек"""
    stock_prices = []
    sp500_tickers = read_json("../user_settings.json").get("user_stocks")
    for ticker in sp500_tickers:
        try:
            # Получаем данные о цене акции
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")

            if len(history) == 0:
                print(f"No data available for {ticker}")
                continue

            current_price = round(float(history["Close"].iloc[0]), 2)
            stock_price = {"stock": ticker, "price": current_price}
            stock_prices.append(stock_price)
        except Exception as e:
            print(f"Error retrieving data for {ticker}: {e}")

    return stock_prices


def main_page(date: datetime) -> str:
    data = read_file("../data/operations.xls")
    greeting = get_greeting(date)
    card_summary = process_transactions(data)
    top_5_transactions = top_transactions(data)
    exchange_rate = exchange_rates()
    sp = sp500()

    return json.dumps(
        [
            {"greeting": greeting},
            {"cards": card_summary},
            {"top_transactions": top_5_transactions},
            {"currency_rates": exchange_rate},
            {"stock_prices": sp},
        ],
        ensure_ascii=False,
    )
