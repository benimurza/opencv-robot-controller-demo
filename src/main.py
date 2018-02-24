import threading
# Contains all robots
import cv2
import time

from citybuilder import CityBuilder
from colordetection import ColorDetection
from maputils import PointPairing, MapPoint
from robotcollisioncontroller import RobotCollisionController
from robotregistrationcontroller import RobotRegistrationController
from udpcommandcontroller import UdpCommandController

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Main")

# List containing all in-game robots
robot_list = list()

# Global city builder
city_builder = CityBuilder()

# Moves robots and listens for registrations
command_controller = UdpCommandController()

# Checks for collisions among robots
robot_collision_controller = RobotCollisionController()

# The frame processing and robot registration run in different threads.
# During robot registration, robots are inserted in a list which is used by the frame processing controller.
robot_list_lock = threading.Lock()


def run_camera():
    logger.debug("Camera running.")
    global city_builder
    global robot_list_lock

    # Set up camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    warm_up_count = 0
    while warm_up_count < 2:
        _, frame = cap.read()
        time.sleep(1)
        warm_up_count += 1

    # Start capturing frames
    while True:
        _, frame = cap.read()

        lead_points, trail_points = ColorDetection.get_blue_and_green_points_from_frame(frame)

        if len(lead_points) == len(trail_points):
            paired_points = PointPairing.pair_point_lists(lead_points, trail_points, 20)
            # Points have been paired. For each point, select the appropriate robot.
            # TODO: are the points really paired ok?
            # Access robot_list
            robot_list_lock.acquire()
            try:
                if len(robot_list) > 0:
                    for robot in robot_list:
                        closest_point = robot.leading_point.get_nearest_point(20, list(paired_points.keys()))
                        if closest_point is None:
                            logger.warning("Robot " + robot.robot_name + " has been removed from the game!")
                            robot_list.remove(robot)
                            pass
                        else:
                            logger.debug("new closest point! " + str(closest_point.x) + "," + str(closest_point.y))
                            robot.leading_point = closest_point
                            # Get corresponding paired point for the closest point
                            robot.trailing_point = paired_points[closest_point]
                            logger.debug("New points for robot " + str(robot.robot_name) + ": " + str(
                                robot.leading_point.x) + ", " + str(robot.leading_point.y) + ";" + str(
                                robot.trailing_point.x) + ", " + str(robot.trailing_point.y))
                            for robot_to_check in robot_list:
                                if robot_collision_controller.is_robot1_in_collision_with_robot2(robot, robot_to_check):
                                    logger.debug("Robot " + robot.robot_name + " is on collision course with " +
                                                 robot_to_check.robot_name)
                                    robot.is_on_collision_course = True
                                else:
                                    robot.is_on_collision_course = False

                            robot.move_robot_to_next_position(command_controller, city_builder)
                else:
                    logger.info("No robots contained in list.")
            finally:
                robot_list_lock.release()
        else:
            logger.debug("Length of leading points and length of trailing points not equal. Error occurred.")

        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            break

        cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()


# Run async registration service
register_thread = threading.Thread(target=RobotRegistrationController.listen_for_registrations,
                                   args=(command_controller.sock, robot_list, city_builder.streets['D1N'],
                                         robot_list_lock))
# Set as daemon (program can exit even if this thread is still running)
register_thread.daemon = True

register_thread.start()
camera_thread = threading.Thread(target=run_camera)
camera_thread.start()
