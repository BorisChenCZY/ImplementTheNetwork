class socket(object):
    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None):
        self.family = family
        self.type = type
        self.proto = proto
        self.fileno = fileno
        pass

    def bind(self, address):  # real signature unknown; restored from __doc__
        """
        bind(address)

        Bind the socket to a local address.  For IP sockets, the address is a
        pair (host, port); the host must refer to the local host. For raw packet
        sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])
        """
        self.ip = address[0]
        self.port = address[1]
        address = (self.ip, self.port)
        if self.type == SOCK_STREAM:
            self.tcp = TCP(address)
        elif self.type == SOCK_DGRAM:
            self.udp = UDP(address)
        pass

    def listen (self, backlog=None):  # real signature unknown; restored from __doc__
        """
        listen([backlog])

        Enable a server to accept connections.  If backlog is specified, it must be
        at least 0 (if it is lower, it is set to 0); it specifies the number of
        unaccepted connections that the system will allow before refusing new
        connections. If not specified, a default reasonable value is chosen.
        """
        if backlog is None:
            self.blacklog = 1
        elif backlog < 0:
            self.blacklog = 0
        else:
            self.blacklog = backlog
        pass
    
    def accept(self):
        """accept() -> (socket object, address info)

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        fd, addr = self._accept()
        # If our type has the SOCK_NONBLOCK flag, we shouldn't pass it onto the
        # new socket. We do not currently allow passing SOCK_NONBLOCK to
        # accept4, so the returned socket is always blocking.
        sock = socket(self.family, self.type, self.proto, fileno=fd)
        # Issue #7995: if no default timeout is set and the listening
        # socket had a (non-zero) timeout, force the new socket in blocking
        # mode to override platform-specific socket flags inheritance.
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

    def send (self, data, flags=None):  # real signature unknown; restored from __doc__
        """
        send(data[, flags]) -> count

        Send a data string to the socket.  For the optional flags
        argument, see the Unix manual.  Return the number of bytes
        sent; this may be less than len(data) if the network is busy.
        """
        pass

    def sendto (self, data, flags=None, *args,
                **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
        """
        sendto(data[, flags], address) -> count

        Like send(data, flags) but allows specifying the destination address.
        For IP sockets, the address is a pair (hostaddr, port).
        """
        pass
    
    def recv (self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recv(buffersize[, flags]) -> data

        Receive up to buffersize bytes from the socket.  For the optional flags
        argument, see the Unix manual.  When no data is available, block until
        at least one byte is available or until the remote end is closed.  When
        the remote end is closed and all data is read, return the empty string.
        """
        pass

    def recvfrom (self, buffersize, flags=None):  # real signature unknown; restored from __doc__
        """
        recvfrom(buffersize[, flags]) -> (data, address info)

        Like recv(buffersize, flags) but also return the sender's address info.
        """
        pass