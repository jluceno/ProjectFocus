import sys

from PyQt5.QtWidgets import QApplication

from config_model import ConfigStore
from pathlib import Path
from constants import Constants
from config_main import MainWindow
from api_strava import Strava
from datetime import datetime

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

        # Setup Strava API
        # TODO have a cleaner way of doing this
        Core.log_core.debug("Starting Strava thread")
        strava_thread = threading.Thread(target=Strava.run_poll)
        Core.polling_threads["Strava"] = strava_thread

        if ConfigStore.find_api("Strava"):
            strava_config = ConfigStore.get_api("Strava")
            if not strava_config is None:
                Strava.auth_key = strava_config["auth_data"]["authenticationKey"]
                Core.polling_threads["Strava"].start()


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

        if "StravaCommand" in command:
            ConfigStore.add_api("Strava", command["StravaCommand"])
            Strava.auth_key = ConfigStore.get_api("Strava")["auth_data"]["authenticationKey"]
            if (not Core.polling_threads["Strava"].is_alive()):
                Core.polling_threads["Strava"].start()
        elif "WeatherCommand" in command:
            ConfigStore.add_api("Weather", command["WeatherCommand"])

    @staticmethod
    def _command_function(command):
        result = Core.add_new_api(command)
        if result is None:
            Core.log_core.error("Command from config UI not recognized")

    @staticmethod
    def get_strava_data():
        if "Strava" in Core.polling_threads:
            Core.log_core.debug("Fetching Strava data!")
            strava_data = Strava.WeekMonthTotals()
            strava_dict = None
           
            if ConfigStore.find_api("Strava") is True:
                strava_config = ConfigStore.get_api("Strava")
                
                strava_dict = {"weekly_data": {
                    "mile_goal" : strava_config["weekly_goals"]["mile_goal"],
                    "calorie_goal" : strava_config["weekly_goals"]["calorie_goal"],
                    "current_miles" : strava_data[0],
                    "current_calories" : strava_data[1]
                    },
                    "monthly_data": {
                        "mile_goal" : strava_config["monthly_goals"]["mile_goal"],
                        "calorie_goal": strava_config["monthly_goals"]["calorie_goal"],
                        "current_miles" : strava_data[2],
                        "current_calories" : strava_data[3]
                    },
                    "totals": {
                        "total_miles": Strava.TotalMiles(),
                        "total_calories": Strava.TotalCals()
                    }
                }
            return json.dumps(strava_dict)

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