# Dynamic Plant Watering System
A dynamic plant watering system that utilizes data from the National Weather Service, as well as the plant's orientation and location to adjust watering frequency.\
<img src="https://github.com/howli4/PolygenceProject/blob/master/System%20Picture.jpg" alt="drawing" width="500"/>

## Materials
1. Towerpro SG90 Analog Servo (with a single servo arm)
2. 3 Female-Female Jumper Wires
3. [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) (with latest version of Raspberry Pi OS) **IMPORTANT: This project will _NOT_ work with a Raspberry Pi 5**
4. [3D Printed Parts](https://cad.onshape.com/documents/d2bddf53dcd5558dbb8bdeef/w/6d26f46bb79cac228e16e5e8/e/d892201bd4037640de4d20c5?renderMode=0&uiState=67101d823e284f6f3d667be1)
5. O-rings (5/16" ID, 7/16" OD, 1/16" Width)
6. Hot Glue Gun + Hot Glue Sticks
7. Internet Connection

## Hardware Setup
1. Export, slice, and 3D print all required parts.
2. Glue the actuator flap onto the servo arm and attach it to the SG90 servo. Make sure to rotate the arm so it is at -90 degrees.
3. Push an O-ring into the indent on the bottom of the reservoir, glue the servo into the mount, glue the servo and mount onto the bottom of the reservoir as shown in the CAD, and glue the supports in place.
5. Connect the servo's ground pin to one of the RPi's GPIO ground pins, the servo's power pin to one of the RPI's 5V supply pins, and the PWM pin to the RPi's GPIO pin 18.

## Software Setup
1. Install required packages.\
`sudo apt update`\
`pip install datetime pgeocode time gpiozero numpy noaa-sdk suntime pigpio`
2. Clone Github repository\
`cd <install location>`\
`git clone https://github.com/howli4/PolygenceProject.git`
3. Run the Python script\
`cd /PolygenceProject`\
`python main.py`
