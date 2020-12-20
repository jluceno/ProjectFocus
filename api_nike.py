import os
import json
from constants import Constants

test = None


# See nike_sync.py for file pull script
# Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2


class Nike:
    input_miles = 0
    input_cals = 0
    total_input_miles = 0
    total_input_cals = 0

    def __init__(self, miles, cals):
        self.miles = miles
        self.cals = cals

# Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2
    @staticmethod
    def GetLatests():
        for x, y, files in os.walk(os.path.abspath(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES)):
            sorted_files = sorted(files)
            test = open(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES + '\\' + sorted_files[-1], "r")
            test2 = json.load(test)
            for i in test2['summaries']:
                if i['metric'] == 'distance':
                    Nike.input_miles = i['value']
                    Nike.input_miles = round(Nike.input_miles, 2)

                if i['metric'] == 'calories':
                    Nike.input_cals = i['value']
                    Nike.input_cals = round(Nike.input_cals, 2)
    @staticmethod
    def GetTotals():
        Nike.total_input_cals = 0
        Nike.total_input_miles = 0
        for x, y, files in os.walk(os.path.abspath(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES)):
            sorted_files = sorted(files)
            for curr_file in sorted_files:
                test = open(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES + '\\' + curr_file, "r")
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


# Call these 4 functions for latest or total miles or calories. Totals functions are incomplete
    @staticmethod
    def LatestMiles():
        Nike.GetLatests()
        print(Nike.input_miles)
        return Nike.input_miles

    @staticmethod
    def LatestCals():
        Nike.GetLatests()
        print(Nike.input_cals)
        return Nike.input_cals

    @staticmethod
    def TotalMiles():
        Nike.GetTotals()
        print(Nike.total_input_miles)
        return Nike.total_input_miles

    @staticmethod
    def TotalCals():
        Nike.GetTotals()
        print(Nike.total_input_cals)
        return Nike.total_input_cals
