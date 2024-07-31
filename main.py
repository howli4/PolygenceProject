from noaa_sdk import NOAA
from numpy import interp

n = NOAA()
# res = n.get_forecasts('95064', 'US')  # update zipcode
# forecast = res[0]
# temp = forecast['temperature']
temp = 67
tempInterp = interp(temp, [30, 100], [1, 100])  # min temp max temp to 1-100
# sun = forecast['shortForecast']
sun = 'Partly Cloudy'
print("Temperature: ", temp)
print("Interpolated Temperature (30-100 to 1-100): ", tempInterp)
print("Short Forecast for Sun Intensity: ", sun)

# add more (potentially add dictionary of modifier words)
sunDict = {
    'Cloud': 0.25,
    'Fog': 0.5,
    'Sun': 1
}

modDict = {
    'Patchy': 0.25,
    'Partly': 0.5,
    'Mostly': 0.75,
}

# any way to make this more efficient?
sunSplit = sun.split()
sunVal = 0
modVal = 0
for s in sunSplit:
    for v in sunDict:
        if v in s:
            sunVal = sunDict[v]
    for m in modDict:
        if m in s:
            modVal = modDict[m]
print("Sun Intensity Value: ", sunVal)
print("Sun Intensity Modifier: ", modVal)

# come up with equation other than multiplying
finalVal = tempInterp * sunVal * modVal / 100
print("Final Value: ", finalVal)
