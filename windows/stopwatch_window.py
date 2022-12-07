from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtCore import QTimer, Qt
from function.time_for_human import transformation


class TimerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.time = 0

        self.setWindowTitle('Секундомер')
        self.setFixedSize(330, 290)
        self.setStyleSheet('''
            color: white;
            background-color: #2b2b2b;
            font-family: "Arial Black";
            font-size: 22px;
            border: 2px solid #ffffff;
            border-radius: 5;
        ''')

        style_button_first = '''
            QPushButton {
                background-color: #1a1a1a;
                height: 50px;
                border: 2px solid #8c8b8c;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white;
                border: 0px;
            }
        '''

        style_button_second = '''
            QPushButton {
                background-color: #1a1a1a;
                height: 70px;
                border: 2px solid #8c8b8c;
                border-radius: 5;
            }
            QPushButton:pressed {
                color: #1a1a1a;
                background-color: white;
                border: 0px
            }
        '''

        self.timer = QTimer()
        self.timer.setInterval(1000)

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.btn_start = QPushButton('Старт')
        self.btn_stop = QPushButton('Стоп')
        self.lineEdit = QLineEdit('00:00:00')
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.btn_reset = QPushButton('Сброс')
        self.btn_record = QPushButton('Записать\nданные')
        self.btn_menu = QPushButton('Главное меню')

        self.btn_start.setStyleSheet(style_button_first)
        self.btn_stop.setStyleSheet(style_button_first)
        self.btn_reset.setStyleSheet(style_button_second)
        self.btn_record.setStyleSheet(style_button_second)
        self.lineEdit.setStyleSheet('''
            height: 50px
        ''')
        self.btn_menu.setStyleSheet(style_button_second)

        self.mainLayout.addWidget(self.btn_start, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.btn_stop, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.btn_reset, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.btn_record, 2, 1, 1, 1)
        self.mainLayout.addWidget(self.btn_menu, 3, 0, 1, 2)

        self.btn_start.clicked.connect(self.timer.start)
        self.btn_stop.clicked.connect(self.timer.stop)
        self.btn_reset.clicked.connect(self.reset)
        self.timer.timeout.connect(self.go_time)

    def reset(self):
        self.time = 0
        self.lineEdit.setText('00:00:00')
        self.timer.stop()

    def go_time(self):
        self.lineEdit.setText(transformation(self.time))
        self.time += 1