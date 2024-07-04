from typing import Any, Callable, Union

from src.logger import logger


def report_to_file(filename: Union[str, None] = None) -> Callable:
    """Внутренняя функция, которая записывает результат функции в файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            output_file = filename if filename else "report.json"
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(result)
                logger.info(f"Report saved to {output_file}")
            except Exception as e:
                logger.error(f"Report cant saved to {output_file}")
                print(e)

            return result

        return wrapper

    return decorator
