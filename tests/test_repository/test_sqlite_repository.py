from bookkeeper.repository.sqlite_repository import SQLiteRepository
import pytest
from dataclasses import dataclass


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        name: str = ''
        test: str = ''
    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository('test.db', custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    assert repo.get_all({'test': 'test'}) == objects
    for i in range(5):
        repo.delete(i+1)

