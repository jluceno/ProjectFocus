import logging
import sys

from PyQt5.QtWidgets import QApplication
from config_main import MainWindow
from task_manager import TaskManager


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug("Starting project focus")

    # Setup the UI
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    # Start the task manager thread
    tm = TaskManager()
    TaskManager.config_class = win
    tm.start()

    # Start the Qt application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

