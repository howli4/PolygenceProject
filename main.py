from datetime import datetime
import pgeocode
import time
from plant import Plant
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

def deliverWater(servo, watering_amount):
    servo.angle = -40
    time.sleep(20)
    servo.angle = -90
    promptUser(watering_amount)

def promptUser(amount):
    print("refill with ", amount, " ml of water")

if __name__ == "__main__":

    # Prompt user for setup
    zipcode = input("Zipcode: ")
    direction = input("Cardinal Direction (N,E,S,W): ")
    plant_type = input("Plant: ")

    # Find timezone from provided zipcode
    nomi = pgeocode.Nominatim('us')
    location = nomi.query_postal_code(zipcode)
    lat = location.get('latitude')
    lon = location.get('longitude')

    # Initialize the plant object
    my_plant = Plant(zipcode, lat, lon, direction, plant_type)

    #Initialize the servo
    servo = AngularServo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=PiGPIOFactory())
    servo.angle = -90

    # Run our iterative loop
    # TODO: check current time, subtract from noon, then 'sleep' for that long

    tz = datetime.now().astimezone().tzinfo
    current_time = datetime.now(tz)
    next_noon = datetime(year=current_time.year, month=current_time.month, day=current_time.day+1, hour=12, tzinfo=tz)
    wait_time = (next_noon-current_time).seconds
    time.sleep(wait_time)  # waiting until the next noon
    
    while True:
        my_plant.update()
        if my_plant.count == my_plant.adjusted_freq:
            deliverWater(servo, my_plant.watering_amount)
            my_plant.count = 0
        my_plant.total_count += 1
        my_plant.count += 1
        time.sleep(86400)  # 24 hours in seconds