from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 400)
        self.setWindowTitle('Основное окно')
        self.setStyleSheet('''
            color: white;
            background-color: #2b2b2b;
            font-family: "Arial Black";
        ''')

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        font_label = QtGui.QFont()
        font_label.setPointSize(18)

        self.label = QLabel('Хронометр')
        self.label.setFont(font_label)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        style_button = '''
            QPushButton {
                background-color: #1a1a1a;
                border-radius: 10;
                font-size: 22px;
                height: 50px
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white
            }
        '''

        self.btn_stopwatch = QPushButton('Секундомер', self)
        self.btn_add_data = QPushButton('Запись данных', self)
        self.btn_create_categories = QPushButton('Создать категорию', self)
        self.btn_look_data = QPushButton('Просмотр данных', self)

        self.btn_stopwatch.setStyleSheet(style_button)
        self.btn_add_data.setStyleSheet(style_button)
        self.btn_create_categories.setStyleSheet(style_button)
        self.btn_look_data.setStyleSheet(style_button)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn_stopwatch)
        self.layout.addWidget(self.btn_add_data)
        self.layout.addWidget(self.btn_create_categories)
        self.layout.addWidget(self.btn_look_data)