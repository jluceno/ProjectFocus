# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random as rand

# Variables written in snake case, classes and objects in camel case

# replace with API pull, JSON format, retrieval of info.

# input_miles = rand.randint(0, 10)
# input_cals = rand.randint(100, 1000)

input_miles = 10
input_cals = 500


class Nike:

    current_miles = input_miles
    current_cals = input_cals
    total_miles = 0
    total_cals = 0

    def __init__(self, miles, cals):
        self.miles = miles
        self.cals = cals

# pulls JSON, retrieves miles and cals, refreshes last run info
    def pull(self):
        print()

# Refreshes totals with new run info
    def refreshTotals(self):
        print('test')
        self.total_miles = self.current_miles + self.total_miles
        self.total_cals = self.current_cals + self.total_miles
        print(self.total_miles)

    def printMiles(self):

        print(self.miles)

    def printCals(self):
        print(self.cals)


NikeLast = Nike(Nike.current_miles, Nike.current_cals)

NikeTotal = Nike(Nike.total_miles, Nike.total_cals)

NikeLast.printMiles()
NikeTotal.printMiles()
NikeTotal.refreshTotals()
NikeTotal.refreshTotals()