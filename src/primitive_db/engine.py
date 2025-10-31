import prompt
from .core import create_table, drop_table, list_tables
from .utiles import load_metadata, save_metadata


METADATA_FILE = 'db_meta.json'

def print_help():
    """Вывод справки."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """Основной цикл программы."""
    while True:
        # Загружаем актуальные метаданные
        metadata = load_metadata(METADATA_FILE)

        # Запрос команды через prompt
        try:
            user_input = prompt.string('>>> Введите команду: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nДо свидания!')
            break

        if not user_input:
            continue

        # Разбор команды
        args = user_input.split()
        command = args[0].lower()

        # Обработка команд
        if command == 'create_table':
            if len(args) < 3:
                print('Некорректное значение: недостаточно аргументов. Пример: create_table users name:str age:int')
                continue

            table_name = args[1]
            columns = args[2:]
            new_metadata = create_table(metadata, table_name, columns)
            if new_metadata is not None:
                save_metadata(METADATA_FILE, new_metadata)

        elif command == 'drop_table':
            if len(args) != 2:
                print('Некорректное значение: укажите имя таблицы. Пример: drop_table users')
                continue

            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            if new_metadata is not None:
                save_metadata(METADATA_FILE, new_metadata)

        elif command == 'list_tables':
            list_tables(metadata)

        elif command == 'help':
            print_help()

        elif command == 'exit':
            print('До свидания!')
            break

        else:
            print(f'Функции "{command}" нет. Попробуйте снова.')
