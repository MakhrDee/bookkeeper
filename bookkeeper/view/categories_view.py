"""
Модуль графического диалогового окна категорий
"""
from collections import deque
from typing import Any
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class CategoryDialog(QDialog):
    """
    Диалоговое окно категорий
    """
    def __init__(self, data: Any):
        super().__init__()
        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        data = [{'unique_id': c.pk, 'category_name': c.name,
                 'parent_id': c.parent} for c in data]
        self.importData(data)
        self.tree.expandAll()

    def importData(self, data: Any, root: Any = None) -> None:
        """
        Импорт данных по категориям в дерево
        """
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen: Any = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['parent_id'] is None:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['category_name'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)
