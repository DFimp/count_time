from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QCheckBox, QLabel


class Look_data(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel('Жопа')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)



# import sys
# app = QApplication(sys.argv)
#
# window = See_data()
#
# window.show()
#
# app.exec_()
