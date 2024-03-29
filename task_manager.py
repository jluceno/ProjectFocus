import sys

from PyQt5.QtWidgets import QApplication

from config_model import ConfigStore
from pathlib import Path
from constants import Constants
from config_main import MainWindow
from api_nike import Nike
from datetime import datetime
from config_classes import CommandMessage, CommandMessageNike

import logging
import time
import os
import threading
import json
from util import get_logging


class TaskManager(threading.Thread):

    started = False
    config_class = None
    poll_interval_seconds = 5
    polling_threads = {}
    log_tm = None

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        super().__init__()

    # Main function of task manager
    @staticmethod
    def init():
        TaskManager.log_tm = get_logging("main.tm", logging.DEBUG)
        # Register any functions for the configuration interface
        if TaskManager.config_class is None:
            TaskManager.log_tm.error("Config class is not set! Aborting")
            raise Exception("Config UI not set!")
        TaskManager.config_class.register_command_func(TaskManager._command_function)

        # Load previous configuration or start a new one
        regenerate_file = False
        config_file = None

        if Constants.CONFIG_FILE_PATH.exists():
            config_file = Constants.CONFIG_FILE_PATH.open(mode='r')

            try:
                config_success = ConfigStore.import_json(config_file.read())
            except json.JSONDecodeError:
                config_success = False

            if config_success:
                TaskManager.log_tm.debug("Successfully loaded config file")
            else:
                TaskManager.log_tm.error("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()
        else:
            regenerate_file = True

        if regenerate_file:
            TaskManager.log_tm.debug("Regenerating config file")
            config_path = Path('.', 'config')
            if not config_path.exists():
                config_path.mkdir()
            config_file = Constants.CONFIG_FILE_PATH.open('w')
            config_file.write(ConfigStore.generate_default_json())
            ConfigStore.init_default_values()
            config_file.close()

        # Setup Nike API
        # TODO have a cleaner way of doing this
        TaskManager.log_tm.debug("Starting Nike thread")
        nike_thread = threading.Thread(target=Nike.run_poll)
        TaskManager.polling_threads["Nike"] = nike_thread

        if "Nike" in ConfigStore.api_configs:
            nike_config = ConfigStore.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            TaskManager.polling_threads["Nike"].start()


    @staticmethod
    def _polling_function():
        # Get the current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


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
            ConfigStore.api_configs[api_config_name] = api_config_data

            # TODO save the information in a file
            config_file = Constants.CONFIG_FILE_PATH.open(mode='w')
            config_file.write(ConfigStore.to_json())
            config_file.close()

            # Run the Nike thread
            nike_config = ConfigStore.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            TaskManager.polling_threads["Nike"].start()
            return True
        else:
            return None

    @staticmethod
    def _command_function(command: CommandMessage):
        result = TaskManager.add_new_api(command)
        if result is None:
            TaskManager.log_tm.error("Command from config UI not recognized")

    @staticmethod
    def get_nike_data():
        if "Nike" in TaskManager.polling_threads:
            TaskManager.log_tm.debug("Fetching Nike data!")
            nike_dict = { "latest_calories" : Nike.LatestCals(),
                "latest_miles": Nike.LatestMiles(),
                "total_calories": Nike.TotalCals(),
                "total_miles" : Nike.TotalMiles()}
            return json.dumps(nike_dict)