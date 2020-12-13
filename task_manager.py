import sys

from PyQt5.QtWidgets import QApplication

from config_model import TaskManagerConfigModel
from os import path
from constants import Constants
from config_main import MainWindow
from api_nike import Nike
from datetime import datetime
import logging
import time
import os
import threading


class TaskManager(threading.Thread):

    started = False
    config_class = None
    display_class = None
    window_thread = None
    poll_interval_seconds = 5
    config = None
    nike = None

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        super().__init__()

    # Main function of task manager
    @staticmethod
    def init():
        # Startup configure interface

        # Register any functions for the configuration interface

        # Load previous configuration or start a new one
        config = TaskManagerConfigModel()

        regenerate_file = False
        config_file = None

        if path.exists(Constants.CONFIG_FILE_PATH):
            config_file = open(Constants.CONFIG_FILE_PATH, "r")
            config_success = config.import_json(config_file.read())

            if config_success:
                logging.debug("Successfully loaded config file")
            else:
                logging.debug("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()
        else:
            regenerate_file = True

        if regenerate_file:
            os.makedirs('config')
            config_file = open(Constants.CONFIG_FILE_PATH, "w")
            config_file.write(TaskManagerConfigModel.generate_default_json())
            config.init_default_values()
            config_file.close()

        # Startup display class

        # Setup the display

        # Setup the Nike API

        # TODO call the API function to authenticate


    @staticmethod
    def _polling_function():
        # Get the current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        logging.debug("Calling the polling function! " + dt_string)
        logging.debug("NIKE_API:")
        logging.debug("Latest calories:" + str(Nike.LatestCals()))
        logging.debug("Latest miles:" + str(Nike.LatestMiles()))
        logging.debug("Total calories:" + str(Nike.TotalCals()))
        logging.debug("Total miles:" + str(Nike.TotalMiles()))
        time.sleep(TaskManager.poll_interval_seconds)

    def run(self):
        TaskManager.init()

        # Polling function
        while True:
            TaskManager._polling_function()

    # Adds a new configuration
    @staticmethod
    def add_widget_config(config_command):
        # Pause the polling thread

        # Update the configuration

        # Get data from the API for the new object

        # Resume the polling thread

        pass

    # Removes a configuration
    @staticmethod
    def remove_widget_config(config_command):
        # Pause the polling thread

        # Remove the config

        # Resume the polling thread
        pass

    # Gets the whole configuration of the application
    # Helps preview the current state of the display to the configuration
    @staticmethod
    def get_current_configuration():
        # Read and return the current configuration

        # Must remove all authentication data

        pass

    @staticmethod
    def _command_function(command):
        logging.debug("Command function hit!")
