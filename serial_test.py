#!/usr/bin/env python3
import serial
import time
import numpy as np
import struct

port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
port.flush()


def tx_rx_floats():
    # TX
    byte_array = struct.pack('4f', 123.123, 342.322, 783.39, 8478.49)
    port.write(byte_array)
    # RX
    response = port.readline()
    if len(response) == 17:
        floats = struct.unpack('4f', response[0:16])
        print(f"Received: {floats} size = {len(response)}")
    else:
        print(f"corrupted msg of size {len(response)}")


for _ in range(15):
    tx_rx_floats()

port.close()
