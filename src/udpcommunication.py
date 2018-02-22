import socket

import struct


class UdpServerCommunication:
    multicast_group = '224.3.2.5'
    server_port = 3334
    server_address = ('', server_port)
    sock = None

    # Connect to address
    def __init__(self):
        print("Multicast group " + self.multicast_group + ", port: " + str(self.server_port))
        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        self.sock.bind(self.server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def get_socket(self):
        return self.sock
