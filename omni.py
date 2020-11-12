from omnimath import *
import serial
import struct
from threading import Thread


class Car:
    def __init__(self):
        self._velocity = [0.0, 0.0, 0.0, 0.0]

        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._arduino_thread = Thread(target=self.talk_arduino)
        self._is_stop = False
        self._msg_count = 0
        self._corrupt_count = 0

    def set_wheels_velocities(self, u):
        pass

    def set_car_velocity(self, dq):
        pass

    # ------------- Arduino ----------------
    def tx_velocity(self):
        byte_array = struct.pack('4f', self._velocity[0], self._velocity[1], self._velocity[2], self._velocity[3])
        self._port.write(byte_array)

    def rx_velocity(self):
        response = self._port.readline()
        if len(response) == 17:
            floats = struct.unpack('4f', response[0:16])
            self._velocity[0] = floats[0]
            self._velocity[1] = floats[1]
            self._velocity[2] = floats[2]
            self._velocity[3] = floats[3]
            # print(f"Received {self._velocity}")
        else:
            self._corrupt_count += 1
            # print(f"corrupted msg of size {len(response)}")

    def talk_arduino(self):
        while not self._is_stop:
            self.tx_velocity()
            self.rx_velocity()
            self._msg_count += 1
        self._port.close()

    def start_arduino_talk(self):
        if not self._arduino_thread.is_alive():
            # self._arduino_thread = Thread(target=self.talk_arduino)
            self._arduino_thread.start()
        else:
            print("Arduino thread is already running")

    def stop_arduino_talk(self):
        self._is_stop = True
        self._arduino_thread.join()
        print(f"Arduino communication stopped after {self._msg_count} messages ({self._corrupt_count} corrupted)")
        self._msg_count = 0
        self._corrupt_count = 0

    def print_velocity(self):
        print(f"Velocity: {self._velocity}")
