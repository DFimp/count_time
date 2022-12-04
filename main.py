from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import Qt, QDate
from oter_window.stopwatch import Timer
from oter_window.record_data import Add
from oter_window.look_data import Look_data
from oter_window.create_category import Create
from fill_json import fill_past_date


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Основное окно')
        self.layout = QtWidgets.QVBoxLayout()

        self.btn_stopwatch = QPushButton('Секундомер', self)
        self.layout.addWidget(self.btn_stopwatch)

        self.btn_add_data = QPushButton('Запись данных', self)
        self.layout.addWidget(self.btn_add_data)

        self.btn_create_categories = QPushButton('Создать категорию', self)
        self.layout.addWidget(self.btn_create_categories)

        self.btn_look_data = QPushButton('Просмотр данных', self)
        self.layout.addWidget(self.btn_look_data)

        self.layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(self.layout)

        self.btn_stopwatch.clicked.connect(self.stopwatch)
        self.btn_add_data.clicked.connect(self.add_data)
        self.btn_create_categories.clicked.connect(self.create_category)
        self.btn_look_data.clicked.connect(self.look_data)

    def stopwatch(self):
        global window_stopwatch
        window_stopwatch = Timer()
        window_stopwatch.show()
        # self.close()

    def add_data(self):
        global window_record_data
        window_record_data = Add()
        window_record_data.show()
        # self.close()

    def create_category(self):
        global window_create
        window_create = Create()
        window_create.show()
        # self.close()

    def look_data(self):
        global window_look
        window_look = Look_data()
        window_look.show()
        # self.close()


today = QDate.currentDate().toString(Qt.ISODate)
fill_past_date(today)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

