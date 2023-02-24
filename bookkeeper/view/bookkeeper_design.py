# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bookkeeper_design.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import sys

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 652)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 4, 581, 641))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_last_expence = QLabel(self.verticalLayoutWidget)
        self.lbl_last_expence.setObjectName(u"lbl_last_expence")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lbl_last_expence.setFont(font)

        self.verticalLayout.addWidget(self.lbl_last_expence)

        self.tree_category = QTreeView(self.verticalLayoutWidget)
        self.tree_category.setObjectName(u"tree_category")

        self.verticalLayout.addWidget(self.tree_category)

        self.lbl_budget = QLabel(self.verticalLayoutWidget)
        self.lbl_budget.setObjectName(u"lbl_budget")
        self.lbl_budget.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.lbl_budget)

        self.table_budget = QTableView(self.verticalLayoutWidget)
        self.table_budget.setObjectName(u"table_budget")
        self.table_budget.setMouseTracking(False)
        self.table_budget.setEditTriggers(QAbstractItemView.DoubleClicked)

        self.verticalLayout.addWidget(self.table_budget)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.text_sum = QLineEdit(self.verticalLayoutWidget)
        self.text_sum.setObjectName(u"text_sum")

        self.gridLayout.addWidget(self.text_sum, 1, 1, 1, 1)

        self.lbl_category = QLabel(self.verticalLayoutWidget)
        self.lbl_category.setObjectName(u"lbl_category")

        self.gridLayout.addWidget(self.lbl_category, 3, 0, 1, 1)

        self.list_category = QComboBox(self.verticalLayoutWidget)
        self.list_category.setObjectName(u"list_category")
        self.list_category.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.list_category, 3, 1, 1, 1)

        self.but1_add = QPushButton(self.verticalLayoutWidget)
        self.but1_add.setObjectName(u"but1_add")
        self.but1_add.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.but1_add, 4, 1, 1, 1)

        self.but2_change = QPushButton(self.verticalLayoutWidget)
        self.but2_change.setObjectName(u"but2_change")
        self.but2_change.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.but2_change, 3, 2, 1, 1)

        self.lbl_sum = QLabel(self.verticalLayoutWidget)
        self.lbl_sum.setObjectName(u"lbl_sum")

        self.gridLayout.addWidget(self.lbl_sum, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"The Bookkeeper App"))
        self.lbl_last_expence.setText(QCoreApplication.translate("MainWindow", u"Последние расходы"))
        self.lbl_budget.setText(QCoreApplication.translate("MainWindow", u"Бюджет"))
        self.lbl_category.setText(QCoreApplication.translate("MainWindow", u"Категория"))
        self.but1_add.setText(QCoreApplication.translate("MainWindow", u"Добавить"))
        self.but2_change.setText(QCoreApplication.translate("MainWindow", u"Редактировать"))
        self.lbl_sum.setText(QCoreApplication.translate("MainWindow", u"Сумма"))
    # retranslateUi


class TheBookkeeperApp(QMainWindow):
    def __init__(self):
        super(TheBookkeeperApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TheBookkeeperApp()
    window.show()

    sys.exit(app.exec())