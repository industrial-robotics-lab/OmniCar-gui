#!/usr/bin/env python3
from omni import *
import time

wheels_vels = [
    [10, 10, 10, 10],
    [50, 50, 50, 50],
    [80, 80, 80, 80],
    [120, 120, 120, 120],
    [80, 80, 80, 80],
    [40, 40, 40, 40],
    [10, 10, 10, 10],
    [-15, -15, -15, -15],
    [-50, -50, -50, -50],
]

car_vels = [
    [0, 2, 0],
    [0, -2, 0],
    [0, 0, 2],
    [0.05, 0, 0],
    [-0.05, 0, 0],
    [-0.02, 0, 0],
    [-0.005, 0, 0],
    [0, 0, 0]
]

# wheel diameter = 58.99mm
# wheel width = 30.54mm
car = Car(10, 20, 0.0589/2)


def print_vel():
    while not car.is_stop():
        # car.print_velocity()
        time.sleep(0.5)


printer = Thread(target=print_vel)
printer.start()

car.start_arduino_talk()
for vel in car_vels:
# for vel in wheels_vels:
#     car.set_wheels_velocities(vel)
    car.set_car_velocity(vel)
    print(f"Change vel to {vel}")
    time.sleep(2)
car.stop_arduino_talk()

printer.join()
