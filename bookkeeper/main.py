from PySide6.QtWidgets import QApplication
from presenter.expense_presenter import ExpensePresenter
from models.expense import Expense
from view.expense_view import MainWindow

import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    model = None  # TODO: здесь должна быть модель
    window = ExpensePresenter(model, view)
    window.show()
    app.exec_()
