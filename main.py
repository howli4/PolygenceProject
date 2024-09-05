import pgeocode
from noaa_sdk import NOAA
import numpy as np
from suntime import Sun
import datetime
import pytz
import time
from plant import Plant


def deliverWater():
    print("watered")
    promptUser()

def promptUser():
    print("refill")

if __name__ == "__main__":
    # This is your main fcn
    # TODO: make this a python package

    # Prompt user for setup
    zipcode = input("Zipcode: ")
    direction = input("Cardinal Direction (N,E,S,W): ")
    plant_type = input("Plant: ")

    # Initialize the plant object
    my_plant = Plant(zipcode, direction, plant_type)

    # Run our iterative loop
    # TODO: check current time, subtract from noon, then 'sleep' for that long
    while True:
        current_time = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
        if current_time.hour == 12 and current_time.minute == 0 and current_time.second == 0:
            my_plant.update()
            if my_plant.count == my_plant.adjusted_freq:
                deliverWater()
                my_plant.count = 0
            my_plant.total_count += 1


