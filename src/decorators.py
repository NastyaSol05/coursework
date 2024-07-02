from typing import Any, Callable, Union

from src.logger import logger


def report_to_file(filename: Union[str, None] = None) -> Callable:
    """Внутренняя функция, которая записывает результат функции в файл"""

    def decorator(func: Callable) -> Callable:
        # @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            output_file = filename if filename else "report.csv"
            try:
                if output_file.split(".")[1] == "csv":
                    result.to_csv(output_file, encoding="utf-8")
                elif output_file.split(".")[1] == "xlsx":
                    result.to_excel(output_file)
                else:
                    result.to_string(output_file)
                logger.info(f"Report saved to {output_file}")
            except Exception as e:
                logger.error(f"Report cant saved to {output_file}")
                print(e)

            return result

        return wrapper

    return decorator
