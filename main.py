#!/usr/bin/env python3
from communication import SerialTransceiver
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread

theta = []
x = []
y = []

transceiver = SerialTransceiver()

def talk():
    for i in range(1000):
        transceiver.tx([0, 0.5, 0])
        response = transceiver.rx()
        if (response != -1):
            theta.append(response[0])
            x.append(response[1])
            y.append(response[2])



def animate(i):
    plt.cla()  # clear axis (keep line the same color on each iteration)
    plt.plot(x, y)


ani = FuncAnimation(plt.gcf(), animate, interval=1000)  # get current figure

t1 = Thread(target=talk)

t1.start()

plt.tight_layout()
plt.show()

t1.join()