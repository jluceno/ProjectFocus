# settings - project - python interpreter - pyqt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from config_classes import CommandMessage


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # initialize widgets inside init method
        self.b1 = QtWidgets.QPushButton(self)

        self.label1 = QtWidgets.QLabel(self)
        self.dd1 = QtWidgets.QComboBox(self)

        self.label2 = QtWidgets.QLabel(self)

        self.setGeometry(200, 200, 900, 600)

        self.setWindowTitle("hey")

        # call config function
        self.config()

        # Call to send a command
        self.command_function = None

    # modify the objects initialized in init
    def config(self):

        # config button 1
        self.b1.setText("press to send dictionary")
        self.b1.clicked.connect(self.clicked)
        self.b1.setGeometry(300, 0, 150, 30)

        # config line 1 and dropdown 1
        self.label1.setText("select api")
        self.label1.move(55, 50)
        self.dd1.setGeometry(200, 50, 250, 30)
        self.dd1.addItems(["nike", "google_weather"])

        # TODO config checklist1



        # test config_classes

        # example dictionaries
        example_dict = {
            "api_name": "Nike",
            "command": "add",
            "graph_type": "progress_bar",
            "data_type": "calories"
        }

        example_u = {
            "api_name": "google_weather",
            "command": "add",
            "graph_type": "display_value",
            "data_type": "temperature"
        }

        # **list => not edited everywhere
        test = CommandMessage(**example_dict)

    def clicked(self):
        self.b1.setText("dictionary sent")

    def register_command_func(self, command_function):
        self.command_function = command_function
        return

def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    # josh sends me a function to call if i want to run a command
    # josh will call win.register_command_function(function*(ofTypeCommandWidget))

    win.show()
    sys.exit(app.exec())


window()
