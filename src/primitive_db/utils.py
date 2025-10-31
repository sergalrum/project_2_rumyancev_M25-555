import json
#import os

def load_metadata(filepath):
    """Загружает метаданные из JSON-файла. Если файл не найден, возвращает пустой словарь."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
