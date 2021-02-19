import serial
import struct
from threading import Thread

# float array serial transceiver
class SerialTransceiver:

    def __init__(self) -> None:
        self.max_velocity = 10
        self.msg_to_send = [0, 0.5, 0]
        self.msg_to_receive = [0, 0, 0]
        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._arduino_thread = Thread(target=self.talk_arduino)
        self._is_stop = False
        self._msg_count = 0
        self._corrupt_count = 0

    def tx(self):
        byte_array = struct.pack('3f', self.msg_to_send[0], self.msg_to_send[1], self.msg_to_send[2])
        self._port.write(byte_array)
        self._port.write(b'\n')

    def rx(self):
        response = self._port.readline()
        if len(response) == 13:
            float_array = struct.unpack('3f', response[0:12])
            if max(float_array) <= self.max_velocity and min(float_array) >= -self.max_velocity:
                self.msg_to_receive = float_array
        else:
            self._corrupt_count += 1
    
    def talk_arduino(self):
        while not self._is_stop:
            self.tx()
            self.rx()
            self._msg_count += 1
        self._port.close()

    def start_arduino_talk(self):
        if not self._arduino_thread.is_alive():
            self._arduino_thread.start()
            print("Arduino thread started")
        else:
            print("Arduino thread already running")

    def stop_arduino_talk(self):
        self._is_stop = True
        self._arduino_thread.join()
        print(f"Arduino communication stopped after {self._msg_count} messages ({self._corrupt_count} corrupted)")
        self._msg_count = 0
        self._corrupt_count = 0

    def is_stop(self):
        return self._is_stop