# settings - project - python interpreter - pyqt5

import sys

from PyQt5.QtWidgets import QComboBox, QWidget, QStackedWidget, QFormLayout, QLineEdit, \
    QRadioButton, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout

from config_classes import CommandMessageNike, CommandMessageGW


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # init for stack_n1
        self.qrb_nr = QRadioButton("Remove")
        self.qrb_na = QRadioButton("Add")
        self.command_n = QHBoxLayout()
        self.command_n.addWidget(self.qrb_na)
        self.command_n.addWidget(self.qrb_nr)
        self.qle_n2 = QLineEdit()
        self.qle_n3 = QLineEdit()
        self.qle_n4 = QLineEdit()
        self.qle_n5 = QLineEdit()
        self.qle_n6 = QLineEdit()
        self.qle_n7 = QLineEdit()

        # init for stack_gw2
        self.qrb_gwr = QRadioButton("Remove")
        self.qrb_gwa = QRadioButton("Add")
        self.command_gw = QHBoxLayout()
        self.command_gw.addWidget(self.qrb_gwa)
        self.command_gw.addWidget(self.qrb_gwr)
        self.qle_gw2 = QLineEdit()
        self.qle_gw3 = QLineEdit()
        self.qle_gw4 = QLineEdit()
        self.qle_gw5 = QLineEdit()
        self.qle_gw6 = QLineEdit()
        self.qle_gw7 = QLineEdit()

        self.butt = QPushButton("Press to send", self)

        self.setWindowTitle("Config UI")

        self.dd1 = QComboBox(self)
        self.dd1.insertItem(0, 'Nike')
        self.dd1.insertItem(1, 'Google Weather')
        # "timeular tracker"

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1ui()
        self.stack2ui()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        box = QVBoxLayout(self)
        box.addWidget(self.dd1)
        box.addWidget(self.Stack)
        box.addWidget(self.butt)

        self.butt.clicked.connect(self.button_clicked)
        self.dd1.currentIndexChanged.connect(self.display)
        self.setGeometry(300, 300, 600, 300)

        # test config_classes

        # example dictionaries OUTDATED
        # example_dict = {
        #     "api_name": "Nike",
        #     "command": "add",
        #     "graph_type": "progress_bar",
        #     "data_type": "calories",
        #     "username": "uh",
        #     "password": "password"
        # }

        # example_u = {
        #     "api_name": "google_weather",
        #     "command": "add",
        #     "graph_type": "display_value",
        #     "data_type": "temperature",
        #     "coordinates": "30,40"
        # }

        # **list => not edited everywhere
        # test = CommandMessage(**example_dict)

        # Call to send a command
        self.command_function = None

    def stack1ui(self):
        layout = QFormLayout()

        layout.addRow(QLabel("Add/Remove"), self.command_n)
        layout.addRow("Graph Type", self.qle_n2)
        layout.addRow("Data Type", self.qle_n3)
        layout.addRow("username", self.qle_n4)
        layout.addRow("password", self.qle_n5)
        layout.addRow("Total Miles Goal", self.qle_n6)
        layout.addRow("Total Calories Goal", self.qle_n7)

        self.stack1.setLayout(layout)

    def stack2ui(self):
        layout = QFormLayout()

        layout.addRow(QLabel("Add/Remove"), self.command_gw)
        layout.addRow("Graph Type", self.qle_gw2)
        layout.addRow("Data Type", self.qle_gw3)
        layout.addRow("username", self.qle_gw4)
        layout.addRow("password", self.qle_gw5)
        layout.addRow("Latitude", self.qle_gw6)
        layout.addRow("Longitude", self.qle_gw7)

        self.stack2.setLayout(layout)

    def button_clicked(self):

        # if self.combobox_name == nike
        if self.dd1.currentText() == 'Nike':
            test_obj = CommandMessageNike()

            test_obj.api_name = self.dd1.currentText()

            # check if QRB add isChecked, then update it in the object
            if self.qrb_na.isChecked():
                test_obj.command = self.qrb_na.text()
            if self.qrb_nr.isChecked():
                test_obj.command = self.qrb_nr.text()

            test_obj.graph_type = self.qle_n2.text()
            test_obj.data_type = self.qle_n3.text()
            test_obj.username = self.qle_n4.text()
            test_obj.password = self.qle_n5.text()
            test_obj.goal_miles = self.qle_n6.text()
            test_obj.goal_calories = self.qle_n7.text()

            print(test_obj)

        if self.dd1.currentText() == 'Google Weather':
            test_obj = CommandMessageGW()

            test_obj.api_name = self.dd1.currentText()

            if self.qrb_gwa.isChecked():
                test_obj.command = self.qrb_gwa.text()
            if self.qrb_gwr.isChecked():
                test_obj.command = self.qrb_gwa.text()

            test_obj.graph_type = self.qle_gw2.text()
            test_obj.data_type = self.qle_gw3.text()
            test_obj.username = self.qle_gw4.text()
            test_obj.password = self.qle_gw5.text()
            test_obj.coordinate_lat = self.qle_gw6.text()
            test_obj.coordinate_long = self.qle_gw7.text()

            print(test_obj)

        # completed_message = CommandMessage(None, None, None, None, None, None)
        # if self.command_function is not None:
        #     self.command_function(completed_message)

        print("button pressed")

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
