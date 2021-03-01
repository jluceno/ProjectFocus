import logging
import sys

from PyQt5.QtWidgets import QApplication
from config_main import MainWindow
from core import Core
from util import get_logging
from flask_server import FlaskServer

def main():
    main_log = get_logging("main", logging.DEBUG)
    main_log.debug("Starting project focus")

    # Start the task manager thread
    main_log.debug("Starting core")
    tm = Core()
    tm.start()

    # Start the flask server
    main_log.debug("Starting flask")
    flask = FlaskServer
    FlaskServer.start()


if __name__ == "__main__":
    main()