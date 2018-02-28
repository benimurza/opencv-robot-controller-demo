import logging
import struct
from enum import Enum

from udpcommunication import UdpServerCommunication

logger = logging.getLogger("UdpCommandController")

class RobotCommands(Enum):
    GO_FORWARD = 1
    ROBOT_STOP = 2
    GO_LEFT = 3
    GO_RIGHT = 4


# TODO: same counter is being used for all robots!
class UdpCommandController:
    # Not needed now
    # TODO: delete
    duty_cycle_forward_command = 100
    duty_cycle_direction_command = 25

    # dict to keep track of counter for each address (robot)
    robot_counter_dict = dict()
    sock = None
    udpcomm = UdpServerCommunication()

    def __init__(self):
        # Retrieve socket which will be used throughout the server lifetime
        self.sock = self.udpcomm.get_socket()

    def send_command_stop(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([160]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1

    def send_command_left(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([173]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1

    def send_command_left_one_wheel(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([175]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1

    def send_command_right(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([172]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1

    def send_command_right_one_wheel(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([174]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1

    def send_command_forward(self, address, duty_cycle, counter):
        self.sock.sendto(bytes([170]) + struct.pack('hb', counter, duty_cycle), address)
        return counter + 1
