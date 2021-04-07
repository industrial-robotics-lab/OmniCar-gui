#!/usr/bin/env python3
from communication import SerialTransceiver
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
# from multiprocessing import Process
import time
import keyboard

is_forward = False
is_left = False
is_backward = False
is_right = False
is_rotate_left = False
is_rotate_right = False

def parse_keys(event):
    global is_forward
    global is_left
    global is_backward
    global is_right
    global is_rotate_left
    global is_rotate_right
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'w' and not is_forward:
            is_forward = True
        elif event.name == 'a' and not is_left:
            is_left = True
        elif event.name == 's' and not is_backward:
            is_backward = True
        elif event.name == 'd' and not is_right:
            is_right = True
        elif event.name == 'q' and not is_rotate_left:
            is_rotate_left = True
        elif event.name == 'e' and not is_rotate_right:
            is_rotate_right = True
    elif event.event_type == keyboard.KEY_UP:
        if event.name == 'w' and is_forward:
            is_forward = False
        elif event.name == 'a' and is_left:
            is_left = False
        elif event.name == 's' and is_backward:
            is_backward = False
        elif event.name == 'd' and is_right:
            is_right = False
        elif event.name == 'q' and is_rotate_left:
            is_rotate_left = False
        elif event.name == 'e' and is_rotate_right:
            is_rotate_right = False

need_stop = False
car_vel = [0,0,0]
def calculate_velocity():
    global need_stop
    global car_vel
    lin_speed = 0.03
    ang_speed = 0.1
    while not need_stop:
        car_vel = [0,0,0]
        if is_rotate_left:
            car_vel[0] += ang_speed
        if is_rotate_right:
            car_vel[0] -= ang_speed
        if is_forward:
            car_vel[1] += lin_speed
        if is_backward:
            car_vel[1] -= lin_speed
        if is_left:
            car_vel[2] += lin_speed
        if is_right:
            car_vel[2] -= lin_speed
        # print(f"Velocity: {car_vel}")
        transceiver.set_msg(car_vel)
        time.sleep(0.1)

start = time.perf_counter()
def animate(i):
    plt.cla() # clear axis (keep line the same color on each iteration)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(transceiver.x, transceiver.y)

    global start
    finish = time.perf_counter()
    # print(f"Plot interval = {finish - start}")
    start = finish

ani = FuncAnimation(plt.gcf(), animate, interval=500) # get current figure

transceiver = SerialTransceiver('/dev/ttyACM0', 115200)

change_velocity_thread = Thread(target=calculate_velocity)
change_velocity_thread.start()

arduino_talker_thread = Thread(target=transceiver.talk_arduino)
arduino_talker_thread.start()
keyboard.hook(parse_keys)
plt.tight_layout()
plt.show()
keyboard.wait('esc')
need_stop = True

transceiver.stop()
arduino_talker_thread.join()

change_velocity_thread.join()