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

    # receive from josh
    # pass in function pointer of self.command_handler
    def register_command(self):

        # josh is sending me command_handler function
        print(1)
        # takes commandmessage as an argument
        # call commandhandler, pass in commandmessage object

        # whenever i want to issue a command, call the function josh passed me

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

        # replace 'nike' with 'input'
        test_name = 1

        print(CommandMessage.ApiEnum(test_name).name)

        # pass api_name as only parameter for CommandMessage
        test = CommandMessage("nike")

        # print object's commands for CommandEnum
        print(test.ApiEnum.samsung.name)

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
