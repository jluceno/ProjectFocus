import os
import json
import threading
import time
import datetime
from datetime import datetime
from datetime import timezone
from pathlib import Path
from constants import Constants

test = None

class Strava():
    input_miles = 0
    input_cals = 0
    total_input_miles = 0
    total_input_cals = 0
    lock = threading.Lock()
    week_stamp = 0
    week_miles = 0
    week_cals = 0
    month_stamp = 0
    month_miles = 0
    month_cals = 0
    auth_key = None

    def __init__(self):
        super().__init__()

##FULFILL
    @staticmethod
    def run_poll():
        return

## CHANGE
    @staticmethod
    def JSON_pull():
        Strava.lock.acquire()
        cwd = os.getcwd()
        #remap
        os.chdir(Constants.PATH_TO_STRAVA_ACTIVITIES.resolve())
        # sync_token_run(Strava.auth_key) UPDATE TO STRAVA METHOD
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
            # Compares current time to unix time of JSON and categorizes JSON as "this week" or "this month"
    @staticmethod
    def GetTimes():

        #Convert currtime to first of month and last sunday
        TempTime = time.localtime()
        CurrTime = (TempTime.tm_year, TempTime.tm_mon, TempTime.tm_mday, TempTime.tm_hour, TempTime.tm_min, TempTime.tm_sec, TempTime.tm_wday, TempTime.tm_yday, TempTime.tm_isdst)
        CurrTime = list(CurrTime)
        TempTime1 = CurrTime
        MonthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if TempTime1[1] < 10:
            MonZero = '0'
        else:
            MonZero = ''
        FirstOfMonthDate = (str(TempTime1[0])+MonZero+str(TempTime1[1])+'01')
        dt = datetime.strptime(FirstOfMonthDate, '%Y%m%d')
        Strava.month_stamp = dt.timestamp() * 1000
        #Sunday
        SubtractBy = TempTime1[6] + 1
        Sunday = TempTime1[2] - SubtractBy
        if Sunday <= 0:
            TempTime1[1] = TempTime1[1] - 1
            if TempTime1[1] == 0:
                TempTime1[1] = 12
                TempTime1[0] = TempTime1[0] - 1
            Sunday = MonthDays[TempTime1[1] - 1] + Sunday
        if TempTime1[1] < 10:
            MonZero = '0'
        else:
            MonZero = ''
        if Sunday < 10:
            DayZero = '0'
        else:
            DayZero = ''
        SundayDate = (str(TempTime1[0])+MonZero+str(TempTime1[1])+DayZero+str(Sunday))

        #Convert sunday time to unix stamp, convert to PST
        dt = datetime.strptime(SundayDate, '%Y%m%d')
        MillisecondConv = 1000
        Strava.week_stamp = dt.timestamp() * MillisecondConv
        PacificUnixConv = 28800000
        Strava.month_stamp = Strava.month_stamp - PacificUnixConv
        Strava.week_stamp = Strava.week_stamp - PacificUnixConv

        #Compare files greater than sunday stamp, total their values
        for file in Constants.PATH_TO_STRAVA_ACTIVITIES.iterdir():
            FileUnix = float(file.stem)
            if FileUnix > Strava.month_stamp:
                curr_file = Path(file).open(mode='r')
                curr_file = json.load(curr_file)
                for i in curr_file['summaries']:
                    if i['metric'] == 'distance':
                        temp_total = i['value']
                        print(temp_total)
                        Strava.month_miles += temp_total
                    if i['metric'] == 'calories':
                        temp_total = i['value']
                        Strava.month_cals += temp_total
                Strava.month_miles = round(Strava.month_miles, 2)
                Strava.month_cals = round(Strava.month_cals, 2)
            if FileUnix > Strava.week_stamp:
                curr_file = Path(file).open(mode='r')
                curr_file = json.load(curr_file)
                for i in curr_file['summaries']:
                    if i['metric'] == 'distance':
                        temp_total = i['value']
                        Strava.week_miles += temp_total
                    if i['metric'] == 'calories':
                        temp_total = i['value']
                        Strava.week_cals += temp_total
                Strava.week_miles = round(Strava.week_miles, 2)
                Strava.week_cals = round(Strava.week_cals, 2)

# Call these 5 functions for latest or total miles or calories.

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

# Returns weekly miles, weekly calories, monthly miles, and monthly calories in a tuple.
    @staticmethod
    def WeekMonthTotals():
        Strava.GetLatests()
        Strava.GetTimes()
        return(Strava.week_miles, Strava.week_cals, Strava.month_miles, Strava.month_cals)

