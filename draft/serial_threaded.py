#!/usr/bin/env python3
import serial
import time
import threading

if __name__ == '__main__':
    port = serial.Serial('/dev/ttyACM0', 115200)
    port.flush()

    start = time.time()


    def process_message(msg):
        print(msg)
        # print(f"Time passed: {time.time() - start} secs; msg len = {len(msg)}")


    def transmit():
        while True:
            # global start
            # start = time.time()
            port.write(b"Hello from Raspberry Pi!\n")
            time.sleep(1)


    def receive():
        while True:
            line = port.readline().decode('utf-8').rstrip()
            process_message(line)


    tx_thread = threading.Thread(target=transmit)
    # rx_thread = threading.Thread(target=receive)
    tx_thread.start()
    # rx_thread.start()

    # transmit()
    receive()

    tx_thread.join()
    # rx_thread.join()
