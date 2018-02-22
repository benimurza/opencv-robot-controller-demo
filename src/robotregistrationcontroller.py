import asyncio

from robot import Robot


class RobotRegistrationController:
    @staticmethod
    def listen_for_registrations(udp_socket, robot_list, default_street, robot_list_lock):
        """
        Run this as a daemon. Listens to incoming registrations, appends robot with default values and robot id
        to the current robot list.
        :param udp_socket: Socket to listen to.
        :param robot_list: List of Robot() objects.
        :param default_street: Default street with which the robot will be instantiated.
        :param robot_list_lock: Used for thread locking, since robot_list is a shared resource.
        """
        while True:
            print("waiting to receive message")
            data, address = udp_socket.recvfrom(1024)

            print("Received " + str(len(data)) + " from " + str(address))

            print("Sending ack.")
            if data[0] == 234:
                robot_id = data[1]
                print("Register command received!")

                # Send register ack
                udp_socket.sendto(bytes([235]), address)
                registered_robot = Robot()
                registered_robot.leading_point = default_street.road_component_list[0].start_point
                registered_robot.robot_id = robot_id
                registered_robot.ip_address = address
                registered_robot.robot_name = "Robot" + str(robot_id)
                registered_robot.current_street = default_street
                # Atomically insert
                robot_list_lock.acquire()
                try:
                    robot_list.append(registered_robot)
                finally:
                    robot_list_lock.release()
