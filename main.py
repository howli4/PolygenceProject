import datetime
import pytz
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
    # This is your main fcn
    # TODO: make this a python package

    # Prompt user for setup
    zipcode = input("Zipcode: ")
    direction = input("Cardinal Direction (N,E,S,W): ")
    plant_type = input("Plant: ")

    # Initialize the plant object
    my_plant = Plant(zipcode, direction, plant_type)

    #Initialize the servo
    servo = AngularServo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=PiGPIOFactory())
    servo.angle = -90

    # Run our iterative loop
    # TODO: check current time, subtract from noon, then 'sleep' for that long
    while True:
        current_time = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
        if current_time.hour == 12 and current_time.minute == 0 and current_time.second == 0:
            my_plant.update()
            if my_plant.count == my_plant.adjusted_freq:
                deliverWater(servo, my_plant.watering_amount)
                my_plant.count = 0
            my_plant.total_count += 1
            my_plant.count += 1