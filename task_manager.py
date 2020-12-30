import sys

from PyQt5.QtWidgets import QApplication

from config_model import TaskManagerConfigModel
from os import path
from constants import Constants
from config_main import MainWindow
from api_nike import Nike
from datetime import datetime
from config_classes import CommandMessage, CommandMessageNike
from flask_server import flask_server

import logging
import time
import os
import threading
import json


class TaskManager(threading.Thread):

    started = False
    config_class = None
    poll_interval_seconds = 5
    polling_threads = {}

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        super().__init__()

    # Main function of task manager
    @staticmethod
    def init():
        # Register any functions for the configuration interface
        TaskManager.config_class.register_command_func(TaskManager._command_function)

        # Load previous configuration or start a new one
        regenerate_file = False
        config_file = None

        if path.exists(Constants.CONFIG_FILE_PATH):
            config_file = open(Constants.CONFIG_FILE_PATH, "r")

            try:
                config_success = TaskManagerConfigModel.import_json(config_file.read())
            except json.JSONDecodeError:
                config_success = False

            if config_success:
                logging.debug("Successfully loaded config file")
            else:
                logging.error("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()
        else:
            regenerate_file = True

        if regenerate_file:
            if not path.exists('config'):
                os.makedirs('config')
            config_file = open(Constants.CONFIG_FILE_PATH, "w")
            config_file.write(TaskManagerConfigModel.generate_default_json())
            TaskManagerConfigModel.init_default_values()
            config_file.close()

        # Startup display class


        # Setup the display


        # Setup the flask server for the display
        flask_server.start_server()

        # Setup Nike API
        nike_thread = threading.Thread(target=Nike.run_poll)
        TaskManager.polling_threads["Nike"] = nike_thread

        if "Nike" in TaskManagerConfigModel.api_configs:
            nike_config = TaskManagerConfigModel.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            TaskManager.polling_threads["Nike"].start()


    @staticmethod
    def _polling_function():
        # Get the current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # TODO fix the logging level
        logging.info("Calling the polling function! " + dt_string)
        logging.info("NIKE_API:")
        logging.info("Latest calories:" + str(Nike.LatestCals()))
        logging.info("Latest miles:" + str(Nike.LatestMiles()))
        logging.info("Total calories:" + str(Nike.TotalCals()))
        logging.info("Total miles:" + str(Nike.TotalMiles()))
        time.sleep(TaskManager.poll_interval_seconds)

    def run(self):
        TaskManager.init()

        # Polling function
        while True:
            TaskManager._polling_function()

    @staticmethod
    # Adds a new api configuration
    def add_new_api(command):
        api_config_name = None
        api_config_data = None
        if command.api_name == "Nike":
            api_config_name = command.api_name
            api_config_data = {
                "username" : command.username,
                "password" : command.password,
                "goal_miles_total": command.goal_miles_total,
                "goal_calories_total": command.goal_calories_total,
                "goal_miles_week": command.goal_miles_week,
                "goal_calories_week": command.goal_calories_week,
                "goal_miles_month": command.goal_miles_month,
                "goal_calories_month": command.goal_calories_month}

        if api_config_name is not None and api_config_data is not None:
            TaskManagerConfigModel.api_configs[api_config_name] = api_config_data

            # TODO save the information in a file
            config_file = open(Constants.CONFIG_FILE_PATH, "w")
            config_file.write(TaskManagerConfigModel.to_json())
            config_file.close()

            # Run the Nike thread
            nike_config = TaskManagerConfigModel.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            TaskManager.polling_threads["Nike"].start()
            return True
        else:
            return None

    @staticmethod
    def _command_function(command: CommandMessage):
        result = TaskManager.add_new_api(command)
        if result is None:
            logging.error("Command from config UI not recognized")
