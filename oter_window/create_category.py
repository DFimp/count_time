from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QMessageBox
from PyQt5.QtGui import QFont
import json


class Create(QWidget):
    def __init__(self):
        super().__init__()

        with open('data_time.json') as file:
            self.data_time = json.load(file)

        self.setWindowTitle('Создать категорию')
        self.setGeometry(500, 300, 100, 100)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        font_1 = QFont()
        font_1.setPointSize(10)

        font_2 = QFont()
        font_2.setPointSize(10)
        font_2.setBold(True)

        self.labelCategory = QLabel('\n'.join(list(self.data_time['decoding'].values())), self)
        self.labelCategory.setFont(font_1)

        label = QLabel('Имеющиеся категории:', self)
        label.setFont(font_2)

        self.lineEdit = QLineEdit()
        self.btn_save = QPushButton('Сохранить')
        self.btn_save.setFont(font_2)
        labelLineEdit = QLabel('Добавляемая категория', self)
        labelLineEdit.setFont(font_2)

        self.layout.addWidget(label, 0, 0, 1, 1)
        self.layout.addWidget(self.labelCategory, 0, 1, 1, 1)
        self.layout.addWidget(labelLineEdit, 1, 0, 1, 1)
        self.layout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.layout.addWidget(self.btn_save, 1, 2, 1, 1)

        self.btn_save.clicked.connect(self.save)

    def create_labelCategoty(self):
        self.labelCategory.setText('\n'.join(list(self.data_time['decoding'].values())))

    def save(self):
        text = self.lineEdit.text().capitalize()

        if (text in self.data_time['decoding'].values()):
            question = QMessageBox.information(self, '', 'Данная категория уже есть')

        elif not text:
            question = QMessageBox.information(self, '', 'Вы ничего не ввели\nПопробуйте ещё')

        else:
            category = max(list(self.data_time['decoding'].keys()))
            category = category[:-1] + str(int(category[-1:]) + 1)
            self.data_time['decoding'][category] = text
            question = QMessageBox.information(self, '', 'Категория успешно сохранена')
            self.lineEdit.clear()
            self.create_labelCategoty()
            with open('data_time.json', 'w') as file:
                json.dump(self.data_time, file, indent=4)