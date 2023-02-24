"""
# TODO: ADD DOCSTRING
"""

import sqlite3
from abc import ABC

from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    TODO: ADD DOCSTRING
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS "Category" '
                f'("id" integer primary key autoincrement, "name" text, "parent" integer);'
                )
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
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
                )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} WHERE id = {pk}')
            res: T = cur.fetchone()  # Возвращает список из корежа со значением из БД
        con.close()
        return res

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is not None:
                k, v = list(where.keys()), list(where.values())
                cur.execute(f'SELECT * FROM {self.table_name} WHERE {k[0]} = "{v[0]}";')
            else:
                cur.execute(f'SELECT * FROM {self.table_name}')
            res = cur.fetchall()  # Возвращает список корежей из БД
        con.close()
        return res

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

        '''names = ' = ?, '.join(self.fields.keys())
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'UPDATE {self.table_name} SET ({names}) WHERE id = {obj.pk}', self.fields)
        con.close()'''

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE id = {pk}')
        con.close()

