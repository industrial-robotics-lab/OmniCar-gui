#!/usr/bin/env python3
from time import sleep
import keyboard
from threading import Thread

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
def evaluate():
    global need_stop
    while not need_stop:
        lin_speed = 0.03
        ang_speed = 0.01
        vel = [0,0,0]
        if is_forward:
            vel[0] += lin_speed
        if is_left:
            vel[1] += lin_speed
        if is_backward:
            vel[0] -= lin_speed
        if is_right:
            vel[1] -= lin_speed
        if is_rotate_left:
            vel[2] += ang_speed
        if is_rotate_right:
            vel[2] -= ang_speed
        print(f"Velocity: {vel}")
        sleep(0.5)

t1 = Thread(target=evaluate)
t1.start()
keyboard.hook(parse_keys)
keyboard.wait('esc')
need_stop = True
t1.join()
