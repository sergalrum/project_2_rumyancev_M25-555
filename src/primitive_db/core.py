SUPPORTED_TYPES = {'int', 'str', 'bool'}


def create_table(metadata, table_name, columns):
    """
    Создаёт таблицу с указанным именем и столбцами.
    Автоматически добавляет ID:int в начало.
    Возвращает обновлённые метаданные или None при ошибке.
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    # Проверяем корректность типов
    for col in columns:
        col_name, col_type = col.split(':')
        if col_type not in SUPPORTED_TYPES:
            print(f'Некорректное значение: {col}. Поддерживаемые типы: int, str, bool.')
            return None

    # Добавляем ID и сохраняем структуру
    metadata[table_name] = ['ID:int'] + columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(metadata[table_name])}') # noqa: E501
    return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу. Возвращает обновлённые метаданные или None при ошибке."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        print('Нет созданных таблиц.')
        return

    for table in metadata:
        print(f'- {table}')
