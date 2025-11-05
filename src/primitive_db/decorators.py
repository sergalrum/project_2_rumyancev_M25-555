import time
from functools import wraps


def handle_db_errors(func):
    """Декоратор для централизованной обработки ошибок БД."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.") # noqa: E501
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper



def confirm_action(action_name):
    """Фабрика декораторов для подтверждения опасных действий."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirmation = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower() # noqa: E501
            if confirmation == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                return None
        return wrapper
    return decorator



def log_time(func):
    """Декоратор для замера времени выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.3f} секунд.") # noqa: E501
        return result
    return wrapper
