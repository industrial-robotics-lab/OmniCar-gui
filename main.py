#!/usr/bin/env python3
from communication import SerialTransceiver
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
# from multiprocessing import Process
import time

car_vels = [
    [0, 0, 0],
    [0, 0.05, 0],
    [0, 0, 0.05],
    [0, -0.05, 0],
    [0, 0, -0.05],
    [0, 0, 0]
]

def switch_vels():
    for vel in car_vels:
        transceiver.set_msg(vel)
        # print(f"Change vel to {vel}")
        time.sleep(2)
    # plt.close()

start = time.perf_counter()
def animate(i):
    plt.cla() # clear axis (keep line the same color on each iteration)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(transceiver.x, transceiver.y)


    global start
    finish = time.perf_counter()
    print(f"Plot interval = {finish - start}")
    start = finish

ani = FuncAnimation(plt.gcf(), animate, interval=500) # get current figure

transceiver = SerialTransceiver()

switcher = Thread(target=switch_vels)
talker = Thread(target=transceiver.talk_arduino)

talker.start()
switcher.start()

plt.tight_layout()
plt.show()

switcher.join()
transceiver.stop()
talker.join()