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


class Core(threading.Thread):

    started = False
    config_startup_flag = False
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

        Core.config_startup_flag = ConfigStore.startup()

        # Register any functions for the configuration interface
        if Core.config_startup_flag is False:
            Core.log_core.error("Config class is not set! Aborting")
            raise Exception("Config UI not set!")

        # Load previous configuration or start a new one
        startup_result = ConfigStore.startup()
        if startup_result is False:
            raise Exception("Cant load the config file")

        # Setup Nike API
        # TODO have a cleaner way of doing this
        Core.log_core.debug("Starting Nike thread")
        nike_thread = threading.Thread(target=Nike.run_poll)
        Core.polling_threads["Nike"] = nike_thread

        if ConfigStore.find_api("Nike"):
            nike_config = ConfigStore.find_api("Nike")
            if not nike_config is None:
                Nike.auth_key = nike_config["auth_data"]["authenticationKey"]
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
    def add_new_api(command : dict):
        api_config_name = None
        api_config_data = None
        ConfigStore.add_api("Nike", command["NikeCommand"])
        Nike.auth_key = ConfigStore.get_api("Nike")["auth_data"]["authenticationKey"]
        
        if (not Core.polling_threads["Nike"].is_alive()):
            Core.polling_threads["Nike"].start()

    @staticmethod
    def _command_function(command):
        result = Core.add_new_api(command)
        if result is None:
            Core.log_core.error("Command from config UI not recognized")

    @staticmethod
    def get_nike_data():
        if "Nike" in Core.polling_threads:
            Core.log_core.debug("Fetching Nike data!")
            nike_data = Nike.WeekMonthTotals()
            nike_dict = None
           
            if ConfigStore.find_api("Nike") is True:
                nike_config = ConfigStore.get_api("Nike")
                
                nike_dict = {"weekly_data": {
                    "mile_goal" : nike_config["weekly_goals"]["mile_goal"],
                    "calorie_goal" : nike_config["weekly_goals"]["calorie_goal"],
                    "current_miles" : nike_data[0],
                    "current_calories" : nike_data[1]
                    },
                    "monthly_data": {
                        "mile_goal" : nike_config["monthly_goals"]["mile_goal"],
                        "calorie_goal": nike_config["monthly_goals"]["calorie_goal"],
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