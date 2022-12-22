from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QGridLayout, QTableWidgetItem, QAbstractItemView, \
    QComboBox, QPushButton, QLabel, QVBoxLayout, QRadioButton, QGroupBox
from PyQt5.QtCore import QDate
from additionally import days_in_month, title_month
import json


class LookDataWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open('../data_time.json') as file:
            self.data_time = json.load(file)

        today = QDate.currentDate().toString(Qt.ISODate)
        self.day_week = QDate.currentDate().toString().split()[0]
        self.year, self.month, self.day = map(int, today.split('-'))

        self.setWindowTitle('Просмотр')
        self.setGeometry(300, 300, 800, 300)

        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        self.check_box_days = QRadioButton('День')
        self.check_box_weeks = QRadioButton('Неделя')
        self.check_box_months = QRadioButton('Месяц')
        self.check_box_years = QRadioButton('Год')

        self.comboBox_days = QComboBox()
        self.comboBox_weeks = QComboBox()
        self.comboBox_months = QComboBox()
        self.comboBox_years = QComboBox()

        self.check_box_days.toggled.connect(self.time_segment)
        self.check_box_weeks.toggled.connect(self.time_segment)
        self.check_box_months.toggled.connect(self.time_segment)
        self.check_box_years.toggled.connect(self.time_segment)

        self.reset()

        self.unitLayout = QGridLayout()
        self.unitLayout.addWidget(self.check_box_days, 0, 0)
        self.unitLayout.addWidget(self.check_box_weeks, 1, 0)
        self.unitLayout.addWidget(self.check_box_months, 2, 0)
        self.unitLayout.addWidget(self.check_box_years, 3, 0)
        self.unitLayout.addWidget(self.comboBox_days, 0, 1)
        self.unitLayout.addWidget(self.comboBox_weeks, 1, 1)
        self.unitLayout.addWidget(self.comboBox_months, 2, 1)
        self.unitLayout.addWidget(self.comboBox_years, 3, 1)

        self.groupBox = QGroupBox()
        self.groupBox.setLayout(self.unitLayout)

        self.btn_menu = QPushButton('Главное меню')

        self.grid_layout.addWidget(self.groupBox, 0, 0)
        self.grid_layout.addWidget(self.btn_menu, 0, 1)

    def reset(self):
        self.check_box_days.setChecked(True)

    def time_segment(self):
        try:
            self.widget.deleteLater()

        except:
            pass

        if self.check_box_days.isChecked():
            self.widget = QLabel('days')
            self.fill_day(self.month)
            self.fill_month(self.year)
            self.fill_year()
        if self.check_box_weeks.isChecked():
            self.widget = QLabel('weeks')
        if self.check_box_months.isChecked():
            self.widget = QLabel('months')
        if self.check_box_years.isChecked():
            self.widget = QLabel('years')

        self.grid_layout.addWidget(self.widget, 1, 0)

    def create_days_widgets(self):
        pass

    def fill_day(self, month):
        self.comboBox_days.clear()
        if month == self.month:
            day = self.day - 1
            self.comboBox_days.addItem('Сегодня')
        else:
            day = days_in_month[month - 1]

        while day != 0:
            self.comboBox_days.addItem(str(day))
            day -= 1

    def fill_month(self, year):
        months = sorted(set(map(int, [x.split('-')[1] for x in self.data_time.keys()
                                      if x != 'decoding' and x.split('-')[0] == str(year)])))
        months.reverse()

        self.comboBox_months.clear()
        for month in months:
            self.comboBox_months.addItem(title_month[month - 1])

    def fill_year(self):
        self.comboBox_years.clear()

        year = int(self.year)
        min_year = min(map(int, [x.split('-')[0] for x in self.data_time.keys() if x != 'decoding']))

        self.comboBox_years.addItem(str(year))
        while min_year != year:
            year -= 1
            self.comboBox_years.addItem(str(year))

    def create_table(self):
        today = f'2022-12-01'.split('-')
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
                table.setItem(i, j, QTableWidgetItem('0'))

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

        self.grid_layout.addWidget(table, 1, 0, 1, 1)


import sys
app = QApplication(sys.argv)

window = LookDataWindow()

window.show()

app.exec_()
