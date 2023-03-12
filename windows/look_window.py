from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QGridLayout, QTableWidgetItem, QAbstractItemView, \
    QComboBox, QPushButton, QLabel, QRadioButton, QGroupBox, QVBoxLayout
from PyQt5.QtCore import QDate
from additionally import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from function.time_for_human import transformation
import json
import math
import numpy as np

DATA = 'data_time.json'


class LookDataWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open(DATA) as file:
            self.data_time = json.load(file)

        self.today = QDate.currentDate().toString(Qt.ISODate)
        self.day_week = QDate.currentDate().toString().split()[0]
        self.year, self.month, self.day = map(int, self.today.split('-'))

        self.setWindowTitle('Просмотр')
        self.setFixedSize(1550, 700)
        self.setStyleSheet('''
                    color: white;
                    background-color: #2b2b2b;
                    font-family: "Arial Black";
                ''')

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
            self.fill_day(TITLE_MONTH.index(self.comboBox_months.currentText()) + 1)
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
            self.fill_week(TITLE_MONTH[self.month - 1], int(self.year))
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

    def create_clean_widget(self) -> QLabel:
        ''' Creates a QLabel only if there is no data for the selected period '''

        return QLabel("За выбранный период данные не найдены ¯\_(ツ)_/¯")

    def create_days_widgets(self, day: str or int, month: str or int, year: str or int) -> None:
        ''' Creates a widget that is displayed when RadioButton_day is selected '''

        self.delete()

        if type(day) == str:
            if day == 'Сегодня':
                day = self.day

            day = int(day)
            year = int(year)
            month = TITLE_MONTH.index(month) + 1

        with open(DATA) as file:
            self.data_time = json.load(file)

        date = str(year) + '-' + '0' * (2 - len(str(month))) + str(month) + '-' + '0' * (2 - len(str(day))) + str(day)
        data = self.data_time[date]

        if data:
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

            fig = Figure()
            ax = fig.add_subplot(111)
            canvas = FigureCanvas(fig)
            ax.pie(list(data.values()), explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
            ax.set_title('Распределение времени по категориям')

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

            layout.addWidget(canvas, 0, 0)
            layout.addWidget(group_label_day, 0, 1)
            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clean_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def create_weeks_widgets(self, number_week: str, month: int, year: int) -> None:
        ''' Creates a widget that is displayed when RadioButton_week is selected '''

        self.delete()

        if type(month) == str:
            month = TITLE_MONTH.index(month) + 1
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
            first_month = TITLE_MONTH.index(number_week[1]) + 1
            second_month = TITLE_MONTH.index(number_week[4]) + 1
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
            self.widget = QWidget()
            layout = QGridLayout()

            sum_data_category, canvas = self.get_pie_chart(data, categories)

            layout.addWidget(self.get_histogram(data, dates_days_week, categories, 'week'), 0, 0)
            layout.addWidget(canvas, 0, 1)
            layout.addWidget(self.get_analytics_data_week(data, sum_data_category, categories), 0, 2)
            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clean_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def get_pie_chart(self, data: list, categories: list) -> list and FigureCanvas:
        ''' Creating a pie chart for week, month, year widget '''

        fig = Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        sum_data_category = []
        ind = 0

        for category in categories:
            sum_data_category.append(0)
            for dat in data:
                if dat and dat.get(category):
                    sum_data_category[ind] += dat.get(category)
            ind += 1

        explode = [0.1 if activity == max(sum_data_category) else 0 for activity in sum_data_category]
        ax.pie(sum_data_category, labels=[self.data_time['decoding'][category] for category in categories],
                           explode=explode, autopct='%1.1f%%', shadow=True)
        ax.set_title('Распределение времени по категориям')

        return sum_data_category, canvas

    def get_histogram(self, data: list, dates: list, categories: list, type_: str) -> FigureCanvas:
        ''' Creating a histogram for week, month, year widget '''

        fig1 = Figure()
        ax_histogram = fig1.add_subplot(111)
        canvas_histogram = FigureCanvas(fig1)

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

        if type_ == 'month':
            dates = [date[-5:] for date in dates]
            [ax_histogram.bar(dates, x) for x in time_for_day[::-1]]
            ax_histogram.tick_params(axis='x', which='major', labelsize=9)

        elif type_ == 'week' or type_ == 'year':
            [ax_histogram.bar(dates, x) for x in time_for_day[::-1]]

        categories = [self.data_time['decoding'][category] for category in categories]
        categories.reverse()
        ax_histogram.legend(categories)
        ax_histogram.set_title(f'Потрачено времени в {style}')

        if type_ == 'week':
            ax_histogram.tick_params('x', labelrotation=15)

        elif type_ == 'month':
            ax_histogram.set_xticks(np.arange(0, len(dates), (len(dates) // 7)))
            ax_histogram.tick_params('x', labelrotation=15)

        elif type_ == 'year':
            ax_histogram.tick_params('x', labelrotation=45)

        return canvas_histogram

    def get_analytics_data_week(self, data: list, sum_data_category: list, categories: list) -> QGroupBox:
        ''' Creating an analytics widget in a week '''

        week_layout = QVBoxLayout()

        name_category = QLabel('Категории')
        name_category.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        week_layout.addWidget(name_category)

        for category in enumerate(sum_data_category):
            ind = category[0]
            ind = categories[ind]
            week_layout.addWidget(QLabel(f'{self.data_time["decoding"][ind]} - {transformation(category[1])}'))
            week_layout.addWidget(QLabel(f'Среднее время в день - {transformation(int(category[1] / 7))}'))

        name_analytics = QLabel('Аналитика')
        name_analytics.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        week_layout.addWidget(name_analytics)

        all_time = QLabel(f'Всего - {transformation(sum(sum_data_category))}')
        week_layout.addWidget(all_time)

        data = [sum(day.values()) if day else 0 for day in data]
        best_day_week = max(data)
        for day in enumerate(data):
            if day[1] == best_day_week:
                ind = day[0]
                best_day_week = full_title_day_in_week[ind]
                break
        week_layout.addWidget(QLabel(f'Лучший день - {best_day_week}'))

        group_label_month = QGroupBox()
        group_label_month.setLayout(week_layout)

        return group_label_month

    def create_months_widgets(self, month: int or str, year: int or str) -> None:
        ''' Creates a widget that is displayed when RadioButton_month is selected '''

        self.delete()

        if type(month) == str:
            month = TITLE_MONTH.index(month) + 1
            year = int(year)

        with open(DATA) as file:
            self.data_time = json.load(file)

        days_of_month = []

        number_day = check_leap_year(month-1, year)

        for day in range(1, number_day + 1):
            days_of_month.append(str(year) + '-' + '0' * (2 - len(str(month))) + str(month)
                                 + '-' + '0' * (2 - len(str(day))) + str(day))

        data = []
        for date in days_of_month:
            data.append(self.data_time.get(date))

        categories = []
        for dat in data:
            if dat:
                for category in dat:
                    if category not in categories:
                        categories.append(category)

        if any(data):
            self.widget = QWidget()
            layout = QGridLayout()

            sum_data_category, canvas = self.get_pie_chart(data, categories)

            layout.addWidget(self.get_histogram(data, days_of_month, categories, 'month'), 0, 0)
            layout.addWidget(canvas, 0, 1)
            layout.addWidget(self.get_analytics_data_month(data, sum_data_category, categories,
                                                           days_of_month, number_day), 0, 2)
            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clean_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def get_analytics_data_month(self, data: list, sum_data_category: list, categories: list,
                                 days_of_month: list, number_day: int) -> QGroupBox:
        ''' Creating an analytics widget in a month '''

        month_layout = QVBoxLayout()

        name_category = QLabel('Категории')
        name_category.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        month_layout.addWidget(name_category)

        for category in enumerate(sum_data_category):
            ind = category[0]
            ind = categories[ind]
            month_layout.addWidget(QLabel(f'{self.data_time["decoding"][ind]} - {transformation(category[1])}'))
            month_layout.addWidget(QLabel(f'Среднее время в день - {transformation(int(category[1] / number_day))}'))

        name_analytics = QLabel('Аналитика')
        name_analytics.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        month_layout.addWidget(name_analytics)
        month_layout.addWidget(QLabel(f'Всего - {transformation(sum(sum_data_category))}'))
        month_layout.addWidget(QLabel(f'Среднее время в день - '
                                      f'{transformation(math.ceil(sum(sum_data_category) / number_day))}'))
        data = [sum(day.values()) if day else 0 for day in data]
        day = days_of_month[data.index(max(data))]
        month_layout.addWidget(QLabel(f'Лучший день - {int(day[-2:])} '
                                      f'{FULL_TITLE_MONTH_GENITIVE_CASE[int(day[-5: -3]) - 1]}'))

        group_label_week = QGroupBox()
        group_label_week.setLayout(month_layout)

        return group_label_week

    def create_years_widgets(self, year: int or str) -> None:
        ''' Creates a widget that is displayed when RadioButton_year is selected '''

        if type(year) == str:
            year = int(year)

        self.delete()

        with open(DATA) as file:
            self.data_time = json.load(file)

        data = []
        categories = []

        for month in np.arange(1, 13, 1, dtype=int):
            days = check_leap_year(month - 1, year)
            month = '0' * (2 - len(str(month))) + str(month)
            data.append({})
            for day in np.arange(1, days + 1, 1, dtype=int):
                day = '0' * (2 - len(str(day))) + str(day)
                date = str(year)+'-'+month+'-'+day
                if self.data_time.get(date):
                    for key, val in self.data_time[date].items():
                        if key in data[-1].keys():
                            data[-1][key] += val
                        else:
                            data[-1][key] = val

                        if key not in categories:
                            categories.append(key)

        if any(data):
            self.widget = QWidget()
            layout = QGridLayout()

            sum_data_category, canvas = self.get_pie_chart(data, categories)

            layout.addWidget(self.get_histogram(data, TITLE_MONTH, categories, 'year'), 0, 0)
            layout.addWidget(canvas, 0, 1)
            layout.addWidget(self.get_analytics_data_year(data, sum_data_category, categories), 0, 2)

            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clean_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def get_analytics_data_year(self, data: list, sum_data_category: list, categories: list,) -> QGroupBox:
        ''' Creating an analytics widget in a year '''

        year_layout = QVBoxLayout()

        name_category = QLabel('Категории')
        name_category.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        year_layout.addWidget(name_category)

        for category in enumerate(sum_data_category):
            ind = category[0]
            ind = categories[ind]
            year_layout.addWidget(QLabel(f'{self.data_time["decoding"][ind]} - {transformation(category[1])}'))
            year_layout.addWidget(QLabel(f'Среднее время в месяц - {transformation(int(category[1] / 12))}'))

        name_analytics = QLabel('Аналитика')
        name_analytics.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        year_layout.addWidget(name_analytics)
        year_layout.addWidget(QLabel(f'Всего - {transformation(sum(sum_data_category))}'))
        year_layout.addWidget(QLabel(f'Среднее время в месяц - '
                                      f'{transformation(math.ceil(sum(sum_data_category) / 12))}'))
        data = [sum(day.values()) if day else 0 for day in data]
        year_layout.addWidget(QLabel(f'Лучший месяц - {FULL_TITLE_MONTH[data.index(max(data))]}'))
        year_layout.addWidget(QLabel(f'Потрачено времени - {transformation(max(data))}'))

        group_label_year = QGroupBox()
        group_label_year.setLayout(year_layout)

        return group_label_year

    def create_all_widgets(self) -> None:
        ''' Creates a widget that is displayed when RadioButton_all_time is selected '''

        self.delete()

        with open(DATA) as file:
            self.data_time = json.load(file)

        data = self.data_time.copy()
        del data['decoding']
        sum_data = {}
        data_growth = []
        dates = []
        best_day = [None, 0]
        for key, value in data.items():
            if best_day[1] < sum(value.values()):
                best_day = [key, sum(value.values())]

            dates.append(key)
            if data_growth:
                data_growth.append(sum(value.values()) + data_growth[-1])
            else:
                data_growth.append(sum(value.values()))

            for category, val in value.items():
                if category not in sum_data.keys():
                    sum_data[category] = val
                else:
                    sum_data[category] += val

        if any(data):
            self.widget = QWidget()
            layout = QGridLayout()

            layout.addWidget(self.get_plot_chart_all_time(dates, data_growth), 0, 0)
            layout.addWidget(self.get_pie_chart_all_time(sum_data), 0, 1)
            layout.addWidget(self.get_analytics_data_all_time(sum_data, best_day), 0, 2)

            self.widget.setLayout(layout)

        else:
            self.widget = self.create_clean_widget()
            self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.grid_layout.addWidget(self.widget, 1, 0, 1, 2)

    def get_pie_chart_all_time(self, data: dict) -> FigureCanvas:
        """ Creating a pie chart for all time widget """

        fig = Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        explode = [0.1 if activity == max(data.values()) else 0 for activity in data.values()]
        ax.pie(data.values(), labels=[self.data_time['decoding'][category] for category in data.keys()],
                      explode=explode, autopct='%1.1f%%', shadow=True)
        ax.set_title('Распределение времени по категориям')

        return canvas

    def get_plot_chart_all_time(self, dates: list, data_growth: list) -> FigureCanvas:
        """ Creating a plot chart for all time widget """

        fig = Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        style = 'секундах'
        if data_growth[-1] > 3600:
            data_growth = [dat // 3600 for dat in data_growth]
            style = 'часах'
        elif data_growth[-1] > 60:
            data_growth = [dat // 60 for dat in data_growth]
            style = 'минутах'
        ax.plot(dates, data_growth)
        ax.set_xticks(np.arange(0, len(data_growth), (len(data_growth) // 7)))
        ax.tick_params('x', labelrotation=20)
        ax.set_title(f'Прогресс времени в {style}')
        canvas.draw()

        return canvas

    def get_analytics_data_all_time(self, data: dict, best_day: list) -> QGroupBox:
        ''' Creating an analytics widget in the all time '''

        all_time_layout = QVBoxLayout()

        name_category = QLabel('Категории')
        name_category.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        all_time_layout.addWidget(name_category)

        for category, time in data.items():
            all_time_layout.addWidget(QLabel(f'{self.data_time["decoding"][category]} - {transformation(time)}'))

        name_analytics = QLabel('Аналитика')
        name_analytics.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        all_time_layout.addWidget(name_analytics)
        all_time_layout.addWidget(QLabel(f'Всего - {transformation(sum(data.values()))}'))
        all_time_layout.addWidget(QLabel(f'Лучший день - {best_day[0]}'))
        all_time_layout.addWidget(QLabel(f'Время в этот день - {transformation(best_day[1])}'))

        group_label_all_time = QGroupBox()
        group_label_all_time.setLayout(all_time_layout)

        return group_label_all_time

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
        month = TITLE_MONTH.index(month)

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
                list_week.append(f'{check_leap_year(month - 1, year) + 1 - first_day_month} {TITLE_MONTH[month - 1]} - '
                                 f'{end_day} {TITLE_MONTH[month]}')
                first_day_month = 0
            else:
                list_week.append(f'{first_day} - {end_day}')
            first_day = end_day + 1
            end_day += 7
            if end_day > number_days:
                end_day = 6 - (number_days - first_day)
                list_week.append(f'{first_day} {TITLE_MONTH[month]} - {end_day} {TITLE_MONTH[month - 11]}')
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
            self.comboBox_months.addItem(TITLE_MONTH[month - 1])

    def fill_year(self):
        ''' Counting and recording the number of years in ComboBox_years '''

        self.comboBox_years.clear()

        year = int(self.year)
        min_year = min(map(int, [x.split('-')[0] for x in self.data_time.keys() if x != 'decoding']))

        self.comboBox_years.addItem(str(year))
        while min_year != year:
            year -= 1
            self.comboBox_years.addItem(str(year))

    # def create_table(self):
    #     with open(DATA) as file:
    #         self.data_time = json.load(file)
    #
    #     today = f'2023-03-01'.split('-')
    #     category = list(self.data_time['decoding'].values())
    #     month = today[1]
    #
    #     daysKeys = [today[0] + '-' + today[1] + '-' + '0' * (2 - len(str(day + 1))) + str(day + 1) for day in
    #                 range(DAYS_IN_MONTH[int(month) - 1])]
    #
    #     table = QTableWidget(self)
    #     table.setColumnCount(len(category))
    #     table.setRowCount(DAYS_IN_MONTH[int(month) - 1])
    #
    #     table.setHorizontalHeaderLabels(category)
    #     table.setVerticalHeaderLabels(daysKeys)
    #
    #     for i in range(DAYS_IN_MONTH[int(month) - 1]):
    #         for j in range(int(max(self.data_time['decoding'])[-1])):
    #             table.setItem(i, j, QTableWidgetItem('0'))
    #
    #         if self.data_time.get(daysKeys[i]):
    #             data = self.data_time[daysKeys[i]]
    #             for key, val in data.items():
    #                 hours = str(val // 3600)
    #                 minutes = str((val % 3600) // 60)
    #                 seconds = str(val % 60)
    #
    #                 time = '0' * (2 - len(hours)) + hours + ':' + '0' * (2 - len(minutes)) + minutes + ':' + '0' * \
    #                        (2 - len(seconds)) + seconds
    #                 col = int(key[-1]) - 1
    #                 table.setItem(i, col, QTableWidgetItem(time))
    #         else:
    #             pass
    #
    #     table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     return table

# import sys
#
# app = QApplication(sys.argv)
#
# window = LookDataWindow()
#
# window.show()
#
# app.exec_()
