from omnimath import *
import serial
import struct
from threading import Thread


class Car:
    rpm_limit = 400

    def __init__(self, w, l, r):
        self._desired_velocity = np.zeros([4, 1])
        self._feedback_velocity = np.zeros([4, 1])
        
        self.w = w
        self.l = l
        self.r = r
        self.H_0 = 1/r * np.array([[-l-w, 1, -1],
                                   [ l+w, 1,  1],
                                   [ l+w, 1, -1],
                                   [-l-w, 1,  1]])
        self.F = r/4 * np.array([[-1/(l+w), 1/(l+w), 1/(l+w), -1/(l+w)],
                                 [ 1,       1,       1,        1      ],
                                 [-1,       1,      -1,        1      ]])

        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._arduino_thread = Thread(target=self.talk_arduino)
        self._is_stop = False
        self._msg_count = 0
        self._corrupt_count = 0

    def set_wheels_velocities(self, desired):
        assert len(desired) == 4
        if max(abs(desired)) > self.rpm_limit:
            desired = normalize(desired) * self.rpm_limit
        self._desired_velocity[0] = desired[0]
        self._desired_velocity[1] = desired[1]
        self._desired_velocity[2] = desired[2]
        self._desired_velocity[3] = desired[3]

    def set_car_velocity(self, car_vel):
        assert len(car_vel) == 3
        wheels_vel = 1 / self.r * np.dot(self.H_0, car_vel)
        self.set_wheels_velocities(wheels_vel)

    def print_velocity(self):
        print(f"Velocity: {self._feedback_velocity.ravel()}")

    # ------------- Arduino ----------------
    def tx_velocity(self):
        byte_array = struct.pack('4f', self._desired_velocity[0], self._desired_velocity[1], self._desired_velocity[2], self._desired_velocity[3])
        self._port.write(byte_array)
        self._port.write(b'\n')

    def rx_velocity(self):
        response = self._port.readline()
        if len(response) == 17:
            feedback = struct.unpack('4f', response[0:16])
            if max(feedback) <= self.rpm_limit and min(feedback) >= -self.rpm_limit:
                self._feedback_velocity[0] = feedback[0]
                self._feedback_velocity[1] = feedback[1]
                self._feedback_velocity[2] = feedback[2]
                self._feedback_velocity[3] = feedback[3]
        else:
            self._corrupt_count += 1

    def talk_arduino(self):
        while not self._is_stop:
            self.tx_velocity()
            self.rx_velocity()
            self._msg_count += 1
        self._port.close()

    def start_arduino_talk(self):
        if not self._arduino_thread.is_alive():
            self._arduino_thread.start()
        else:
            print("Arduino thread is already running")

    def stop_arduino_talk(self):
        self._is_stop = True
        self._arduino_thread.join()
        print(f"Arduino communication stopped after {self._msg_count} messages ({self._corrupt_count} corrupted)")
        self._msg_count = 0
        self._corrupt_count = 0

    def is_stop(self):
        return self._is_stop
