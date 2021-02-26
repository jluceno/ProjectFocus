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
        startup_result = TaskManagerConfigModel.startup()
        if startup_result is False:
            raise Exception("Cant load the config file")

        # Setup Nike API
        # TODO have a cleaner way of doing this
        Core.log_core.debug("Starting Nike thread")
        nike_thread = threading.Thread(target=Nike.run_poll)
        Core.polling_threads["Nike"] = nike_thread

        if TaskManagerConfigModel.find_api("Nike"):
            nike_config = TaskManagerConfigModel.find_api("Nike")
            if not nike_config is None:
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

    @staticmethod
    def get_timeular_data():
        Core.log_core.debug("Fetching Timeular mock data!")
        time_data = {}
        time_data["current_activity"] = "Coding"
        time_data["current_weekly_prod_hours"] = 20
        time_data["weekly_prod_hour_goal"] = 40
        activities_map = {
                        "Class_Learning": 3.4,
                        "Coding": 1.2,
                        "Misc_Nonproductive": 0.4,
                        "Misc_Prod": 2.1,
                        "Morning_Routine": 1.0,
                        "Projects": 2.2,
                        "Resume_&_Job_Apps": 0.33,
                        "Work_Out": 1.0
                        }
        time_data["activity_list"] = activities_map

        return json.dumps(time_data)