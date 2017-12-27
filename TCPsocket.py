AF_INET = 2
SOCK_STREAM = 1
RECEIVED_BUFFER_SIZE = 1048576  # todo discuss the buffer size, currently 1GMb

from Exceptions import *
from TCP import *
import threading
import os
import time
import Network


class socket():
    # status
    CLOSED = 0
    LISTEN = 1
    SYN_RCVD = 2
    ESTABLISHED = 3
    CLOSE_WAIT = 4
    LAST_ACK = 5
    SYN_SENT = 6
    FIN_WAIT_1 = 7
    FIN_WAIT_2 = 8
    TIME_WAIT = 9

    # const
    TIME_INTERVAL = 100

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0):
        self.__family = family
        self.__type = type
        self.__address = None
        self.__data = b''
        self.__status = self.CLOSED


    def bind(self, address):
        """
                bind(address)

                Bind the socket to a local address.  For IP sockets, the address is a
                pair (host, port); the host must refer to the local host. For raw packet
                sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])
                """
        self.__address = address

    def listen(self, backlog=None):
        """
                        listen([backlog])

                        Enable a server to accept connections.  If backlog is specified, it must be
                        at least 0 (if it is lower, it is set to 0); it specifies the number of
                        unaccepted connections that the system will allow before refusing new
                        connections. If not specified, a default reasonable value is chosen.
                        """
        if not self.__address:
            raise AddressNotSpecified("Did you bind address for this socket?")

        self.__network = Network.Network(self.__address)

    def accept(self):
        """accept() -> address tuple

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        # fd, addr = self._accept()
        # If our type has the SOCK_NONBLOCK flag, we shouldn't pass it onto the
        # new socket. We do not currently allow passing SOCK_NONBLOCK to
        # accept4, so the returned socket is always blocking.
        # type = self.type & ~globals().get("SOCK_NONBLOCK", 0)
        # sock = socket(self.family, type, self.proto, fileno=fd)
        # Issue #7995: if no default timeout is set and the listening
        # socket had a (non-zero) timeout, force the new socket in blocking
        # mode to override platform-specific socket flags inheritance.
        # if getdefaulttimeout() is None and self.gettimeout():
        #     sock.setblocking(True)
        # return sock, addr

        # if not self.__address:
        #     raise AddressNotSpecified("Did you bind address for this socket?")
        if self.__status == self.CLOSED:
            raise ClosedException("The socket is closed, did you start listen process?")

        self.__status = self.LISTEN

        while 1:
            if self.__status != self.LISTEN or self.__status != self.SYN_RCVD:
                raise StatusException("The socket is not listening.")
            if self.__status == self.LISTEN:
                data, address = self.__network.retrive()
            else:
                data = tmp_network.retrive()
            if data == b'':
                continue
            else:
                tcp = TCP()
                tcp.from_bytes(data)
                if self.__status == self.LISTEN:
                    if tcp.SYN == 1:
                        tmp_network = Network.Network(self.__address, address)
                        tcp = TCP()
                        tcp.build(type=TCP.SEND_SYNACK, src_port=self.__address[1], dst_port=address[1])
                        tmp_network.send(bytes(tcp))
                        self.__status = self.SYN_RCVD
                elif self.__status == self.SYN_RCVD:
                    if tcp.ACK == 1:
                        self.__status = self.ESTABLISHED
                        return address

    def connect(self, address):  # real signature unknown; restored from __doc__
        """
        connect(address)

        Connect the socket to a remote address.  For IP sockets, the address
        is a pair (host, port).
        """
        self.__network = Network.Network(self.__address, address)

        tcp = TCP()
        tcp.build(type=TCP.SEND_SYN, src_port=self.__address[1], dst_port=address[1])
        self.__network.send(bytes(tcp))
        self.__status = self.SYN_SENT

        while 1:
            data = self.__network.retrive()
            if data == b'':
                continue
            tcp = TCP()
            tcp.from_bytes(data)
            if tcp.SYN == 1 and tcp.ACK == 1:
                tcp.build(type=tcp.ACK, src_port=self.__address[1], dst_port=address[1])
                self.__network.send(bytes(tcp))
                break

    def recv(self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recv(buffersize[, flags]) -> data

        Receive up to buffersize bytes from the socket.  For the optional flags
        argument, see the Unix manual.  When no data is available, block until
        at least one byte is available or until the remote end is closed.  When
        the remote end is closed and all data is read, return the empty string.
        """
        if self.__status != self.ESTABLISHED:
            raise ClosedException("Connection has not been established?")

        while self.data == b'':
            self.data = self.__network.retrive()
            continue

        # if self.data != None:
        if buffersize > len(self.data):
            buffersize = len(self.data)
        return_data = self.data[:buffersize]
        self.data = self.data[buffersize:]

        return return_data

    def send(self, data, flags=None):  # real signature unknown; restored from __doc__
        """
                send(data[, flags]) -> count

                Send a data string to the socket.  For the optional flags
                argument, see the Unix manual.  Return the number of bytes
                sent; this may be less than len(data) if the network is busy.
                """

        if self.__type != SOCK_STREAM:
            raise TypeNotRightException("type is not correct, is the socket assigned TCP protocol?")

        NextSeqNum: int = 0
        while 1:
            pass

    def close(self):  # real signature unknown; restored from __doc__
        """
        close()

        Close the socket.  It cannot be used after this call.
        """
        pass

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.check_time, args=(time.time(), self.TIME_INTERVAL))

    def check_time(self, start_time, time_interval):
        self.current_pid = os.getpid()
        pid = os.get_pid()
        while 1:
            time.sleep(time_interval * 0.1)
            if self.current_pid != pid:
                return
            current_time: int = time.time()
            if current_time - start_time > time_interval:
                self.time_out = True
                self.timer_thread = None
                return

    def _start_server(self):
        from LinkLayer import LinkLayer, util
        linkLayer = LinkLayer(self._receive_from_Network)

    def _receive_from_Network(self, frame):
        src_mac = frame.src_mac
        dst_mac = frame.dst_mac
        ip = '127.0.0.1'
        self.data.append((frame.payload, ip))
        # todo
        pass

    def _unpack_from_network_layer(self, data):
        pass
