import requests
import http.client
import json
import time
from datetime import datetime
import mimetypes

#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Timeular:
    API_KEY = ""
    API_SECRET = ""
    tempAuth = ""
    Auth = ""
    AllActsReport = {}
    AllActsArray = []
    AllActsWeekTotals = []
    AllActsDayTotals = []
    TodayDateStr = 0
    TomorrowDateStr = 0
    SundayStr = 0
    StartTrackTime = 0
    EndTrackTime = 0
    DayReport = 0
    WeekReport = 0

    def __init__(self):
        super().__init__()

# Fetches Auth Token using API Key and API Secret. - Encrypt these in future, payload should be removed upon using Docker Secrets. Returns token as string
    @staticmethod
    def GetAuth():
        conn = http.client.HTTPSConnection("api.timeular.com")
        payload0 = f'\n  \"apiKey\"    : \"{Timeular.API_KEY}\",\n  \"apiSecret\" : \"{Timeular.API_SECRET}\"\n'
        payload = "{"+payload0+"}"
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v3/developer/sign-in", payload, headers)
        res = conn.getresponse()
        data = res.read()
        Timeular.tempAuth = data.decode("utf-8")
        Timeular.Auth = Timeular.tempAuth[10:58]
        print(Timeular.Auth)

# Lists all user-defined activities
    @staticmethod
    def GenAllActs():
        i = 0
        conn = http.client.HTTPSConnection("api.timeular.com")
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + Timeular.Auth
        }
        conn.request("GET", "/api/v3/activities", payload, headers)
        res = conn.getresponse()
        data = res.read()
        tempallacts = json.loads(data.decode("utf-8"))
        while i < 8:
            Timeular.AllActsReport[tempallacts['activities'][i]['id']] = tempallacts['activities'][i]['name']
            Timeular.AllActsArray.append(tempallacts['activities'][i]['name'])
            i += 1
        for i in Timeular.AllActsArray:
            print(i)

# Shows currently tracked activity
    @staticmethod
    def GenCurrAct():
        conn = http.client.HTTPSConnection("api.timeular.com")
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + Timeular.Auth
        }
        conn.request("GET", "/api/v3/tracking", payload, headers)
        res = conn.getresponse()
        data = res.read()
        tempcurract = json.loads(data.decode("utf-8"))
        if tempcurract['currentTracking'] != None:
            curract = tempcurract['currentTracking']['activityId']
            print('Currently tracking: ' + Timeular.AllActsReport[curract])
        else:
            print('Not currently tracking')

# Generates a report containing all the Time Entries from inside the given time range. If some Time Entry exceeds
# the report’s time range, only the matching part will be included. Requires Pro Timeular subscription
# Will be called once every 6 hours
    @staticmethod
    def GenWeekReport():
        conn = http.client.HTTPSConnection("api.timeular.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Timeular.Auth
        }
        conn.request("GET", f'/api/v3/report/data/{Timeular.SundayStr}T00:00:00.000/{Timeular.TodayDateStr}T23:59:59.999', payload, headers)
        res = conn.getresponse()
        data = res.read()
        Timeular.WeekReport = json.loads(data.decode("utf-8"))
        print(Timeular.WeekReport)

    # Generates JSON report of activity start/stop times for current day. +8 hour correction for PST
    @staticmethod
    def GenDayReport():
        conn = http.client.HTTPSConnection("api.timeular.com")
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + Timeular.Auth
        }
        conn.request("GET",
                     f'/api/v3/report/data/{Timeular.TodayDateStr}T08:00:00.000/{Timeular.TomorrowDateStr}T07:59:59.999',
                     payload, headers)
        res = conn.getresponse()
        data = res.read()
        Timeular.DayReport = json.loads(data.decode("utf-8"))

# Gathers totals of activities pulled from GenDayReport
    @staticmethod
    def DayTotals():

        for i in Timeular.DayReport['timeEntries']:
            StartTime = Timeular.DayReport['timeEntries'][i]['duration']['startedAt'][11:19]
            EndTime = Timeular.DayReport['timeEntries'][i]['duration']['stoppedAt'][11:19]
            FMT = '%H:%M:%S'
            Dur = datetime.strptime(EndTime, FMT) - datetime.strptime(StartTime, FMT)
            i =+ 1



        for i in Timeular.AllActsArray:
            print(i + ':' + Timeular.AllActsDayTotals[i])

# Updates Timeular class time variables
# time.struct_time (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    @staticmethod
    def UpdateTime():

        # Returns current date in YYYY-MM-DD format
        MonZero = 0
        MdayZero = 0
        CurrTime = time.localtime()
        TempTime = (CurrTime.tm_year, CurrTime.tm_mon, CurrTime.tm_mday, CurrTime.tm_hour, CurrTime.tm_min, CurrTime.tm_sec, CurrTime.tm_wday, CurrTime.tm_yday, CurrTime.tm_isdst)
        TempTime = list(TempTime)

        if TempTime[1] < 10:
            MonZero = 0
        else:
            MonZero = ''
        if TempTime[2] < 10:
            MdayZero = 0
        else:
            MdayZero = ''

        Timeular.TodayDateStr = f'{TempTime[0]}-{MonZero}{TempTime[1]}-{MdayZero}{TempTime[2]}'

        # Returns date of most recent Sunday in YYYY-MM-DD format
        TempTime1 = TempTime
        MonthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        SubtractBy = TempTime1[6] + 1
        Sunday = TempTime1[2] - SubtractBy
        if Sunday <= 0:
            TempTime1[1] = TempTime1[1] - 1
            if TempTime1[1] == 0:
                TempTime1[1] = 12
                TempTime1[0] = TempTime1[0] - 1
            Sunday = MonthDays[TempTime1[1] - 1] + Sunday

        if TempTime1[1] < 10:
            MonZero = 0
        else:
            MonZero = ''
        if Sunday < 10:
            MdayZero = 0
        else:
            MdayZero = ''

        Timeular.SundayStr = f'{TempTime1[0]}-{MonZero}{TempTime1[1]}-{MdayZero}{Sunday}'

        # Returns tomorrow's date in YYYY-MM-DD format
        TempTime = [CurrTime.tm_year, CurrTime.tm_mon, CurrTime.tm_mday]
        Tomorrow = TempTime[2] + 1
        if Tomorrow > MonthDays[TempTime[1] - 1]:
            Tomorrow = 1
            if TempTime[1] == 12:
                TempTime[1] = 1
                TempTime[0] = TempTime[0] + 1
        Timeular.TomorrowDateStr = f'{TempTime[0]}-{MonZero}{TempTime[1]}-{MdayZero}{Tomorrow}'
