from datetime import datetime

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=datetime.now(),
                added_date=datetime.now(), comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1


def test_create_brief():
    e = Expense(100, 1, 'test')
    assert e.amount == 100
    assert e.category == 1
    assert e.comment == 'test'


def test_can_add_to_repo(repo):
    e = Expense(100, 1, 'test')
    pk = repo.add(e)
    assert e.pk == pk
