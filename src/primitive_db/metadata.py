import json
from pathlib import Path

META_FILE = Path('db_meta.json')

def load_metadata():
    """Загружает метаданные таблиц из db_meta.json.
    Возвращает пустой словарь, если файла нет."""
    try:
        with open(META_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(metadata):
    """Сохраняет метаданные таблиц в db_meta.json."""
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
