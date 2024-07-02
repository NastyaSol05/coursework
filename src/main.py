from datetime import datetime

from src.reports import spending_by_category
from src.services import search_regex
from src.utils import read_file, read_file_as_pd
from src.views import main_page

data_pd = read_file_as_pd("../data/operations.xls")
data = read_file("../data/operations.xls")


def main() -> None:
    date = datetime.now()
    print("Выполнение задания Веб-сервисы - Главная\n")
    print(main_page(date))
    print("Выполнение задания Сервисы - Простой поиск\n")
    print(search_regex(data, "Супермаркеты"))
    print("Выполнение задания Отчеты - Траты по категории\n")
    print(spending_by_category(data_pd, "Супермаркеты", "31.01.2021"))


if __name__ == "__main__":
    main()
