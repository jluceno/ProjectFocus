import sys

from PyQt5.QtWidgets import QApplication

from config_model import TaskManagerConfigModel
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


class Core(threading.Thread):

    started = False
    config_class = None
    poll_interval_seconds = 5
    polling_threads = {}
    log_core = None

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        super().__init__()

    # Main function of task manager
    @staticmethod
    def init():
        Core.log_core = get_logging("main.tm", logging.DEBUG)
        # Register any functions for the configuration interface
        if Core.config_class is None:
            Core.log_core.error("Config class is not set! Aborting")
            raise Exception("Config UI not set!")
        Core.config_class.register_command_func(Core._command_function)

        # Load previous configuration or start a new one
        regenerate_file = False
        config_file = None

        if Constants.CONFIG_FILE_PATH.exists():
            config_file = Constants.CONFIG_FILE_PATH.open(mode='r')

            try:
                config_success = TaskManagerConfigModel.import_json(config_file.read())
            except json.JSONDecodeError:
                config_success = False

            if config_success:
                Core.log_core.debug("Successfully loaded config file")
            else:
                Core.log_core.error("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()
        else:
            regenerate_file = True

        if regenerate_file:
            Core.log_core.debug("Regenerating config file")
            config_path = Path('.', 'config')
            if not config_path.exists():
                config_path.mkdir()
            config_file = Constants.CONFIG_FILE_PATH.open('w')
            config_file.write(TaskManagerConfigModel.generate_default_json())
            TaskManagerConfigModel.init_default_values()
            config_file.close()

        # Setup Nike API
        # TODO have a cleaner way of doing this
        Core.log_core.debug("Starting Nike thread")
        nike_thread = threading.Thread(target=Nike.run_poll)
        Core.polling_threads["Nike"] = nike_thread

        if "Nike" in TaskManagerConfigModel.api_configs:
            nike_config = TaskManagerConfigModel.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            Core.polling_threads["Nike"].start()


    @staticmethod
    def _polling_function():
        # Get the current time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


        time.sleep(Core.poll_interval_seconds)

    def run(self):
        Core.init()

        # Polling function
        while True:
            Core._polling_function()

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
            config_file = Constants.CONFIG_FILE_PATH.open(mode='w')
            config_file.write(TaskManagerConfigModel.to_json())
            config_file.close()

            # Run the Nike thread
            nike_config = TaskManagerConfigModel.api_configs["Nike"]
            Nike.auth_key = nike_config["password"]
            Core.polling_threads["Nike"].start()
            return True
        else:
            return None

    @staticmethod
    def _command_function(command: CommandMessage):
        result = Core.add_new_api(command)
        if result is None:
            Core.log_core.error("Command from config UI not recognized")

    @staticmethod
    def get_nike_data():
        if "Nike" in Core.polling_threads:
            Core.log_core.debug("Fetching Nike data!")
            nike_data = Nike.WeekMonthTotals()
            nike_dict = {"weekly_data": {
                "mile_goal" : -1,
                "calorie_goal" : -1,
                "current_miles" : nike_data[0],
                "current_calories" : nike_data[1]
                },
                "monthly_data": {
                    "mile_goal" : -1,
                    "calorie_goal": -1,
                    "current_miles" : nike_data[2],
                    "current_calories" : nike_data[3]
                },
                "totals": {
                    "total_miles": Nike.TotalMiles(),
                    "total_calories": Nike.TotalCals()
                }
            }
            return json.dumps(nike_dict)