"""
Репозиторий для работы с БД sqlite
"""

import sqlite3
from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Позволяет работать с sqlite-запросами
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                q = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(q)
        con.close()

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk
        """
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            q = f'INSERT INTO {self.table_name} ({names}) VALUES ({p})'
            cur.execute(q, values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def __generate_object(self, db_row: tuple) -> T:
        obj: T = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            q = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            row = cur.execute(q).fetchone()
        con.close()

        if row is None:
            return None

        obj = self.cls()
        for field, value in zip(self.fields, row[1:]):
            setattr(obj, field, value)
        obj.pk = pk
        return self.__generate_object(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            req: str = f'SELECT * FROM {self.table_name}'
            cur = con.cursor()

            if where is not None:
                k, v = list(where.keys()), list(where.values())
                cur.execute(f'{req} WHERE {k[0]} = "{v[0]}";')
            else:
                cur.execute(req)

            rows = cur.fetchall()  # Возвращает список корежей из БД
        con.close()

        if not rows:
            return []

        return [self.__generate_object(row) for row in rows]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        names = list(self.fields.keys())
        sets = ', '.join(f'{name} = \'{getattr(obj, name)}\'' for name in names)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {sets} WHERE pk = {obj.pk}'
            )
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
        con.close()
