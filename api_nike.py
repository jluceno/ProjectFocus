import os
import json
import threading
import time
import datetime
from datetime import datetime
from datetime import timezone
from pathlib import Path
from constants import Constants
from api.running_page.scripts.nike_sync import run as sync_token_run

test = None


class Nike():
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
        os.chdir(Path('.', 'api', 'running_page').resolve())
        sync_token_run(Nike.auth_key)
        os.chdir(cwd)
        Nike.lock.release()

    # Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2
    @staticmethod
    def GetLatests():
        Nike.lock.acquire()
        
        # Find the latest file
        files = []
        for file in Constants.PATH_TO_NIKE_ACTIVITIES.iterdir():
            files.append(file)

        sorted_files = sorted(files)
        test = Path(sorted_files[-1]).open(mode = 'r')
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

        # Read all files
        files = []
        for file in Constants.PATH_TO_NIKE_ACTIVITIES.iterdir():
            files.append(file)

        # Sort files and sum everything up
        sorted_files = sorted(files)
        for curr_file in sorted_files:
            test = Path(curr_file).open(mode = 'r')
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
        Nike.month_stamp = dt.timestamp() * 1000
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
        Nike.week_stamp = dt.timestamp() * MillisecondConv
        PacificUnixConv = 28800000
        Nike.month_stamp = Nike.month_stamp - PacificUnixConv
        Nike.week_stamp = Nike.week_stamp - PacificUnixConv

        #Compare files greater than sunday stamp, total their values
        for file in Constants.PATH_TO_NIKE_ACTIVITIES.iterdir():
            FileUnix = str(file).split("\\")
            FileUnix = FileUnix[3].split(".")
            FileUnix = int(FileUnix[0]) - PacificUnixConv
            if FileUnix > Nike.month_stamp:
                curr_file = Path(file).open(mode='r')
                curr_file = json.load(curr_file)
                for i in curr_file['summaries']:
                    if i['metric'] == 'distance':
                        temp_total = i['value']
                        print(temp_total)
                        Nike.month_miles += temp_total
                    if i['metric'] == 'calories':
                        temp_total = i['value']
                        Nike.month_cals += temp_total
                Nike.month_miles = round(Nike.month_miles, 2)
                Nike.month_cals = round(Nike.month_cals, 2)
            if FileUnix > Nike.week_stamp:
                curr_file = Path(file).open(mode='r')
                curr_file = json.load(curr_file)
                for i in curr_file['summaries']:
                    if i['metric'] == 'distance':
                        temp_total = i['value']
                        Nike.week_miles += temp_total
                    if i['metric'] == 'calories':
                        temp_total = i['value']
                        Nike.week_cals += temp_total
                Nike.week_miles = round(Nike.week_miles, 2)
                Nike.week_cals = round(Nike.week_cals, 2)

# Call these 5 functions for latest or total miles or calories.
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

# Returns weekly miles, weekly caloris, monthly miles, and monthly calories in a tuple.
    @staticmethod
    def WeekMonthTotals():
        Nike.GetLatests()
        Nike.GetTimes()
        return(Nike.week_miles, Nike.week_cals, Nike.month_miles, Nike.month_cals)