import os
import json
from constants import Constants

test = None
input_miles = 0
input_cals = 0

# Navigates through JSON files that have been pulled and returns miles and cals from most recent run. Rounds float to 2
for x, y, files in os.walk(os.path.abspath(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES)):
    test = open(os.curdir + Constants.PATH_TO_NIKE_ACTIVITIES + '\\' + files[0], "r")
    test2 = json.load(test)
    for i in test2['summaries']:
        if i['metric'] == 'distance':
            input_miles = i['value']
            input_miles = round(input_miles, 2)
        if i['metric'] == 'calories':
            input_cals = i['value']
            input_cals = round(input_cals, 2)


class Nike:

    def __init__(self, miles, cals):
        self.miles = miles
        self.cals = cals

# Call these 4 functions for latest or total miles or calories. Totals functions are incomplete
    def LatestMiles(self):
        print(self.miles)
        return self.miles

    def LatestCals(self):
        print(self.cals)
        return self.cals

# Still working on these
    def TotalMiles(self):
        return self.miles*2

    def TotalCals(self):
        return self.cals*2


nike = Nike(input_miles, input_cals)