#!/usr/bin/env python3
import serial
import time
import numpy as np
import struct

port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
port.flush()


def talk_float():
    msg = b'123.456'
    print(f"Msg: {msg}")
    port.write(msg)
    response = port.readline().decode('ascii')
    print(f"Response: {response}")


def talk_float_as_bytes():
    msg = bytearray(b"123.456")
    print(f"Msg: {msg} as {[i for i in msg]}")
    port.write(msg)
    response = port.readline().decode('ascii')
    print(f"Response: {response}")


def talk_double_array():
    # u = bytearray(np.array([1.1, 2.2, 3.3, 4.4]))
    byte_array = struct.pack('dddd', 1.1, 2.2, 3.3, 4.4)
    print(f"Send: dddd (type = {type(byte_array)}; size = {len(byte_array)})")
    port.write(byte_array)
    # port.write(b'\n')
    response = port.readline()
    double_array = None
    if len(response) == 32:
        double_array = struct.unpack('dddd', response)
    print(f"Response: {double_array} type = {type(response)} size = {len(response)}")


def string_transaction():
    port.write(b"1.1 2.2 3.3 4.4\n")
    line = port.readline().decode('utf-8').rstrip()
    rpms = [float(rpm) for rpm in line.split(' ')]
    print(f"sum = {sum(rpms)}| dt = {time.time() - start} secs")


def receive_float_array():
    response = port.readline()
    if len(response) == 17:  # 17 = 4 floats + '\n'
        floats = struct.unpack('4f', response[0:16])
        print(f"Received: {sum(floats)} size = {len(response)}")
    else:
        print("xxxxx")


def tx_rx_floats():
    byte_array = struct.pack('4f', 1.1, 2.2, 3.3, 4.4)
    port.write(byte_array)
    response = port.readline()
    if len(response) == 17:
        floats = struct.unpack('4f', response[0:16])
        print(f"Received: {floats} size = {len(response)}")
    else:
        print(f"corrupted msg of size {len(response)}")


for _ in range(15):
    # talk_float()
    # talk_float_as_bytes()
    # talk_double_array()
    # receive_float_array()
    tx_rx_floats()

port.close()
