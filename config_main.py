# settings - project - python interpreter - pyqt5

import sys
from PyQt5.QtWidgets import QComboBox, QWidget, QStackedWidget, QHBoxLayout, QFormLayout, QLineEdit, \
    QRadioButton, QLabel, QApplication, QVBoxLayout

from config_classes import CommandMessage


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Config UI")

        self.dd1 = QComboBox(self)

        self.dd1.insertItem(0, 'Nike')
        self.dd1.insertItem(1, 'Google Weather')

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1ui()
        self.stack2ui()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        box = QHBoxLayout(self)
        box.addWidget(self.dd1)
        box.addWidget(self.Stack)

        self.dd1.currentIndexChanged.connect(self.display)
        self.setGeometry(300, 300, 600, 300)

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

        # Call to send a command
        self.command_function = None

    def stack1ui(self):
        layout = QFormLayout()
        layout.addRow("API Name", QLineEdit())

        command = QHBoxLayout()
        command.addWidget(QRadioButton("Add"))
        command.addWidget(QRadioButton("Remove"))
        layout.addRow(QLabel("Add/Remove"), command)

        layout.addRow("Graph Type", QLineEdit())
        layout.addRow("Data Type", QLineEdit())
        self.stack1.setLayout(layout)

    def stack2ui(self):
        layout = QFormLayout()
        layout.addRow("API Name", QLineEdit())

        command = QHBoxLayout()
        command.addWidget(QRadioButton("Add"))
        command.addWidget(QRadioButton("Remove"))
        layout.addRow(QLabel("Add/Remove"), command)

        layout.addRow("Graph Type", QLineEdit())
        layout.addRow("Data Type", QLineEdit())
        self.stack2.setLayout(layout)

    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def register_command_func(self, command_function):
        self.command_function = command_function
        return


def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    # josh sends me a function to call if i want to run a command
    # josh will call win.register_command_function(function*(ofTypeCommandWidget))

    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
