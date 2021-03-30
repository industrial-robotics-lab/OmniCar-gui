#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

x = []
y = []

def animate(i):
    x.append(random.randint(0, 50))
    y.append(random.randint(0, 50))

    plt.cla() # clear axis (keep line the same color on each iteration)
    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval=1000) # get current figure

plt.tight_layout()
plt.show()