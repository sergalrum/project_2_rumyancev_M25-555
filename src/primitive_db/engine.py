import prompt

from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    print_table,
    select,
    update,
)
from .metadata import load_metadata, save_metadata
from .parser import (
    parse_delete_command,
    parse_info_command,
    parse_insert_command,
    parse_select_command,
    parse_update_command,
)
from .utils import load_table_data


def print_help():
    """Вывод справки по всем доступным командам."""
    print("\n***Управление таблицами***")
    print("  create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...")
    print("  drop_table <имя_таблицы>")
    print("  list_tables")

    print("\n***CRUD-операции***")
    print("  insert into <таблица> values (<значение1>, <значение2>, ...)")
    print("  select from <таблица> [where <столбец> = <значение>]")
    print("  update <таблица> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>") # noqa: E501
    print("  delete from <таблица> where <столбец> = <значение>")
    print("  info <таблица>")

    print("\n***Общие команды***")
    print("  help")
    print("  exit")
    print("")



def run():
    """Основной цикл программы."""
    while True:
        # Загружаем актуальные метаданные
        metadata = load_metadata()

        # Запрос команды через prompt
        try:
            user_input = prompt.string('>>> Введите команду: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nДо свидания!')
            break

        if not user_input:
            continue

        args = user_input.split()
        command = args[0].lower()

        # --- Управление таблицами ---
        if command == 'create_table':
            if len(args) < 3:
                print('Ошибка: недостаточно аргументов. Пример: create_table users name:str age:int') # noqa: E501
                continue
            table_name = args[1]
            columns = args[2:]
            new_metadata = create_table(metadata, table_name, columns)
            if new_metadata is not None:
                save_metadata(new_metadata)

        elif command == 'drop_table':
            if len(args) != 2:
                print('Ошибка: укажите имя таблицы. Пример: drop_table users')
                continue
            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)
            if new_metadata is not None:
                save_metadata(new_metadata)

        elif command == 'list_tables':
            list_tables(metadata)

        # --- CRUD-операции ---
        elif user_input.startswith('insert into '):
            parsed = parse_insert_command(user_input)
            if parsed:
                table_name, values = parsed
                insert(metadata, table_name, values)
            else:
                print('Ошибка синтаксиса команды insert. Используйте: insert into <таблица> values (<значение1>, <значение2>, ...)') # noqa: E501

        elif user_input.startswith('select from '):
            parsed = parse_select_command(user_input)
            if parsed:
                table_name, where_clause = parsed
                table_data = load_table_data(table_name)
                result = select(table_data, where_clause)
                columns = metadata.get(table_name, [])
                print_table(result, columns)
            else:
                print('Ошибка синтаксиса команды select. Используйте: select from <таблица> [where <столбец> = <значение>]') # noqa: E501

        elif user_input.startswith('update '):
            parsed = parse_update_command(user_input)
            if parsed:
                table_name, set_clause, where_clause = parsed
                table_data = load_table_data(table_name)
                update(table_data, table_name, set_clause, where_clause)  
            else:
                print('Ошибка синтаксиса команды update. Используйте: update <таблица> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>') # noqa: E501


        elif user_input.startswith('delete from '):
            parsed = parse_delete_command(user_input)
            if parsed:
                table_name, where_clause = parsed
                table_data = load_table_data(table_name)
                delete(table_data, table_name, where_clause)
            else:
                print('Ошибка синтаксиса команды delete. Используйте: delete from <таблица> where <столбец> = <значение>') # noqa: E501


        elif user_input.startswith('info '):
            table_name = parse_info_command(user_input)
            if table_name:
                info(metadata, table_name)
            else:
                print('Ошибка синтаксиса команды info. Используйте: info <таблица>')

        # --- Общие команды ---
        elif command == 'help':
            print_help()

        elif command == 'exit':
            print('До свидания!')
            break

        else:
            print(f'Команда "{command}" не найдена. Введите "help" для списка команд.')
