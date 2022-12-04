from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QComboBox, QLabel, QTimeEdit, QDateEdit, QMessageBox
from PyQt5.QtCore import QSize, Qt, QTime, QDate
import json


class Add(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Запись данных')
        self.setGeometry(500, 300, 10, 10)

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        font_1 = QtGui.QFont()
        font_1.setBold(True)
        font_1.setPointSize(15)

        self.label_dateEdit = QLabel('Дата')
        self.label_timeEdit = QLabel('Время')
        self.label_category = QLabel('Категория')

        self.label_dateEdit.setAlignment(Qt.AlignCenter)
        self.label_timeEdit.setAlignment(Qt.AlignCenter)
        self.label_category.setAlignment(Qt.AlignCenter)

        self.dateEdit = QDateEdit(QDate.currentDate())
        self.dateEdit.setMaximumDate(QDate.currentDate())
        self.timeEdit = QTimeEdit()

        self.label_dateEdit.setFont(font_1)
        self.label_timeEdit.setFont(font_1)
        self.label_category.setFont(font_1)
        self.dateEdit.setFont(font_1)
        self.timeEdit.setFont(font_1)

        self.timeEdit.setDisplayFormat('HH:mm:ss')

        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(QSize(50, 50))

        font_2 = QtGui.QFont()
        font_2.setBold(True)
        font_2.setPointSize(10)

        self.save_btn = QPushButton('Сохранить')
        self.reset_btn = QPushButton('Сбросить')
        self.create_btn = QPushButton('Создать категорию')

        self.save_btn.setFont(font_2)
        self.reset_btn.setFont(font_2)
        self.create_btn.setFont(font_2)
        self.save_btn.setMinimumSize(QSize(50, 100))
        self.reset_btn.setMinimumSize(QSize(100, 100))
        self.create_btn.setMinimumSize(QSize(200, 100))

        self.mainLayout.addWidget(self.label_dateEdit, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.dateEdit, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.label_timeEdit, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.timeEdit, 1, 1, 1, 2)
        self.mainLayout.addWidget(self.label_category, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.comboBox, 2, 1, 1, 2)
        self.mainLayout.addWidget(self.save_btn, 3, 0, 1, 1)
        self.mainLayout.addWidget(self.reset_btn, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.create_btn, 3, 2, 1, 1)

        self.create_push_button_category()

        self.reset_btn.clicked.connect(self.reset)
        self.save_btn.clicked.connect(self.save)

    def reset(self):
        self.timeEdit.setTime(QTime(00, 00, 00))
        self.dateEdit.setDate(QDate.currentDate())

    def create_push_button_category(self):
        with open('data_time.json', 'r') as file:
            self.category = json.loads(file.read())['decoding']

        for value in self.category.values():
            self.comboBox.addItem(value)

    def add(self):
        for key, val in self.category.items():
            if val == self.comboBox.currentText():
                selected_category = key
                break

        time = self.timeEdit.text()
        time = list(map(int, time.split(':')))
        time = 3600 * time[0] + 60 * time[1] + time[2]

        date = self.dateEdit.date().toString(Qt.ISODate)

        with open('data_time.json') as file:
            data_time = json.load(file)

        if not data_time[date]:
            data_time[date][selected_category] = time

        else:
            data_time[date][selected_category] += time

        with open('data_time.json', 'w') as file:
            json.dump(data_time, file, indent=4)

    def save(self):
        text = 'Вы уверены, что правильно указали данные и хотите их сохранить?'
        question = QMessageBox.question(self, 'Сохранение', text, QMessageBox.Yes|QMessageBox.No)

        if question == QMessageBox.Yes:
            self.add()
            self.reset()