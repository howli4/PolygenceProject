import numpy as np
from noaa_sdk import NOAA
from suntime import Sun

class Plant():
    """Comment"""
    plant_facing = {
        'N': 100,
        'E': 500,
        'S': 1000,
        'W': 500
    }

    sun_dict = {  # https://www.takethreelighting.com/light-levels.html
        'Rain': 100,
        'Fog': 400,
        'Cloud': 700,
        'Sun': 1000
    }  

    plant_amnt = {
        'Snake Plant': 200,
        'Generic': 200
    }

    plant_freq = {
        'Snake Plant': 7,
        'Generic': 4
    }

    def __init__(self,
                 zipcode: int,
                 lat: float,
                 lon: float,
                 direction: str,
                 plant_type: str):
        self.zipcode = zipcode  
        self.lat = lat
        self.lon = lon
        self.direction = direction
        self.plant_type = plant_type

        # Setup default parameters
        self.seven_day_avg = np.array([0,0,0,0,0,0,0])
        self.count = 0
        self.total_count = 0
        self.adjusted_freq = 0

        self.init_watering_schedule()
        self.check_plant_direction()

    def init_watering_schedule(self) -> None:
        try:
            self.watering_freq = self.plant_freq[self.plant_type]
            self.watering_amount = self.plant_amnt[self.plant_type]
        except:
            raise ValueError("Plant not found in local list")
        
    def check_plant_direction(self) -> None:
        try:
            self.plant_direction = self.plant_facing[self.direction]
        except:
            raise ValueError("Use a cardinal direction N,E,W,S")
        
    def update(self):
        """Grab today's daily footcandle computation."""
        n = NOAA()
        res = n.get_forecasts(self.zipcode, 'US')  # update zipcode
        forecast = res[0]
        sun = forecast['shortForecast']
        print("Short Forecast: ", sun)
        sunSplit = sun.split()

        sunVal = 500
        for s in sunSplit:
            for v in self.sun_dict:
                if v in s:
                    sun_val= self.sun_dict[v]
                    break
        print("Base FC Value: ", sun_val)

        sun = Sun(self.lat, self.lon)
        today_sr, today_ss = sun.get_sunrise_time(), sun.get_sunset_time()
        total_sun = (today_ss - today_sr).seconds / 3600
        totalFC = (sunVal + self.plant_facing[self.direction]) * total_sun
        self.update_seven_day_avg(totalFC)

    def update_seven_day_avg(self, new_value):
        self.seven_day_avg = np.roll(self.seven_day_avg, 1)
        self.seven_day_avg[0] = new_value
        sun_avg = round(np.average(self.seven_day_avg))
        self.adjust_freq(sun_avg)

    def adjust_freq(self, sun_avg):
        maxFC = 30000 #15 hours * 2k FC
        minFC = 2000 #10 hours * 200 FC
        sunScale = np.interp(sun_avg, [minFC, maxFC], [-1, 1])
        if self.total_count < 7:
            adj_f = 0
        else:
            adj_f = self.watering_freq * sunScale

        self.adjusted_freq = round(adj_f + self.watering_freq)