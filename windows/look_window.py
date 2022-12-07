from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QGridLayout, QTableWidgetItem, QAbstractItemView, \
    QComboBox, QPushButton
from PyQt5.QtCore import QDate
from additionally import days_in_month
import json


class Look_data(QWidget):
    def __init__(self):
        super().__init__()

        with open('data_time.json') as file:
            self.data_time = json.load(file)

        self.setWindowTitle('Просмотр')
        self.setGeometry(300, 300, 800, 300)

        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        self.comboBox = QComboBox()
        self.comboBox.addItem('1')
        self.comboBox.addItem('2')

        self.btn_menu = QPushButton('Главное меню')

        self.grid_layout.addWidget(self.comboBox, 0, 0)
        self.grid_layout.addWidget(self.btn_menu, 0, 1)

        self.create_table()

        self.comboBox.currentTextChanged.connect(self.create_table)

    def create_table(self):

        today = '2022-11-01'.split('-')
        category = list(self.data_time['decoding'].values())
        month = today[1]

        daysKeys = [today[0] + '-' + today[1] + '-' + '0' * (2 - len(str(day + 1))) + str(day + 1) for day in
                    range(days_in_month[int(month) - 1])]

        table = QTableWidget(self)
        table.setColumnCount(len(category))
        table.setRowCount(days_in_month[int(month) - 1])

        table.setHorizontalHeaderLabels(category)
        table.setVerticalHeaderLabels(daysKeys)

        for i in range(days_in_month[int(month) - 1]):
            for j in range(int(max(self.data_time['decoding'])[-1])):
                table.setItem(i, j, QTableWidgetItem('00:00:00'))

            if self.data_time.get(daysKeys[i]):
                data = self.data_time[daysKeys[i]]
                for key, val in data.items():
                    hours = str(val // 3600)
                    minutes = str((val % 3600) // 60)
                    seconds = str(val % 60)

                    time = '0' * (2 - len(hours)) + hours + ':' + '0' * (2 - len(minutes)) + minutes + ':' + '0' * (
                            2 - len(seconds)) + seconds
                    col = int(key[-1]) - 1
                    table.setItem(i, col, QTableWidgetItem(time))
            else:
                pass

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.grid_layout.addWidget(table, 1, 0, 1, 2)
#
#
# import sys
# app = QApplication(sys.argv)
#
# window = Look_data()
#
# window.show()
#
# app.exec_()
