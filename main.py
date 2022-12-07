from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QApplication
import sys

from function.fill_json import fill_past_date
from windows.main_window import MainWindow
from windows.stopwatch_window import TimerWindow
from windows.record_window import Add
from windows.look_window import Look_data
from windows.create_window import CreateWindow


today = QDate.currentDate().toString(Qt.ISODate)
fill_past_date(today, 'data_time.json')


def launch(start_win, stop_win):
    start_win.show()
    stop_win.close()


def launch_record():
    text = list(map(int, window_stopwatch.lineEdit.text().split(':')))
    window_stopwatch.reset()
    window_record.record_time_edit(time=text)
    window_stopwatch.close()
    window_record.show()


def launch_create():
    window_record.comboBox.clear()
    window_record.create_push_button_category()


app = QApplication(sys.argv)
window = MainWindow()
window_stopwatch = TimerWindow()
window_record = Add()
window_create = CreateWindow()
window_look = Look_data()
window.show()


# Attaching functions to a button in the main menu
window.btn_stopwatch.clicked.connect(lambda clicked, start_win=window_stopwatch, stop_win=window:
                                     launch(start_win, stop_win))
window.btn_add_data.clicked.connect(lambda clicked, start_win=window_record, stop_win=window:
                                    launch(start_win, stop_win))
window.btn_create_categories.clicked.connect(lambda clicked, start_win=window_create, stop_win=window:
                                             launch(start_win, stop_win))
window.btn_look_data.clicked.connect(lambda clicked, start_win=window_look, stop_win=window:
                                     launch(start_win, stop_win))


window_stopwatch.btn_menu.clicked.connect(lambda clicked, start_win=window, stop_win=window_stopwatch:
                                          launch(start_win, stop_win))
window_stopwatch.btn_record.clicked.connect(launch_record)


window_record.btn_menu.clicked.connect(lambda clicked, start_win=window, stop_win=window_record:
                                       launch(start_win, stop_win))
window_record.btn_create.clicked.connect(lambda clicked, start_win=window_create, stop_win=window_record:
                                         launch(start_win, stop_win))


window_create.btn_menu.clicked.connect(lambda clicked, start_win=window, stop_win=window_create:
                                       launch(start_win, stop_win))
window_create.btn_save.clicked.connect(launch_create)


window_look.btn_menu.clicked.connect(lambda clicked, start_win=window, stop_win=window_look:
                                     launch(start_win, stop_win))


sys.exit(app.exec_())