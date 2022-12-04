from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QTimer, Qt


class Timer(QWidget):
    def __init__(self):
        super().__init__()

        self.time = 0

        self.setWindowTitle('Секундомер')
        self.setGeometry(200, 200, 400, 200)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.p)

        self.mainLayout = QVBoxLayout()

        self.btn_start = QPushButton('Старт')
        self.mainLayout.addWidget(self.btn_start)

        self.btn_stop = QPushButton('Стоп')
        self.mainLayout.addWidget(self.btn_stop)

        self.lineEdit = QLineEdit('00:00:00')
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.lineEdit)

        self.btn_reset = QPushButton('Сброс')
        self.mainLayout.addWidget(self.btn_reset)

        self.btn_record = QPushButton('Записать данные')
        self.mainLayout.addWidget(self.btn_record)

        self.setLayout(self.mainLayout)

        self.btn_start.clicked.connect(self.timer.start)
        self.btn_stop.clicked.connect(self.timer.stop)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_record.clicked.connect(self.record)

    def reset(self):
        self.time = 0
        self.lineEdit.setText('00:00:00')

    def p(self):
        self.display_time()
        self.time += 1

    def record(self):
        pass

    def display_time(self):

        hours = str(self.time // 3600)
        minutes = str((self.time % 3600) // 60)
        seconds = str(self.time % 60)

        time = '0' * (2 - len(hours)) + hours + ':' + '0' * (2 - len(minutes)) + minutes + ':' + '0' * (2 - len(seconds)) + seconds

        self.lineEdit.setText(time)
