#!/usr/bin/env python3
import serial
import struct
import time

port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
port.flush()
times = []
corrupted = 0


def tx_rx_floats():
    global corrupted
    start = time.time()
    # TX
    byte_array = struct.pack('4f', 1.1, 2.2, 3.3, 4.4)
    port.write(byte_array)
    # RX
    response = port.readline()
    end = time.time() - start
    times.append(end)
    if len(response) == 17:
        floats = struct.unpack('4f', response[0:16])
        if int(sum(floats)) != 11:
            corrupted += 1
        print(f"Received: {int(sum(floats))} size = {len(response)}, time = {end}")
    else:
        print(f"corrupted msg of size {len(response)}")
        corrupted += 1


for _ in range(100):
    tx_rx_floats()

print(f"FPS: {1 / (sum(times)/len(times))} ({len(times)} msgs, {corrupted} corrupted)")
port.close()
