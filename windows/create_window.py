from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
import json


class CreateWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open('data_time.json') as file:
            self.data_time = json.load(file)

        self.setWindowTitle('Создать категорию')
        self.setGeometry(500, 300, 500, 100)
        self.setStyleSheet('''
            color: white;
            background-color: #2b2b2b;
            font-family: "Arial Black";
            font-size: 20px;
        ''')

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.labelCategory = QLabel()
        self.create_label_category()
        self.label = QLabel('Имеющиеся\nкатегории', self)
        self.lineEdit = QLineEdit()
        self.btn_save = QPushButton('Сохранить')
        self.labelLineEdit = QLabel('Новая категория', self)
        self.btn_menu = QPushButton('Главное\nменю')

        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.lineEdit.setStyleSheet('''
            border: 2px solid #ffffff;
            border-radius: 5
        ''')
        self.btn_save.setStyleSheet('''
            QPushButton {
                background-color: #1a1a1a;
                border-radius: 10;
                height: 50px;
                width: 150px;
                border: 2px solid #ffffff;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white
            }
        ''')
        self.btn_menu.setStyleSheet('''
            QPushButton {
                background-color: #1a1a1a;
                border-radius: 10;
                height: 100px;
                border: 2px solid #ffffff;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white
            }
        ''')

        self.layout.addWidget(self.labelLineEdit, 0, 0, 1, 1)
        self.layout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.layout.addWidget(self.btn_menu, 1, 2, 1, 1)
        self.layout.addWidget(self.btn_save, 0, 2, 1, 1)
        self.layout.addWidget(self.label, 1, 0, 1, 1)
        self.layout.addWidget(self.labelCategory, 1, 1, 1, 1)

        self.btn_save.clicked.connect(self.save)

    def create_label_category(self):
        if self.data_time['decoding']:
            self.labelCategory.setText('\n'.join(list(self.data_time['decoding'].values())))
        else:
            self.labelCategory.setText('Отсутствуют')

    def save(self):
        text = self.lineEdit.text().capitalize()

        if self.data_time['decoding'] and text in self.data_time['decoding'].values():
            question = QMessageBox.information(self, 'окно', 'Данная категория уже есть')

        elif not text:
            question = QMessageBox.information(self, 'окно', 'Вы ничего не ввели\nПопробуйте ещё')

        else:
            if self.data_time['decoding']:
                category = max(list(self.data_time['decoding'].keys()))
                category = category[:-1] + str(int(category[-1:]) + 1)
            else:
                category = 'category_1'

            self.data_time['decoding'][category] = text
            self.lineEdit.clear()
            self.create_label_category()

            with open('data_time.json', 'w') as file:
                json.dump(self.data_time, file, indent=4)