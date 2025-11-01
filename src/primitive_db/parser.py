def parse_where(where_str):
    """Преобразует строку вида "age = 28" в словарь {'age': '28'}."""
    parts = where_str.strip().split('=')
    if len(parts) != 2:
        raise ValueError(f'Некорректный формат условия: {where_str}')
    key = parts[0].strip()
    value = parts[1].strip().strip('"\'')  # убирает кавычки
    return {key: value}

def parse_set(set_str):
    """Преобразует строку вида "age = 29" в словарь {'age': '29'}."""
    return parse_where(set_str)

def parse_values(values_str):
    """Преобразует строку вида 
    "(\"Sergei\", 28, true)" в список ['Sergei', '28', 'true']."""
    values_str = values_str.strip()[1:-1]  # убирает скобки
    values = [v.strip().strip('"\'') for v in values_str.split(',')]
    return values

def parse_insert_command(command):
    """
    Разбирает команду insert into <table> values (<values>).
    Возвращает: (table_name, list_of_values) или None при ошибке.
    """
    try:
        # Ищем шаблон insert into <table> values (...)
        if not command.startswith('insert into '):
            return None
        
        # Выделяем часть после 'insert into '
        rest = command[len('insert into '):]
        
        # Разделяем на имя таблицы и часть с values
        if ' values ' not in rest:
            return None
        table_part, values_part = rest.split(' values ', 1)
        
        table_name = table_part.strip()
        
        # Парсим значения в скобках
        values = parse_values(values_part)
        
        return table_name, values
    except Exception as e:
        print(f'Ошибка разбора команды insert: {e}')
        return None

def parse_select_command(command):
    """
    Разбирает команду select from <table> [where <condition>].
    Возвращает: (table_name, where_dict) или None при ошибке.
    where_dict может быть None (если нет условия where).
    """
    try:
        if not command.startswith('select from '):
            return None
        
        rest = command[len('select from '):]
        
        # Проверяем наличие where
        if ' where ' in rest:
            table_part, where_part = rest.split(' where ', 1)
            table_name = table_part.strip()
            where_clause = parse_where(where_part)
        else:
            table_name = rest.strip()
            where_clause = None
        
        
        return table_name, where_clause
    except Exception as e:
        print(f'Ошибка разбора команды select: {e}')
        return None

def parse_update_command(command):
    """
    Разбирает команду update <table> set <set_clause> where <where_clause>.
    Возвращает: (table_name, set_dict, where_dict) или None при ошибке.
    """
    try:
        if not command.startswith('update '):
            return None
        
        rest = command[len('update '):]
        
        # Ищем set
        if ' set ' not in rest:
            return None
        before_set, after_set = rest.split(' set ', 1)
        table_name = before_set.strip()
        
        # Ищем where после set
        if ' where ' not in after_set:
            return None  # where обязателен в нашем синтаксисе
        set_part, where_part = after_set.split(' where ', 1)
        
        set_clause = parse_set(set_part)
        where_clause = parse_where(where_part)
        
        
        return table_name, set_clause, where_clause
    except Exception as e:
        print(f'Ошибка разбора команды update: {e}')
        return None

def parse_delete_command(command):
    """
    Разбирает команду delete from <table> where <condition>.
    Возвращает: (table_name, where_dict) или None при ошибке.
    """
    try:
        if not command.startswith('delete from '):
            return None
        
        rest = command[len('delete from '):]
        
        if ' where ' not in rest:
            return None
        
        table_part, where_part = rest.split(' where ', 1)
        table_name = table_part.strip()
        where_clause = parse_where(where_part)
        
        return table_name, where_clause
    except Exception as e:
        print(f'Ошибка разбора команды delete: {e}')
        return None

def parse_info_command(command):
    """
    Разбирает команду info <table>.
    Возвращает: table_name или None при ошибке.
    """
    try:
        if not command.startswith('info '):
            return None
        table_name = command[len('info '):].strip()
        return table_name
    except Exception as e:
        print(f'Ошибка разбора команды info: {e}')
        return None
