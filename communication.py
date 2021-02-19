import serial
import struct

# float array serial transceiver
class SerialTransceiver:
    max_velocity = 10

    def __init__(self) -> None:
        self._port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self._port.flush()
        self._is_stop = False
        self._msg_count = 0
        self._corrupt_count = 0

    def tx(self, msg):
        byte_array = struct.pack('3f', msg[0], msg[1], msg[2])
        self._port.write(byte_array)
        self._port.write(b'\n')

    def rx(self):
        response = self._port.readline()
        if len(response) == 13:
            float_array = struct.unpack('3f', response[0:12])
            if max(float_array) <= self.max_velocity and min(float_array) >= -self.max_velocity:
                return float_array
        else:
            self._corrupt_count += 1
            return -1