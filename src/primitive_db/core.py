import json
from pathlib import Path

from prettytable import PrettyTable

from .decorators import confirm_action, handle_db_errors, log_time
from .metadata import save_metadata
from .utils import create_cacher, load_table_data, save_table_data

SUPPORTED_TYPES = {'int', 'str', 'bool'}


# Кэш для SELECT-запросов (замыкание)
_select_cache = create_cacher()



def create_table(metadata, table_name, columns):
    """
    Создаёт таблицу с указанным именем и столбцами.
    Автоматически добавляет ID:int в начало.
    Возвращает обновлённые метаданные или None при ошибке.
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    # Проверка корректности типов
    for col in columns:
        col_name, col_type = col.split(':')
        if col_type not in SUPPORTED_TYPES:
            print(f'Некорректное значение: {col}. Поддерживаемые типы: int, str, bool.')
            return None


    # Добавляем ID и сохраняем структуру
    metadata[table_name] = ['ID:int'] + columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(metadata[table_name])}') # noqa: E501


    # Создаём JSON-файл для таблицы
    data_file = Path(f'data/{table_name}.json')
    if not data_file.exists():
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f'Файл данных {data_file} создан.')
    

    return metadata



@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных и файла данных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None


    # 1. Удаляем метаданные
    del metadata[table_name]
    save_metadata(metadata)

    # 2. Удаляем файл данных
    data_file = Path(f'data/{table_name}.json')
    if data_file.exists():
        data_file.unlink()  # Удаляем файл
        print(f'Файл данных {data_file} удалён.')
    else:
        print(f'Файл данных {data_file} не найден (пропущено удаление).')


    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata




def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        print('Нет созданных таблиц.')
        return

    for table in metadata:
        print(f'- {table}')




@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет запись в таблицу. Возвращает обновлённые данные или None при ошибке."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name]
    expected_values_count = len(columns) - 1  # без ID
    if len(values) != expected_values_count:
        print(f'Некорректное значение: ожидается {expected_values_count} значений (без ID).') # noqa: E501
        return None

    # Валидация типов
    for i, (col, val) in enumerate(zip(columns[1:], values)):
        col_name, col_type = col.split(':')
        if not _validate_type(val, col_type):
            print(f'Ошибка типа: значение "{val}" для столбца "{col_name}" должно быть типа {col_type}.') # noqa: E501
            return None

    # Загрузка данных таблицы
    table_data = load_table_data(table_name)


    # Генерация ID
    new_id = 1 if not table_data else max(row['ID'] for row in table_data) + 1


    # Создание новой записи
    new_row = {'ID': new_id}
    for col, val in zip(columns[1:], values):
        col_name = col.split(':')[0]
        new_row[col_name] = val


    table_data.append(new_row)

    save_table_data(table_name, table_data)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data




@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает отфильтрованные записи. Если where_clause None — все записи."""
    # Ключ кэша: комбинация данных и условий
    cache_key = (str(table_data), str(where_clause))

    def get_data():
        if not where_clause:
            return table_data
        filtered = []
        for row in table_data:
            if all(str(row.get(k)) == str(v) for k, v in where_clause.items()):
                filtered.append(row)
        return filtered

    return _select_cache(cache_key, get_data)




@handle_db_errors
def update(table_data, table_name, set_clause, where_clause):
    """Обновляет записи по условию. Возвращает изменённые данные."""
    updated_count = 0
    for row in table_data:
        if all(str(row.get(k)) == str(v) for k, v in where_clause.items()):
            for k, v in set_clause.items():
                row[k] = v
            updated_count += 1

    if updated_count:
        save_table_data(table_name, table_data)
        print(f'Записи с условием {where_clause} успешно обновлены.')
    else:
        print('Записи не найдены для обновления.')
    return table_data




@confirm_action("удаление записей")
@handle_db_errors
def delete(table_data, table_name, where_clause):
    """Удаляет записи по условию. Возвращает изменённые данные."""
    filtered = [row for row in table_data if not all(str(row.get(k)) == str(v) for k, v in where_clause.items())] # noqa: E501
    deleted_count = len(table_data) - len(filtered)


    if deleted_count:
        save_table_data(table_name, filtered)
        print(f'Удалено {deleted_count} записей по условию {where_clause}.')
    else:
        print('Записи не найдены для удаления.')


    return filtered




def info(metadata, table_name):
    """Выводит информацию о таблице."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    table_data = load_table_data(table_name)

    print(f'Таблица: {table_name}')
    print(f'Столбцы: {", ".join(columns)}')
    print(f'Количество записей: {len(table_data)}')





def _validate_type(value, expected_type):
    """Проверяет тип значения. Поддерживает int, str, bool."""
    try:
        if expected_type == 'int':
            int(value)
        elif expected_type == 'bool':
            if str(value).lower() not in ['true', 'false']:
                return False
        elif expected_type == 'str':
            str(value)  # всегда True для str
        return True
    except (ValueError, TypeError):
        return False




def print_table(data, columns):
    """Выводит данные в виде таблицы с помощью PrettyTable."""
    if not data:
        print('Нет данных для отображения.')
        return

    table = PrettyTable()
    col_names = [col.split(':')[0] for col in columns]
    table.field_names = col_names

    for row in data:
        table.add_row([row[col] for col in col_names])

    print(table)


