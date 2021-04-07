#!/usr/bin/env python3
import serial
import struct
from threading import Thread
import sys
import time
import keyboard
import crc8
from random import random

msg = [0, 0, 0]
count = 0
corrupted = 0
wrong_len = 0
# baudrate - msg/sec - isOk
# 9600       63        True
# 14400      98        True
# 19200      129       True
# 28800      189       True
# 38400      242       True
# 57600      318       False (fail on 6586)
# 115200     451       False (fail on 6871)
serialPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1, write_timeout=5)
trigger = False
isConnected = False


def print_data():
    while not trigger:
        sys.stdout.write(
            f"\rcount={count}, corrupted={corrupted}, wrong_len={wrong_len}")
        sys.stdout.flush()
        time.sleep(0.1)

def talk():
    global msg, count, wrong_len, response, corrupted
    printer_thread.start()
    start = time.perf_counter()
    while not trigger:
        # tx
        byte_array = struct.pack('3f', random(), random(), random())
        hash = crc8.crc8() # MUST make new one on each iteration
        hash.update(byte_array)
        checksum = hash.digest()
        serialPort.write(byte_array)
        serialPort.write(checksum)
        serialPort.write(b'\n')
        serialPort.reset_output_buffer()

        # rx
        response = serialPort.readline()
        count += 1
        if len(response) == 14:
            hash = crc8.crc8() # MUST make new one on each iteration
            hash.update(response[0:12])
            checksum = hash.digest()
            # print(f"msg: {msg}; crc8: p={checksum} | a={bytes([response[12]])}")
            if checksum == bytes([response[12]]):
                msg = struct.unpack('3f', response[0:12])
            else:
                corrupted += 1
        else:
            wrong_len += 1

    end = time.perf_counter()
    print(f"\nAverage msg/sec = {count/(end-start)}")


arduino_talker_thread = Thread(target=talk)
printer_thread = Thread(target=print_data)

arduino_talker_thread.start()

keyboard.wait('esc')
trigger = True

arduino_talker_thread.join()
printer_thread.join()
