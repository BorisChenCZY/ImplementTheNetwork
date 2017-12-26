AF_INET = 2
SOCK_STREAM = 1
RECEIVED_BUFFER_SIZE = 1048576 # todo discuss the buffer size, currently 1GMb

from Exceptions import *
import threading
import os
import time


class socket():
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

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0):
        self.__family = family
        self.__type = type
        self.__address = None
        self.__data = None
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

        pass

    def accept(self):
        """accept() -> (socket object, address info)

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
            if self.__status != self.LISTEN:
                raise StatusException("The socket is not listening.")
            if self.data == None:
                continue
            # todo here

    def recv(self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recv(buffersize[, flags]) -> data

        Receive up to buffersize bytes from the socket.  For the optional flags
        argument, see the Unix manual.  When no data is available, block until
        at least one byte is available or until the remote end is closed.  When
        the remote end is closed and all data is read, return the empty string.
        """
        if self.__status == self.CLOSED:
            raise ClosedException("The socket is closed, did you start listen process?")

        while self.data == None:
            pass
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
        self.data = frame.payload
        # todo
        pass