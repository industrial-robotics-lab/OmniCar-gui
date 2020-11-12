#!/usr/bin/env python3
from omni import *
import time

car = Car()
car.start_arduino_talk()
for i in range(5):
    car.print_velocity()
    time.sleep(0.5)
car.stop_arduino_talk()
car.print_velocity()
