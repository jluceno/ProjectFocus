# settings - project - python interpreter - pyqt5

import sys

from PyQt5.QtWidgets import QComboBox, QWidget, QStackedWidget, QFormLayout, QLineEdit, \
    QRadioButton, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup

from config_classes import CommandMessageNike, CommandMessageGW, CommandMessageTimeular


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # init for stack_n1
        self.command_group1 = QButtonGroup(self)
        self.qrb_nr = QRadioButton("Remove")
        self.qrb_na = QRadioButton("Add")
        self.command_group1.addButton(self.qrb_nr)
        self.command_group1.addButton(self.qrb_na)
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
        self.command_group2 = QButtonGroup(self)
        self.qrb_gwr = QRadioButton("Remove")
        self.qrb_gwa = QRadioButton("Add")
        self.command_group2.addButton(self.qrb_gwr)
        self.command_group2.addButton(self.qrb_gwa)
        self.command_gw = QHBoxLayout()
        self.command_gw.addWidget(self.qrb_gwa)
        self.command_gw.addWidget(self.qrb_gwr)
        self.qle_gw2 = QLineEdit()
        self.qle_gw3 = QLineEdit()
        self.qle_gw4 = QLineEdit()
        self.qle_gw5 = QLineEdit()
        self.qle_gw6 = QLineEdit()
        self.qle_gw7 = QLineEdit()

        # init for stack_timeular
        self.command_group3 = QButtonGroup(self)
        self.qrb_tr = QRadioButton("Remove")
        self.qrb_ta = QRadioButton("Add")
        self.command_group3.addButton(self.qrb_tr)
        self.command_group3.addButton(self.qrb_ta)
        self.command_t = QHBoxLayout()
        self.command_t.addWidget(self.qrb_ta)
        self.command_t.addWidget(self.qrb_tr)

        self.qle_t2 = QLineEdit()
        self.qle_t3 = QLineEdit()

        self.time_group = QButtonGroup(self)
        self.qrb_td = QRadioButton("Daily")
        self.qrb_tw = QRadioButton("Weekly")
        self.qrb_tm = QRadioButton("Monthly")
        self.time_group.addButton(self.qrb_td)
        self.time_group.addButton(self.qrb_tw)
        self.time_group.addButton(self.qrb_tm)
        self.qle_t4 = QHBoxLayout()
        self.qle_t4.addWidget(self.qrb_td)
        self.qle_t4.addWidget(self.qrb_tw)
        self.qle_t4.addWidget(self.qrb_tm)

        self.qle_t5 = QLineEdit()
        self.qle_t6 = QLineEdit()
        self.qle_t7 = QLineEdit()

        self.butt = QPushButton("Press to send", self)

        self.setWindowTitle("Config UI")

        self.dd1 = QComboBox(self)
        self.dd1.insertItem(0, 'Nike')
        self.dd1.insertItem(1, 'Google Weather')
        self.dd1.insertItem(3, 'Timeular')
        # "timeular tracker"

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1ui()
        self.stack2ui()
        self.stack3ui()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

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
        layout.addRow("username", self.qle_n4)
        layout.addRow("password", self.qle_n5)
        layout.addRow("Graph Type", self.qle_n2)
        layout.addRow("Data Type", self.qle_n3)
        layout.addRow("Total Miles Goal", self.qle_n6)
        layout.addRow("Total Calories Goal", self.qle_n7)

        self.stack1.setLayout(layout)

    def stack2ui(self):
        layout = QFormLayout()

        layout.addRow(QLabel("Add/Remove"), self.command_gw)
        # numbers are out of order, because I wanted to move username and password up
        layout.addRow("username", self.qle_gw4)
        layout.addRow("password", self.qle_gw5)
        layout.addRow("Graph Type", self.qle_gw2)
        layout.addRow("Data Type", self.qle_gw3)
        layout.addRow("Latitude", self.qle_gw6)
        layout.addRow("Longitude", self.qle_gw7)

        self.stack2.setLayout(layout)

    def stack3ui(self):
        layout = QFormLayout()

        layout.addRow(QLabel("Add/Remove"), self.command_t)
        layout.addRow("username", self.qle_t2)
        layout.addRow("password", self.qle_t3)
        layout.addRow(QLabel("Daily/Weekly/Monthly"), self.qle_t4)
        layout.addRow("Name of Goal", self.qle_t5)
        layout.addRow("Goal Progress", self.qle_t6)
        layout.addRow("Goal To Reach", self.qle_t7)

        self.stack3.setLayout(layout)

    def button_clicked(self):

        # if self.combobox_name == nike
        if self.dd1.currentText() == 'Nike':
            stored_object = CommandMessageNike()

            stored_object.api_name = self.dd1.currentText()

            # check if QRB add isChecked, then update it in the object
            if self.qrb_na.isChecked():
                stored_object.command = self.qrb_na.text()
            if self.qrb_nr.isChecked():
                stored_object.command = self.qrb_nr.text()

            stored_object.graph_type = self.qle_n2.text()
            stored_object.data_type = self.qle_n3.text()
            stored_object.username = self.qle_n4.text()
            stored_object.password = self.qle_n5.text()
            stored_object.goal_miles = self.qle_n6.text()
            stored_object.goal_calories = self.qle_n7.text()

            self.com_func(stored_object)

            print(stored_object)

        if self.dd1.currentText() == 'Google Weather':
            stored_object = CommandMessageGW()

            stored_object.api_name = self.dd1.currentText()

            if self.qrb_gwa.isChecked():
                stored_object.command = self.qrb_gwa.text()
            if self.qrb_gwr.isChecked():
                stored_object.command = self.qrb_gwr.text()

            stored_object.graph_type = self.qle_gw2.text()
            stored_object.data_type = self.qle_gw3.text()
            stored_object.username = self.qle_gw4.text()
            stored_object.password = self.qle_gw5.text()
            stored_object.coordinate_lat = self.qle_gw6.text()
            stored_object.coordinate_long = self.qle_gw7.text()

            self.com_func(stored_object)

            print(stored_object)

        if self.dd1.currentText() == 'Timeular':
            stored_object = CommandMessageTimeular()

            stored_object.api_name = self.dd1.currentText()

            if self.qrb_ta.isChecked():
                stored_object.command = self.qrb_ta.text()
            if self.qrb_tr.isChecked():
                stored_object.command = self.qrb_tr.text()

            stored_object.username = self.qle_t2.text()
            stored_object.password = self.qle_t3.text()

            # check if daily, weekly, or monthly isChecked
            if self.qrb_td.isChecked():
                stored_object.time_range = self.qrb_td.text()
            if self.qrb_tw.isChecked():
                stored_object.time_range = self.qrb_tw.text()
            if self.qrb_tm.isChecked():
                stored_object.time_range = self.qrb_tm.text()

            stored_object.goal_label = self.qle_t5.text()
            stored_object.goal_progress = self.qle_t6.text()
            stored_object.goal_wanted = self.qle_t7.text()

            self.com_func(stored_object)

            print(stored_object)

    def com_func(self, obj):
        if self.command_function is not None:
            self.command_function(obj)
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
