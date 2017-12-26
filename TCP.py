import threading
import time
import os


class TCP():
    # build TCP type
    SEND_DATA = 0
    SEND_SYN = 1
    SEND_SYNACK = 2
    SEND_ACK = 3
    SEND_FIN = 4


    def from_bytes(self, bytes):
        self.src_port = int.from_bytes(bytes[:2], byteorder='little')
        self.dst_port = int.from_bytes(bytes[2:4], byteorder='little')
        self.sequence_number = int.from_bytes(bytes[4:8], byteorder='little')
        self.acknowledgement_number = int.from_bytes(bytes[8:12], byteorder='little')
        self.header_length = int.from_bytes(bytes[12], byteorder='little')
        self.unused_and_flag_bits = int.from_bytes(bytes[13:16], byteorder='little')
        self.receive_window = int.from_bytes(bytes[16:20], byteorder='little')
        self.checksum = int.from_bytes(bytes[20:22], byteorder='little')
        self.urgent_pointer = int.from_bytes(bytes[22:24], byteorder='little')
        self.options = int.from_bytes(bytes[24:28], byteorder='little')
        self.data = bytes[28:]

    def build(self,
              type: int,
              src_port: int,
              dst_port: int,
              sequence_number: int = 0,
              acknowledgement_number: int = 0,
              header_length: int = 0,
              CEW: int = 0, # DK
              ECE: int = 0, # DK
              URG: int = 0, # urgent
              ACK: int = 0,
              PSH: int = 0, # should pass immediately
              RST: int = 0, # reset
              SYN: int = 0,
              FIN: int = 0,
              receive_window: int = 0,
              urgent_data_pointer: int = 0,
              options: int = 0,
              data: bytes = b''):
        self.src_port = src_port
        self.dst_port = dst_port
        self.sequence_number = sequence_number
        self.acknowledgement_number = acknowledgement_number
        self.header_length = header_length
        self.reserved_and_control_bits = 0
        self.receive_window = receive_window
        self.checksum = 0
        self.urgent_pointer = urgent_data_pointer
        self.options = options
        self.data = data

        if type == self.SEND_SYN:
            self._create_flag_field(SYN = 1)
            return bytes(self)
        elif type == self.SEND_SYNACK:
            self._create_flag_field(SYN = 1, ACK = 1)
            return bytes(self)
        elif type == self.SEND_ACK:
            self._create_flag_field(ACK = 1)
            return bytes(self)
        elif type == self.SEND_FIN:
            self._create_flag_field(FIN = 1)
            return bytes(self)




    def _create_flag_field(self, URG: int = 0, ACK: int = 0, PSH: int = 0, RST: int = 0, SYN: int = 0, FIN: int = 0, CWR = 0, ECE = 0):
        s = "00000000{CWR}{ECE}{URG}{ACK}{PSH}{RST}{SYN}{FIN}".format(CWR = CWR, ECE = ECE, URG = URG, ACK = ACK, PSH = PSH, RST = RST, SYN = SYN, FIN = FIN)
        self.unused_and_flag_bits = int(s, 2)


    def __bytes__(self):
        return_byte = int.to_bytes(self.src_port, 2, 'little') + \
                      int.to_bytes(self.dst_port, 2, 'little') + \
                      int.to_bytes(self.sequence_number, 4, 'little') + \
                      int.to_bytes(self.acknowledgement_number, 4, 'little') + \
                      int.to_bytes(self.header_length) + \
                      int.to_bytes(self.reserved_and_control_bits) + \
                      int.to_bytes(self.receive_window) + \
                      int.to_bytes(self.checksum) + \
                      int.to_bytes(self.urgent_pointer) + \
                      int.to_bytes(self.options) + \
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
