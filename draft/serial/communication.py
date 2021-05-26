import serial
import struct
import crc8

# float array serial transceiver
class SerialTransceiver:

    def __init__(self, port_name, baud_rate) -> None:
        self._msg_to_send = [0, 0, 0]
        self._msg_to_receive = [0, 0, 0]

        self.theta = [0]
        self.x = [0]
        self.y = [0]

        self._port = serial.Serial(port_name, baud_rate, timeout=1, write_timeout=5)
        self._port.flush()
        self._transactions_count = 0
        self._wrong_len_msgs = 0
        self.is_stop = False
        self._repeats = 0
        self._corrupted = 0

    def set_msg(self, msg):
        assert (len(msg) == 3)
        self._msg_to_send = msg

    def get_msg(self):
        return self._msg_to_receive

    def get_transactions_count(self):
        return self._transactions_count
    
    def get_corrupted_count(self):
        return self._wrong_len_msgs
        
    def get_repeats_count(self):
        return self._repeats

    def get_corrupted_count(self):
        return self._corrupted

    def tx(self):
        byte_array = struct.pack('3f', self._msg_to_send[0], self._msg_to_send[1], self._msg_to_send[2])
        hash = crc8.crc8()
        hash.update(byte_array)
        checksum = hash.digest()
        self._port.write(byte_array)
        self._port.write(checksum)
        self._port.write(b'\n')

    def rx(self):
        response = self._port.readline()
        if len(response) == 14:
            hash = crc8.crc8()
            hash.update(response[0:12])
            checksum = hash.digest()
            if checksum == bytes([response[12]]):
                float_array = struct.unpack('3f', response[0:12])
                self.msg_to_receive = float_array
                if self.theta[-1] == float_array[0] and self.x[-1] == float_array[1] and self.y[-1] == float_array[2]:
                    self._repeats += 1
                else:
                    self.theta.append(float_array[0])
                    self.x.append(float_array[1])
                    self.y.append(float_array[2])
            else:
                self._corrupted += 1
        else:
            self._wrong_len_msgs += 1
    
    def talk_arduino(self):
        while not self.is_stop:
            try:
                self.tx()
            except serial.serialutil.SerialTimeoutException:
                self._port.cancel_write()
                print("Cancelled write on timeout")
                self.is_stop = True

            try:
                self.rx()
            except serial.serialutil.SerialTimeoutException:
                self._port.cancel_read()
                print("Cancelled read on timeout")
                self.is_stop = True
            
            self._transactions_count += 1
        
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()
        self._port.close()

    def stop(self):
        print(f"Transactions = {self._transactions_count}\n accepted={len(self.x)}\n repeats: {self._repeats}\n wrong length: {self._wrong_len_msgs}\n corrupted: {self._corrupted}\n")
        self.is_stop = True
        self._transactions_count = 0
        self._repeats = 0
        self._wrong_len_msgs = 0
        self._corrupted = 0
