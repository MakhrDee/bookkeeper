"""
Графический модуль модели расходов
"""
from typing import Any
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QComboBox, QLineEdit, QPushButton
from PySide6 import QtCore, QtWidgets
from bookkeeper.view.categories_view import CategoryDialog


class TableModel(QtCore.QAbstractTableModel):
    """
    Модель таблицы расходов
    """
    def __init__(self, data: Any):
        super(TableModel, self).__init__()
        self._data = data

        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section: int, orientation: Any,
                   role: int = QtCore.Qt.DisplayRole) -> Any:
        """
        Данные по заголовкам столбцов
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index: Any, role: int) -> Any:
        """
        Данные по заполнению полей
        """
        if role == QtCore.Qt.DisplayRole:
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index: Any) -> int:
        """
        Расчет числа строк
        """
        return len(self._data)

    def columnCount(self, index: Any) -> int:
        """
        Расчет числа столбцов
        """
        return len(self._data[0].__dataclass_fields__)


class MainWindow(QtWidgets.QMainWindow):
    """
    Главное окно графического интерфейса
    """
    def __init__(self) -> None:
        super().__init__()
        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel('Последние расходы'))
        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget = QtWidgets.QTableView()
        self.layout.addWidget(self.budget)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 2, 0)
        self.comment_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.comment_line_edit, 2, 1)
        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 3, 1)
        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 3, 2)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data: Any) -> None:
        """
        Разметка таблицы расходов
        """
        if data:
            self.item_model = TableModel(data)
            self.expenses_grid.setModel(self.item_model)
            self.expenses_grid.resizeColumnsToContents()
            grid_width = sum([self.expenses_grid.columnWidth(x) for x
                              in range(0, self.item_model.columnCount(0) + 1)])
            self.setFixedSize(grid_width + 80, 600)

    def set_category_dropdown(self, data: Any) -> None:
        """
        Установить выбранную в выпадающем списке категорию
        """
        for cat in data:
            self.category_dropdown.addItem(cat.name, cat.pk)

    def on_expense_add_button_clicked(self, slot: Any) -> None:
        """
        Кнопка добавления записи о расходах
        """
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot: Any) -> None:
        """
        Кнопка удаления записи/записей о расходах
        """
        self.expense_delete_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """
        Получить сумму из текстового поля
        """
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

    def __get_selected_row_indices(self) -> list[int]:
        """
        Получить индексы выбранной строки/строк из таблицы расходов
        """
        return list(set([qmi.row() for qmi in
                         self.expenses_grid.selectionModel().selection().indexes()]))

    def get_selected_expenses(self) -> list[int] | None:
        """
        Получить выбранную/выбранные записи о расходах
        """
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]

    def get_selected_cat(self) -> Any:
        """
        Получить индекс выбранную категорию в выпадающем списке
        """
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def get_comment(self) -> str:
        """
        Получить комментарий из текстового поля
        """
        return str(self.comment_line_edit.text())

    def on_category_edit_button_clicked(self, slot: Any) -> None:
        """
        Кнопка редактирования категорий
        """
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, data: Any) -> None:
        """
        Открыть диалоговое окно категорий
        """
        if data:
            cat_dlg = CategoryDialog(data)
            cat_dlg.setWindowTitle('Редактирование категорий')
            cat_dlg.setGeometry(300, 100, 600, 300)
            cat_dlg.exec_()
