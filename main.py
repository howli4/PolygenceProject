import pgeocode
from noaa_sdk import NOAA
import numpy as np
from suntime import Sun
import datetime
import pytz
import time

zipcode = input("Zipcode: ")
direction = input("Cardinal Direction (N,E,S,W): ")
plant = input("Plant: ")
lat = 0
lon = 0
sunDict = {  # https://www.takethreelighting.com/light-levels.html
    'Rain': 100,
    'Fog': 400,
    'Cloud': 700,
    'Sun': 1000
}
sevenAvg = np.array([0,0,0,0,0,0,0])
currCount = 0
totalDays = 0
wf = 0
wa = 0
adj_f = 0

def init():
    nomi = pgeocode.Nominatim('us')
    location = nomi.query_postal_code(zipcode)
    global lat, lon
    lat = location.get('latitude')
    lon = location.get('longitude')
    plantSetup()

def plantSetup():
    global wf, wa
    wf = 5 #days
    wa = 200 #ml

def computeFC():
    n = NOAA()
    res = n.get_forecasts(zipcode, 'US')  # update zipcode
    forecast = res[0]
    sun = forecast['shortForecast']
    print("Short Forecast: ", sun)
    sunSplit = sun.split()

    sunVal = 500
    for s in sunSplit:
        for v in sunDict:
            if v in s:
                sunVal = sunDict[v]
                break
    print("Base FC Value: ", sunVal)

    plantFacing = {
        'N': 100,
        'E': 500,
        'S': 1000,
        'W': 500
    }

    sun = Sun(lat, lon)
    today_sr, today_ss = sun.get_sunrise_time(), sun.get_sunset_time()
    total_sun = (today_ss - today_sr).seconds / 3600
    totalFC = (sunVal + plantFacing[direction]) * total_sun
    print("Total Sunlight: ", total_sun)
    print("Total FC Hours: ", totalFC)

    # maxFC = 30000 #15 hours * 2k FC
    # minFC = 2000 #10 hours * 200 FC
    # sunScale = np.interp(totalFC, [minFC, maxFC], [0, 1])
    # print("Scale of 0-1: ", sunScale)
    getAvg(totalFC)

def getAvg(newFC):
    global sevenAvg
    sevenAvg = np.roll(sevenAvg, 1)
    sevenAvg[0] = newFC
    avg = round(np.average(sevenAvg))
    print("Average: ", avg)
    print(sevenAvg)

def adjFreq():
    global wf, adj_f
    if totalDays < 7:
        adj_f = wf

def deliverWater():
    print("watered")
    promptUser()

def promptUser():
    print("refill")

def runLoop():
    global currCount, totalDays
    while True:
        # current_time = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
        # if current_time.hour == 12 and current_time.minute == 0 and current_time.second == 0:
        computeFC()
        currCount+=1
        totalDays+=1
        if currCount == adj_f:
            deliverWater()
            currCount = 0

        time.sleep(5)

init()
runLoop()



