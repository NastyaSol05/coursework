from src.utils import filter_by_regex, list_to_json


def search_regex(data: list, search: str) -> str:
    """функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    new_data = filter_by_regex(data, search.lower())
    return list_to_json(new_data)
