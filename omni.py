from omnimath import vec6_to_SE3, np
import serial
import struct
import threading


class Car:
    max_velocity = 10

    def __init__(self):
        self._desired_velocity = np.zeros([3, 1])
        self._feedback_pose = np.zeros([3, 1])

        self.x = [0]
        self.y = [0]

        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._arduino_thread = threading.Thread(target=self.talk_arduino)
        self._stop_event = threading.Event()
        self._msg_count = 0
        self._corrupt_count = 0
        self.repeats = 0

    def set_car_velocity(self, desired):
        assert len(desired) == 3
        self._desired_velocity[0] = desired[0]
        self._desired_velocity[1] = desired[1]
        self._desired_velocity[2] = desired[2]

    def print_velocity(self):
        print(f"Velocity: {self._feedback_pose.ravel()}")

    def get_velocity(self):
        return self._feedback_pose

    # ------------- Arduino ----------------
    def tx_velocity(self):
        byte_array = struct.pack(
            '3f', self._desired_velocity[0], self._desired_velocity[1], self._desired_velocity[2])
        self._port.write(byte_array)
        self._port.write(b'\n')

    def rx_velocity(self):
        response = self._port.readline()
        if len(response) == 13:
            feedback = struct.unpack('3f', response[0:12])
            self._feedback_pose[0] = feedback[0]
            self._feedback_pose[1] = feedback[1]
            self._feedback_pose[2] = feedback[2]
            # print(f"feedback: {feedback}")
            if self.x[-1] == feedback[1] and self.y[-1] == feedback[2]:
                self.repeats += 1
            else:
                self.x.append(feedback[1])
                self.y.append(feedback[2])

    def talk_arduino(self):
        while not self._stop_event.is_set():
            self.tx_velocity()
            self.rx_velocity()
            self._msg_count += 1
        self._port.close()
        print("port closed")

    def start_arduino_talk(self):
        if not self._arduino_thread.is_alive():
            self._arduino_thread.start()
        else:
            print("Arduino thread is already running")

    def stop_arduino_talk(self):
        self._stop_event.set()
        print("_stop_event.set()")
        self._arduino_thread.join()
        print(
            f"Arduino communication stopped after {self._msg_count} messages ({self._corrupt_count} corrupted)")
        self._msg_count = 0
        self._corrupt_count = 0
        self._stop_event.clear()
