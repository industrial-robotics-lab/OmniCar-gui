#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from omni import *
import time

def switch_vels():
    for vel in car_vels:
        car.set_car_velocity(vel)
        print(f"Change vel to {vel}")
        time.sleep(2)
    # plt.close()


def animate(i):
    plt.cla() # clear axis (keep line the same color on each iteration)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(car.x, car.y)

ani = FuncAnimation(plt.gcf(), animate, interval=500) # get current figure

switcher = Thread(target=switch_vels)

car_vels = [
    [0, 0, 0],
    [0, 0.05, 0],
    [0, 0, 0]
]

car = Car()

car.start_arduino_talk()
switcher.start()

plt.tight_layout()
plt.show()

switcher.join()
car.stop_arduino_talk()
print(f"x: {len(car.x)}; y: {len(car.y)}")