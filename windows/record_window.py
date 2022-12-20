from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QComboBox, QLabel, QTimeEdit, QDateEdit, QMessageBox
from PyQt5.QtCore import Qt, QTime, QDate
import json


class Add(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Запись данных')
        self.setGeometry(500, 300, 10, 10)
        self.setStyleSheet('''
            color: white;
            background-color: #2b2b2b;
            font-family: "Arial Black";
            font-size: 22px
        ''')

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.label_dateEdit = QLabel('Дата')
        self.label_timeEdit = QLabel('Время')
        self.label_category = QLabel('Категория')

        self.dateEdit = QDateEdit(QDate.currentDate())
        self.dateEdit.setMaximumDate(QDate.currentDate())
        self.timeEdit = QTimeEdit()

        self.timeEdit.setDisplayFormat('HH:mm:ss')

        self.comboBox = QComboBox()

        self.btn_save = QPushButton('Добавить')
        self.btn_reset = QPushButton('Сбросить')
        self.btn_create = QPushButton('Создать\nкатегорию')
        self.btn_menu = QPushButton('Главное\nменю')

        style_button = '''
            QPushButton {
                background-color: #1a1a1a;
                border-radius: 10;
                width: 170px;
                height: 70px;
                border: 2px solid #ffffff;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white
            }
        '''

        style_button_menu = '''
            QPushButton {
                color: #1a1a1a;
                background-color: white;
                border-radius: 10;
                width: 170px;
                height: 70px;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: white;
                background-color: #1a1a1a 
            }
        '''

        self.label_dateEdit.setAlignment(Qt.AlignCenter)
        self.label_timeEdit.setAlignment(Qt.AlignCenter)
        self.label_category.setAlignment(Qt.AlignCenter)
        self.comboBox.setStyleSheet('''
            QComboBox{
                background-color: #1a1a1a;
                border: 2px solid white;
                border-radius: 5;
            }
            QComboBox QAbstractItemView {
                border: 1px solid white;
                padding: 5px;
                background-color: black;
                outline: 0px;
                selection-background-color: #7d7d7d;
            }
        ''')
        self.btn_save.setStyleSheet(style_button)
        self.btn_create.setStyleSheet(style_button)
        self.btn_menu.setStyleSheet(style_button_menu)
        self.btn_reset.setStyleSheet(style_button)

        self.mainLayout.addWidget(self.label_dateEdit, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.dateEdit, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.label_timeEdit, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.timeEdit, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.label_category, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.comboBox, 2, 1, 1, 1)
        self.mainLayout.addWidget(self.btn_save, 3, 0, 1, 1)
        self.mainLayout.addWidget(self.btn_reset, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.btn_create, 4, 1, 1, 1)
        self.mainLayout.addWidget(self.btn_menu, 4, 0, 1, 1)

        self.create_push_button_category()

        self.btn_reset.clicked.connect(self.reset)
        self.btn_save.clicked.connect(self.save)

    def record_time_edit(self, time):
        self.timeEdit.setTime(QTime(*time))

    def reset(self):
        self.timeEdit.setTime(QTime(00, 00, 00))
        self.dateEdit.setDate(QDate.currentDate())

    def create_push_button_category(self):
        with open('data_time.json') as file:
            self.category = json.load(file)['decoding']

        if self.category:
            for value in self.category.values():
                self.comboBox.addItem(value)
        else:
            self.comboBox.addItem('Категорий нет')

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

        if selected_category not in data_time[date].keys():
            data_time[date][selected_category] = time

        else:
            data_time[date][selected_category] += time

        with open('data_time.json', 'w') as file:
            json.dump(data_time, file, indent=4)

    def save(self):
        if self.comboBox.currentText() == 'Категорий нет':
            window = QMessageBox.information(self, 'Предупреждение', 'У вас пока не имеется категорий')
        else:
            text = 'Вы уверены, что правильно указали данные и хотите их сохранить?'
            question = QMessageBox.question(self, 'Сохранение', text, QMessageBox.Yes | QMessageBox.No)

            if question == QMessageBox.Yes:
                self.add()
                self.reset()