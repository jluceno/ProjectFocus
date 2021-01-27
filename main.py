import logging
import sys

from PyQt5.QtWidgets import QApplication
from config_main import MainWindow
from task_manager import TaskManager
from util import get_logging
from flask_server import FlaskServer

def main():
    main_log = get_logging("main", logging.DEBUG)
    main_log.debug("Starting project focus")

    # Setup the UI
    main_log.debug("Starting the config UI")
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    # Start the task manager thread
    main_log.debug("Starting core")
    tm = TaskManager()
    TaskManager.config_class = win
    tm.start()

    # Start the flask server
    main_log.debug("Starting flask")
    flask = FlaskServer
    FlaskServer.start()

    # Start the Qt application
    main_log.debug("Launching Qt application")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()