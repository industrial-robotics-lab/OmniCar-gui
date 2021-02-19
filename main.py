#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from omni import *
import time

theta = []
x = []
y = []

def switch_vels():
    for vel in car_vels:
        car.set_car_velocity(vel)
        print(f"Change vel to {vel}")
        time.sleep(2)

def get_feedback():
    while not car.is_stop():
        vel = car.get_velocity()
        vel = vel.ravel().tolist()
        # print(f"vel: {vel}")
        theta.append(vel[0])
        x.append(vel[1])
        y.append(vel[2])
        time.sleep(0.1)

def animate(i):
    plt.cla() # clear axis (keep line the same color on each iteration)
    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval=1000) # get current figure

switcher = Thread(target=switch_vels)
feedbacker = Thread(target=get_feedback)

car_vels = [
    [0, 0.05, 0],
    [0, 0, 0.05],
    [0.5, 0, 0],
    [0, 0.05, 0],
    [0, 0, 0],
]

car = Car(10, 20, 0.0589/2)

car.start_arduino_talk()
switcher.start()
feedbacker.start()

plt.tight_layout()
plt.show()

switcher.join()
car.stop_arduino_talk()
feedbacker.join()
print(f"theta: {len(theta)}; x: {len(x)}; y: {len(y)}")
# print(f"theta: {theta}")
# print(f"x: {x}")
# print(f"y: {y}")