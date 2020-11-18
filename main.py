#!/usr/bin/env python3
from omni import *
import time

vals = [
    [50, 50, 50, 50],
    [50, 50, 50, 50],
    [80, 80, 80, 80],
    [120, 120, 120, 120],
    [80, 80, 80, 80],
    [40, 40, 40, 40],
    [10, 10, 10, 10],
    [-15, -15, -15, -15],
    [-50, -50, -50, -50],
]


car = Car()


def print_vel():
    while not car.is_stop():
        car.print_velocity()
        time.sleep(0.5)


printer = Thread(target=print_vel)
printer.start()

car.start_arduino_talk()
for val in vals:
    car.set_wheels_velocities(val)
    print(f"Change vel to {val}")
    time.sleep(1)
car.stop_arduino_talk()

printer.join()
