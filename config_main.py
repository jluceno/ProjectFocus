# settings - project - python interpreter - pyqt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from config_classes import CommandWidget


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
        self.config()

    # modify the objects initialized in init
    def config(self):

        # config button 1
        self.b1.setText("press to send dictionary")
        self.b1.clicked.connect(self.clicked)
        self.b1.setGeometry(300, 0, 150, 30)

        # config line 1 and dropdown 1
        self.label1.setText("first param")
        self.label1.move(55, 50)
        self.dd1.setGeometry(200, 50, 250, 30)
        self.dd1.addItems(["item1", "item2", "item3"])

        # TODO config checklist1

        # test config_classes
        print(CommandWidget.add.value)

        test = CommandWidget(77)
        test.remove_widget()

        # pass testCommandWidget object to Josh's TaskManager.py function()
        # function pointer(?) will be passed to config_main.py

    def clicked(self):
        self.b1.setText("dictionary sent")


def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    # josh sends me a function to call if i want to run a command
    # josh will call win.register_command_function(function*(ofTypeCommandWidget))

    # josh needs to ask for:

    win.show()
    sys.exit(app.exec())


window()
