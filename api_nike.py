import os
import json
import threading
import time
from constants import Constants
from api.running_page.scripts.nike_sync import run as sync_token_run

test = None


class Nike():
    input_miles = 0
    input_cals = 0
    total_input_miles = 0
    total_input_cals = 0
    lock = threading.Lock()
    auth_key = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def run_poll():
        while True:
            Nike.JSON_pull()
            time.sleep(1800)

# Populates 'activities' folder with JSON files. See https://github.com/yihong0618/running_page#nike-run-club for Key.
    @staticmethod
    def JSON_pull():
        Nike.lock.acquire()
        cwd = os.getcwd()
        os.chdir(".\\api\\running_page")
        sync_token_run(Nike.auth_key)
        os.chdir(cwd)
        Nike.lock.release()

# Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2
    @staticmethod
    def GetLatests():
        Nike.lock.acquire()
        for x, y, files in os.walk(os.path.abspath(os.curdir + '/' + Constants.PATH_TO_NIKE_ACTIVITIES)):
            sorted_files = sorted(files)
            test = open(os.curdir + '/' + Constants.PATH_TO_NIKE_ACTIVITIES + '/' + sorted_files[-1], "r")
            test2 = json.load(test)
            for i in test2['summaries']:
                if i['metric'] == 'distance':
                    Nike.input_miles = i['value']
                    Nike.input_miles = round(Nike.input_miles, 2)

                if i['metric'] == 'calories':
                    Nike.input_cals = i['value']
                    Nike.input_cals = round(Nike.input_cals, 2)
        Nike.lock.release()

# Finds and returns totals for all JSON files combined.
    @staticmethod
    def GetTotals():
        Nike.lock.acquire()
        Nike.total_input_cals = 0
        Nike.total_input_miles = 0
        for x, y, files in os.walk(os.path.abspath(os.curdir + '/' + Constants.PATH_TO_NIKE_ACTIVITIES)):
            sorted_files = sorted(files)
            for curr_file in sorted_files:
                test = open(os.curdir + '/' + Constants.PATH_TO_NIKE_ACTIVITIES + '/' + curr_file, "r")
                test2 = json.load(test)
                for i in test2['summaries']:
                    if i['metric'] == 'distance':
                        temp_total = i['value']
                        Nike.total_input_miles += temp_total
                    if i['metric'] == 'calories':
                        temp_total = i['value']
                        Nike.total_input_cals += temp_total
                Nike.total_input_miles = round(Nike.total_input_miles, 2)
                Nike.total_input_cals = round(Nike.total_input_cals, 2)
        Nike.lock.release()

# Call these 4 functions for latest or total miles or calories. Totals functions are incomplete
    @staticmethod
    def LatestMiles():
        Nike.GetLatests()
        return Nike.input_miles

    @staticmethod
    def LatestCals():
        Nike.GetLatests()
        return Nike.input_cals

    @staticmethod
    def TotalMiles():
        Nike.GetTotals()
        return Nike.total_input_miles

    @staticmethod
    def TotalCals():
        Nike.GetTotals()
        return Nike.total_input_cals
