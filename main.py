import pgeocode
from noaa_sdk import NOAA
import numpy as np
from matplotlib import pyplot as plt
from suntime import Sun

zipcode = 10001

nomi = pgeocode.Nominatim('us')
location = nomi.query_postal_code(zipcode)
lat = location.get('latitude')
lon = location.get('longitude')
print("Latitude: ", lat)
print("Longitude: ", lon)

n = NOAA()
res = n.get_forecasts(zipcode, 'US')  # update zipcode
forecast = res[0]
temp = forecast['temperature']
# tempInterp = np.interp(temp, [30, 100], [1, 100])
sun = forecast['shortForecast']
print("Temperature: ", temp)
# print("Interpolated Temperature: ", tempInterp)
print("Short Forecast: ", sun)

# add more (potentially add dictionary of modifier words)

# modDict = {
#     'Patchy': 0.25,
#     'Partly': 0.5,
#     'Mostly': 0.75,
# }

# any way to make this more efficient?

# come up with equation other than multiplying

# finalVal = tempInterp * sunVal * modVal / 100
#
# x = np.linspace(-1, 1, 1000)
# z = 1/(1 + np.exp(-5 * x))
# point = 1/(1 + np.exp(-5 * finalVal))
#
# plt.plot(x, z)
# plt.xlabel("x")
# plt.ylabel("Sigmoid(X)")
# plt.plot(finalVal, point, 'ro')
#
# plt.show()
#
# print("Final Value: ", finalVal)
# print("Sigmoid Value: ", point)

sunDict = {
    'Rain': 100,
    'Fog': 400,
    'Cloud': 700,
    'Sun': 1000
}

sunSplit = sun.split()
sunVal = 1
for s in sunSplit:
    for v in sunDict:
        if v in s:
            sunVal = sunDict[s]
            break

print("Base FC Value: ", sunVal)

plantFacing = {
    'North': 100,
    'East': 500,
    'South': 1000,
    'West': 500
}
plantDir = 'West'

sun = Sun(lat, lon)
today_sr, today_ss = sun.get_sunrise_time(), sun.get_sunset_time()
total_sun = (today_ss - today_sr).seconds / 3600
totalFC = (sunVal + plantFacing[plantDir]) * total_sun

print("Total Sunlight: ", total_sun)
print("Total FC Hours: ", totalFC)

maxFC = 30000 #15 hours * 2k FC
minFC = 2000 #10 hours * 200 FC
avgFC = 15000 #12 hours * 1200 FC
sunScale = np.interp(totalFC, [minFC, maxFC], [0, 1])
print("scale of 0-1: ", sunScale)

sevenDay = np.array([avgFC, avgFC, avgFC, avgFC, avgFC, avgFC, avgFC,])





