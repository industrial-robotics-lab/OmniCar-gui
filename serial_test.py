#!/usr/bin/env python3
import serial
import struct
import time

port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
port.flush()
times = []
corrupted = 0


def tx_rx_floats(values):
    global corrupted
    start = time.time()
    # TX
    assert len(values) == 4
    byte_array = struct.pack('4f', values[0], values[1], values[2], values[3])
    port.write(byte_array)
    port.write(b'\n')
    # RX
    response = port.readline()
    end = time.time() - start
    times.append(end)
    if len(response) == 17:
        floats = struct.unpack('4f', response[0:16])
        print(f"Received: {floats} size = {len(response)}, time = {end}")
    else:
        print(f"corrupted msg of size {len(response)}")
        corrupted += 1


for _ in range(2):
    start = time.time()
    while time.time() - start < 3:
        tx_rx_floats([70, -70, 70, -70])

    start = time.time()
    while time.time() - start < 3:
        tx_rx_floats([0, 0, 0, 0])

print(f"FPS: {1 / (sum(times)/len(times))} ({len(times)} msgs, {corrupted} corrupted)")
port.close()
