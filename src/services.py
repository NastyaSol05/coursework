from src.utils import filter_by_regex


def search_regex(data: list, search: str) -> list:
    """функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    new_data = filter_by_regex(data, search.lower())
    return new_data
