from omnimath import *
import serial
import struct


class Car:
    def __init__(self):
        self.velocity = np.zeros((4, 1))
        self.port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.port.flush()

    def set_wheels_velocities(self, u):
        pass

    def set_car_velocity(self, dq):
        pass

    # ------------- Arduino ----------------
    def tx_velocity(self):
        byte_array = struct.pack('4f', self.velocity[0], self.velocity[1], self.velocity[2], self.velocity[3])
        self.port.write(byte_array)

    def rx_velocity(self):
        response = self.port.readline()
        floats = struct.unpack('4f', response[0:16])
        self.velocity[0] = floats[0]
        self.velocity[1] = floats[1]
        self.velocity[2] = floats[2]
        self.velocity[3] = floats[3]

    def talk_arduino(self):
        pass
