"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

cat_repo = SQLiteRepository[Category]('test.db', Category)
exp_repo = SQLiteRepository[Expense]('test.db', Expense)

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd == 'добавить':
        obj = input('$> ')
        cat_repo.add(Category(obj))
        print(*cat_repo.get_all(), sep='\n')
    elif cmd.isdigit():
        if cat_repo.get(int(cmd)) is not None:
            print(cat_repo.get(int(cmd)))
            print(cmd[0])
        else:
            print(f'неверный id')
        continue
    elif 'del' in cmd and cmd[-1].isdigit():
        pk = cmd.split(maxsplit=1)[1]
        if cat_repo.get(int(pk)) is not None:
            cat_repo.delete(int(pk))
            print(*cat_repo.get_all(), sep='\n')
        else:
            print(f'неверный id')
        continue
    elif 'up' in cmd and cmd[-1].isdigit():
        pk = cmd.split(maxsplit=1)[1]
        if cat_repo.get(int(pk)) is not None:
            cat_repo.update(cat_repo.get(int(pk)))
            print(*cat_repo.get_all(), sep='\n')
        else:
            print(f'неверный id')
            continue
        continue

    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
            print(cat)
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        # cat = cat[int(input('$> '))]
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)

