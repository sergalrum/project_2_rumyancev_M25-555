import json
from pathlib import Path

DATA_DIR = Path('data')

def load_table_data(table_name):
    """Загружает данные таблицы из data/<имя_таблицы>.json. 
    Возвращает пустой список, если файла нет.""" 
    file_path = DATA_DIR / f"{table_name}.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в data/<имя_таблицы>.json."""
    file_path = DATA_DIR / f"{table_name}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
