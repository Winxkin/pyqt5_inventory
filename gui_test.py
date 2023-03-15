from PyQt5 import QtWidgets


class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # set window properties
        self.setWindowTitle("Second Window")
        self.setGeometry(100, 100, 400, 300)


def show_second_window():
    second_window = SecondWindow()
    second_window.exec_()


app = QtWidgets.QApplication([])
main_window = QtWidgets.QMainWindow()
show_second_window_btn = QtWidgets.QPushButton("Show Second Window")
show_second_window_btn.clicked.connect(show_second_window)
main_window.setCentralWidget(show_second_window_btn)
main_window.show()
app.exec_()