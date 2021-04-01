import os
import json
import threading
import time
from pathlib import Path
from constants import Constants

test = None

class Strava():
    input_miles = 0
    input_cals = 0
    total_input_miles = 0
    total_input_cals = 0
    lock = threading.Lock()
    auth_key = None

    def __init__(self):
        super().__init__()

##FULFILL
    @staticmethod
    def run_poll():

## CHANGE
    @staticmethod
    def JSON_pull():
        Strava.lock.acquire()
        cwd = os.getcwd()
        #remap
        os.chdir(Path('.', 'api', 'running_page').resolve())
        sync_token_run(Strava.auth_key)
        os.chdir(cwd)
        Strava.lock.release()

    # Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2
    ## CHANGE
    @staticmethod
    def GetLatests():
        Strava.lock.acquire()

        # Find the latest file
        files = []
        for file in Constants.PATH_TO_STRAVA_ACTIVITIES.iterdir():
            files.append(file)

        sorted_files = sorted(files)
        test = Path(sorted_files[-1]).open(mode='r')
        test2 = json.load(test)
        for i in test2['summaries']:
            if i['metric'] == 'distance':
                Strava.input_miles = i['value']
                Strava.input_miles = round(Strava.input_miles, 2)

            if i['metric'] == 'calories':
                Strava.input_cals = i['value']
                Strava.input_cals = round(Strava.input_cals, 2)
        Strava.lock.release()

    # Finds and returns totals for all JSON files combined.
    @staticmethod
    def GetTotals():
        Strava.lock.acquire()
        Strava.total_input_cals = 0
        Strava.total_input_miles = 0

        # Read all files
        files = []
        for file in Constants.PATH_TO_STRAVA_ACTIVITIES.iterdir():
            files.append(file)

        # Sort files and sum everything up
        sorted_files = sorted(files)
        for curr_file in sorted_files:
            test = Path(curr_file).open(mode='r')
            test2 = json.load(test)
            for i in test2['summaries']:
                if i['metric'] == 'distance':
                    temp_total = i['value']
                    Strava.total_input_miles += temp_total
                if i['metric'] == 'calories':
                    temp_total = i['value']
                    Strava.total_input_cals += temp_total
            Strava.total_input_miles = round(Strava.total_input_miles, 2)
            Strava.total_input_cals = round(Strava.total_input_cals, 2)
        Strava.lock.release()

    # Call these 4 functions for latest or total miles or calories. Totals functions are incomplete
    @staticmethod
    def LatestMiles():
        Strava.GetLatests()
        return Strava.input_miles

    @staticmethod
    def LatestCals():
        Strava.GetLatests()
        return Strava.input_cals

    @staticmethod
    def TotalMiles():
        Strava.GetTotals()
        return Strava.total_input_miles

    @staticmethod
    def TotalCals():
        Strava.GetTotals()
        return Strava.total_input_cals
