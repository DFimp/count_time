from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QGridLayout, QTableWidgetItem, QAbstractItemView, \
    QComboBox, QPushButton, QLabel, QRadioButton, QGroupBox, QVBoxLayout
from PyQt5.QtCore import QDate
from PyQt5.Qt import QPixmap
from additionally import days_in_month, title_month, title_day_in_week, check_leap_year
from function.time_for_human import transformation
import json
import matplotlib.pyplot as chart
import math
import os

DATA = '../data_time.json'


class LookDataWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open(DATA) as file:
            self.data_time = json.load(file)

        self.today = QDate.currentDate().toString(Qt.ISODate)
        self.day_week = QDate.currentDate().toString().split()[0]
        self.year, self.month, self.day = map(int, self.today.split('-'))

        self.setWindowTitle('Просмотр')
        self.setGeometry(300, 300, 800, 300)

        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        self.check_box_days = QRadioButton('День')
        self.check_box_weeks = QRadioButton('Неделя')
        self.check_box_months = QRadioButton('Месяц')
        self.check_box_years = QRadioButton('Год')
        self.check_box_all = QRadioButton('Всё время')

        self.comboBox_days = QComboBox()
        self.comboBox_weeks = QComboBox()
        self.comboBox_months = QComboBox()
        self.comboBox_years = QComboBox()

        self.check_box_days.toggled.connect(self.time_segment)
        self.check_box_weeks.toggled.connect(self.time_segment)
        self.check_box_months.toggled.connect(self.time_segment)
        self.check_box_years.toggled.connect(self.time_segment)
        self.check_box_all.toggled.connect(self.time_segment)

        self.comboBox_days.activated.connect(self.selected_day)
        self.comboBox_weeks.activated.connect(self.selected_week)
        self.comboBox_months.activated.connect(self.selected_month)
        self.comboBox_years.activated.connect(self.selected_year)

        self.reset()

        self.unitLayout = QGridLayout()
        self.unitLayout.addWidget(self.check_box_days, 0, 0)
        self.unitLayout.addWidget(self.check_box_weeks, 1, 0)
        self.unitLayout.addWidget(self.check_box_months, 2, 0)
        self.unitLayout.addWidget(self.check_box_years, 3, 0)
        self.unitLayout.addWidget(self.check_box_all, 4, 0)
        self.unitLayout.addWidget(self.comboBox_days, 0, 1)
        self.unitLayout.addWidget(self.comboBox_weeks, 1, 1)
        self.unitLayout.addWidget(self.comboBox_months, 2, 1)
        self.unitLayout.addWidget(self.comboBox_years, 3, 1)

        self.groupBox = QGroupBox()
        self.groupBox.setLayout(self.unitLayout)

        self.btn_menu = QPushButton('Главное меню')

        self.grid_layout.addWidget(self.groupBox, 0, 0)
        self.grid_layout.addWidget(self.btn_menu, 0, 1)

    def selected_day(self):
        ''' Creates a widget of the selected day when changing ComboBox_days '''

        self.create_days_widgets(self.comboBox_days.currentText(), self.comboBox_months.currentText(),
                                 self.comboBox_years.currentText())

    def selected_week(self):
        ''' Creates a widget of the selected week when changing ComboBox_weeks '''

        self.create_weeks_widgets(self.comboBox_weeks.currentText(), self.comboBox_months.currentText(),
                                  self.comboBox_years.currentText())

    def selected_month(self):
        ''' Changing the value of ComboBox_weeks and ComboBox_days
            when changing the value of ComboBox_months '''

        if self.check_box_days.isChecked():
            self.fill_day(title_month.index(self.comboBox_months.currentText()) + 1)
            self.create_days_widgets(self.comboBox_days.currentText(), self.comboBox_months.currentText(),
                                     self.comboBox_years.currentText())

        if self.check_box_weeks.isChecked():
            self.fill_week(self.comboBox_months.currentText(), int(self.comboBox_years.currentText()))
            self.create_weeks_widgets(self.comboBox_weeks.currentText(), self.comboBox_months.currentText(),
                                      self.comboBox_years.currentText())

        if self.check_box_months.isChecked():
            self.create_months_widgets(self.comboBox_months.currentText(), self.comboBox_years.currentText())

    def selected_year(self):
        ''' Changing the value of ComboBox_weeks and ComboBox_days
            when changing the value of ComboBox_years '''

        if self.check_box_days.isChecked():
            self.fill_month(int(self.comboBox_years.currentText()))
            self.selected_month()
            self.create_days_widgets(self.comboBox_days.currentText(), self.comboBox_months.currentText(),
                                     self.comboBox_years.currentText())

        if self.check_box_weeks.isChecked():
            self.fill_month(int(self.comboBox_years.currentText()))
            self.fill_week(self.comboBox_months.currentText(), int(self.comboBox_years.currentText()))
            self.create_weeks_widgets(self.comboBox_weeks.currentText(), self.comboBox_months.currentText(),
                                      self.comboBox_years.currentText())

        if self.check_box_months.isChecked():
            self.fill_month(int(self.comboBox_years.currentText()))
            self.create_months_widgets(self.comboBox_months.currentText(), self.comboBox_years.currentText())

        if self.check_box_years.isChecked():
            self.create_years_widgets(self.comboBox_years.currentText())

    def reset(self):
        ''' Resets the RadioButton value when exiting the look_window window '''

        self.check_box_days.setChecked(True)

    def delete(self):
        ''' Deletes the widget that currently exists, if it exists '''

        try:
            self.widget.deleteLater()
        except:
            pass

    def time_segment(self):
        ''' Fill in the ComboBox values when changing the selected RadioButton '''

        if self.check_box_days.isChecked():
            self.fill_year()
            self.comboBox_weeks.clear()
            self.fill_day(self.month)
            self.fill_month(self.year)

            self.create_days_widgets(self.day, self.month, self.year)

        if self.check_box_weeks.isChecked():
            self.comboBox_days.clear()
            self.fill_week(title_month[self.month - 1], int(self.year))
            self.fill_month(self.year)
            self.fill_year()

            self.create_weeks_widgets(self.comboBox_weeks.currentText(), self.month, self.year)

        if self.check_box_months.isChecked():
            self.fill_month(self.year)
            self.fill_year()
            self.comboBox_days.clear()
            self.comboBox_weeks.clear()

            self.create_months_widgets(self.month, self.year)

        if self.check_box_years.isChecked():
            self.comboBox_days.clear()
            self.comboBox_weeks.clear()
            self.comboBox_months.clear()
            self.fill_year()

            self.create_years_widgets(self.year)

        if self.check_box_all.isChecked():
            self.comboBox_days.clear()
            self.comboBox_weeks.clear()
            self.comboBox_months.clear()
            self.comboBox_years.clear()

            self.create_all_widgets()

    def create_clear_widget(self):
        ''' Creates a QLabel only if there is no data for the selected period '''

        return QLabel('За выбранный период данные не найдены ¯\_(ツ)_/¯')

    def create_days_widgets(self, day, month, year):
        ''' Creates a widget that is displayed when RadioButton_day is selected '''

        self.delete()

        if type(day) == str:
            if day == 'Сегодня':
                day = self.day

            day = int(day)
            year = int(year)
            month = title_month.index(month) + 1

        with open(DATA) as file:
            self.data_time = json.load(file)

        date = str(year) + '-' + '0' * (2 - len(str(month))) + str(month) + '-' + '0' * (2 - len(str(day))) + str(day)
        data = self.data_time[date]

        if data:
            if os.path.exists('chart_images/image_chart_day.png'):
                os.remove('chart_images/image_chart_day.png')

            self.widget = QWidget()
            layout = QGridLayout()

            category = self.data_time['decoding']
            labels = [category[activity] for activity in data]
            max_activity = max(data, key=data.get)
            explode = []
            for activity in data.keys():
                if activity == max_activity:
                    explode.append(0.1)
                else:
                    explode.append(0)

            chart_day = chart
            chart_day.subplots()
            chart_day.pie(list(data.values()), explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
            chart_day.title('Распределение времени по категориям')
            chart_day.savefig('chart_images/image_chart_day.png')
            chart_day = QLabel()
            chart_day.setPixmap(QPixmap('chart_images/image_chart_day.png'))

            day_layout = QVBoxLayout()
            name_category = QLabel('Категории')
            name_category.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            day_layout.addWidget(name_category)

            all_time = 0
            for activity in data.items():
                day_layout.addWidget(QLabel(f'{category[activity[0]]} - {transformation(activity[1])}'))
                all_time += activity[1]

            name_analytics = QLabel('Аналитика')
            name_analytics.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            all_time = QLabel(f'Всего - {transformation(all_time)}')
            day_layout.addWidget(name_analytics)
            day_layout.addWidget(all_time)

            group_label_day = QGroupBox()
            group_label_day.setLayout(day_layout)

            layout.addWidget(chart_day, 0, 0)
            layout.addWidget(group_label_day, 0, 1)
            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clear_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def create_weeks_widgets(self, number_week, month, year):
        ''' Creates a widget that is displayed when RadioButton_week is selected '''

        self.delete()

        if type(month) == str:
            month = title_month.index(month) + 1
            year = int(year)

        with open(DATA) as file:
            self.data_time = json.load(file)

        number_week = number_week.split()
        dates_days_week = []

        if number_week[1] == '-':
            for day in range(int(number_week[0]), int(number_week[2]) + 1):
                dates_days_week.append(str(year) + '-' + '0' * (2 - len(str(month))) + str(month)
                                       + '-' + '0' * (2 - len(str(day))) + str(day))
        else:
            first_month = title_month.index(number_week[1]) + 1
            second_month = title_month.index(number_week[4]) + 1
            if first_month == 12:
                first_year = year - 1
                second_year = year
            elif second_month == 1:
                first_year = year
                second_year = year + 1
            else:
                first_year = year
                second_year = year

            for day in range(int(number_week[0]), check_leap_year(first_month - 1, first_year) + 1):
                dates_days_week.append(str(first_year) + '-' + '0' * (2 - len(str(first_month))) + str(first_month)
                                       + '-' + '0' * (2 - len(str(day))) + str(day))

            for day in range(1, int(number_week[3]) + 1):
                dates_days_week.append(str(second_year) + '-' + '0' * (2 - len(str(second_month))) + str(second_month)
                                       + '-' + '0' * (2 - len(str(day))) + str(day))

        data = []
        for date in dates_days_week:
            data.append(self.data_time.get(date))

        categories = []
        for dat in data:
            if dat:
                for category in dat:
                    if category not in categories:
                        categories.append(category)

        if any(data):
            if os.path.exists('chart_images/image_chart_week_histogram.png'):
                os.remove('chart_images/image_chart_week_histogram.png')

            self.widget = QWidget()
            layout = QGridLayout()

            self.get_histogram_week(data, dates_days_week, categories)
            chart_week_histogram = QLabel()
            chart_week_histogram.setPixmap(QPixmap('chart_images/image_chart_week_histogram.png'))

            layout.addWidget(chart_week_histogram, 0, 0)
            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clear_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def get_histogram_week(self, data, dates_days_week, categories):
        ''' Creating a histogram for week_widget '''

        chart_week_histogram = chart
        chart_week_histogram.subplots()

        time_for_day = []
        for category in categories:
            if time_for_day:
                day = []
                ind = 0
                for dat in data:
                    if dat:
                        if dat.get(category):
                            day.append(time_for_day[-1][ind] + dat[category])
                        else:
                            day.append(time_for_day[-1][ind] + 0)
                    else:
                        day.append(time_for_day[-1][ind] + 0)
                    ind += 1
                time_for_day.append(day)
            else:
                day = []
                for dat in data:
                    if dat:
                        if dat.get(category):
                            day.append(dat[category])
                        else:
                            day.append(0)
                    else:
                        day.append(0)
                time_for_day.append(day)

        style = 'секундах'
        if max(time_for_day[-1]) > 3600:
            time_for_day = [[dat / 3600 for dat in x] for x in time_for_day]
            style = 'часах'
        elif max(time_for_day[-1]) > 60:
            time_for_day = [[dat / 60 for dat in x] for x in time_for_day]
            style = 'минутах'

        [chart_week_histogram.bar(dates_days_week, x) for x in time_for_day[::-1]]

        b = [self.data_time['decoding'][category] for category in categories]
        b.reverse()
        chart_week_histogram.legend(b)
        chart_week_histogram.xticks(rotation=15)
        chart_week_histogram.title(f'Потрачено времени в {style}')
        chart_week_histogram.savefig('chart_images/image_chart_week_histogram.png')

    def create_months_widgets(self, month, year):
        self.delete()

        self.widget = QWidget()
        l = QGridLayout()
        label = QLabel(f'month = {month}, year = {year}')
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        table = self.create_table()
        l.addWidget(table, 0, 1)

        l.addWidget(label)
        self.widget.setLayout(l)
        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def create_years_widgets(self, year):
        self.delete()

        self.widget = QWidget()
        l = QGridLayout()
        label = QLabel(f'years = {year}')
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        l.addWidget(label, 0, 0)
        self.widget.setLayout(l)
        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def create_all_widgets(self):
        self.delete()

        self.widget = QWidget()
        l = QGridLayout()
        label = QLabel('all time')
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        l.addWidget(label)
        self.widget.setLayout(l)
        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def fill_day(self, month):
        ''' Counting and recording the number of days in ComboBox_days '''

        self.comboBox_days.clear()

        if month == self.month:
            day = self.day - 1
            self.comboBox_days.addItem('Сегодня')
        else:
            day = check_leap_year(month - 1, int(self.comboBox_years.currentText()))

        initial_date = min(self.data_time.keys())
        while day != 0:
            date = str(self.comboBox_years.currentText()) + '-' + '0' * (2 - len(str(month))) + str(month) + '-' + \
                   '0' * (2 - len(str(day))) + str(day)
            self.comboBox_days.addItem(str(day))
            day -= 1
            if date == initial_date:
                break

    def fill_week(self, month, year):
        ''' Counting and recording the number of weeks in ComboBox_weeks '''

        self.comboBox_weeks.clear()

        date = self.day
        day_week = self.day_week
        today_month = self.month - 1
        today_year = self.year
        month = title_month.index(month)

        number_days = check_leap_year(month, year)
        day_week = title_day_in_week.index(day_week)

        if month == today_month:
            first_day_month = day_week - date + 2

        else:
            first_day_month = day_week + 2 - date

            while True:
                if today_year == year and today_month == month:
                    break
                else:
                    today_month -= 1
                    if today_month == -1:
                        today_year -= 1
                        today_month = 11

                    number = check_leap_year(today_month, today_year)
                    first_day_month -= number

        if first_day_month <= 0:
            first_day_month = - (abs(first_day_month) % 7) - 1
        else:
            first_day_month -= 1

        first_day_month = title_day_in_week[first_day_month]
        first_day_month = title_day_in_week.index(first_day_month)

        list_week = []
        first_day = 1
        end_day = first_day + abs(first_day_month - 6)

        while True:
            if first_day_month != 0:
                list_week.append(f'{check_leap_year(month - 1, year) + 1 - first_day_month} {title_month[month - 1]} - '
                                 f'{end_day} {title_month[month]}')
                first_day_month = 0
            else:
                list_week.append(f'{first_day} - {end_day}')
            first_day = end_day + 1
            end_day += 7
            if end_day > number_days:
                end_day = 6 - (number_days - first_day)
                list_week.append(f'{first_day} {title_month[month]} - {end_day} {title_month[month - 11]}')
                break

        min_date = min(self.data_time.keys())
        if str(year) + '-' + '0' * (2 - len(str(month + 1))) + str(month + 1) == min_date[:-3]:
            number_weeks = math.ceil(((first_day_month + int(min_date[-2:]) % 7 + 1) +
                                      (check_leap_year(month, year) - int(min_date[-2:]))) / 7)
            list_week = list_week[-number_weeks:]

        [self.comboBox_weeks.addItem(x) for x in list_week]

    def fill_month(self, year):
        ''' Counting and recording the number of months in ComboBox_months '''

        self.comboBox_months.clear()

        months = sorted(set(map(int, [x.split('-')[1] for x in self.data_time.keys()
                                      if x != 'decoding' and x.split('-')[0] == str(year)])))
        months.reverse()

        for month in months:
            self.comboBox_months.addItem(title_month[month - 1])

    def fill_year(self):
        ''' Counting and recording the number of years in ComboBox_years '''

        self.comboBox_years.clear()

        year = int(self.year)
        min_year = min(map(int, [x.split('-')[0] for x in self.data_time.keys() if x != 'decoding']))

        self.comboBox_years.addItem(str(year))
        while min_year != year:
            year -= 1
            self.comboBox_years.addItem(str(year))

    def create_table(self):
        with open(DATA) as file:
            self.data_time = json.load(file)

        today = f'2023-01-01'.split('-')
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

                    time = '0' * (2 - len(hours)) + hours + ':' + '0' * (2 - len(minutes)) + minutes + ':' + '0' * \
                           (2 - len(seconds)) + seconds
                    col = int(key[-1]) - 1
                    table.setItem(i, col, QTableWidgetItem(time))
            else:
                pass

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        return table


import sys
app = QApplication(sys.argv)

window = LookDataWindow()

window.show()

app.exec_()