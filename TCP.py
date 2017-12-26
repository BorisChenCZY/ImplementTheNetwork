import threading
import time
import os


class TCP():
    def __init__(self, window_size:int = 10):
        self.window_size: int = window_size
        self.TIME_INTERVAL: int = 10
        self.time_out:bool = False

    def from_bytes(self, bytes):
        self.src_port = int.from_bytes(bytes[:2], byteorder='little')
        self.dst_port = int.from_bytes(bytes[2:4], byteorder='little')
        self.sequence_number = int.from_bytes(bytes[4:8], byteorder='little')
        self.acknowledgement_number = int.from_bytes(bytes[8:12], byteorder='little')
        self.data_offset = int.from_bytes(bytes[12], byteorder='little')
        self.reserved_and_control_bits = int.from_bytes(bytes[13:16], byteorder='little')
        self.window = int.from_bytes(bytes[16:20], byteorder='little')
        self.check_sum = int.from_bytes(bytes[20:22], byteorder='little')
        self.urgent_pointer = int.from_bytes(bytes[22:24], byteorder='little')
        self.option_and_padding = int.from_bytes(bytes[24:28], byteorder='little')
        self.data = int.from_bytes(bytes[28:], byteorder='little')

    def build(self, src_port, dst_port, sequence_number, acknowledgement_number, data_offset, reserved_and_control_bits, ):
        pass


    def __bytes__(self):
        return_byte = int.to_bytes(self.src_port) + \
                      int.to_bytes(self.src_port) + \
                      int.to_bytes(self.dst_port) + \
                      int.to_bytes(self.sequence_number) + \
                      int.to_bytes(self.acknowledgement_number) + \
                      int.to_bytes(self.data_offset) + \
                      int.to_bytes(self.reserved_and_control_bits) + \
                      int.to_bytes(self.window) + \
                      int.to_bytes(self.check_sum) + \
                      int.to_bytes(self.urgent_pointer) + \
                      int.to_bytes(self.option_and_padding) + \
                      int.to_bytes(self.data)
        return return_byte

    def calculate_checksum(self):
        checksum: int = 0
        # every two byte compute a checksum
        for i in range(len(self.data) // 2):
            byte = self.data[2 * i: 2 * i + 2]
            checksum += int.from_bytes(byte)
            if checksum > 65535:
                checksum = checksum % 65535 + checksum // 65535

        # if the length is odd, compute another time
        if len(self.data) % 2 != 0:
            checksum += int.from_bytes(self.data[-1])
            if checksum > 65535:
                checksum = checksum % 65535 + checksum // 65535
        return checksum





    def __del__(self):
        pass

    def send(self):
        NextSeqNum: int = 0
        while 1:
            pass
