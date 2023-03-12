"""
Основной исполняемый файл
"""
import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense


db_name = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    model = None
    cat_repo = SQLiteRepository[Category](db_name, Category)
    exp_repo = SQLiteRepository[Expense](db_name, Expense)

    window = ExpensePresenter(model, view, cat_repo, exp_repo)
    window.show()
    app.exec_()
