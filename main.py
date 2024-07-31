from noaa_sdk import NOAA
from numpy import interp

n = NOAA()
res = n.get_forecasts('95064', 'US')  # update zipcode
forecast = res[1]
temp = forecast['temperature']
tempInterp = interp(temp, [30, 100], [1, 100])  # min temp max temp to 1-100
sun = forecast['shortForecast']
print("Temperature: ", temp)
print("Interpolated Temperature (30-100 to 1-100): ", tempInterp)
print("Short Forecast for Sun Intensity: ", sun)

# add more (potentially add dictionary of modifier words)
sunDict = {
    'Cloud': 0,
    'Fog': 0.5,
    'Sun': 1
}

# any way to make this more efficient?
sunSplit = sun.split()
sunVal = 0
for s in sunSplit:
    for v in sunDict:
        if v in s:
            sunVal = sunDict[v]
print("Sun Intensity Value: ", sunVal)

# come up with equation other than multiplying
finalVal = tempInterp * sunVal / 100
print("Final Value: ", finalVal)
