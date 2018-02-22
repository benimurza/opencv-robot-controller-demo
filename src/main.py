import asyncio
import threading
# Contains all robots
import cv2
import time

from citybuilder import CityBuilder
from colordetection import ColorDetection
from maputils import PointPairing, MapPoint
from robotregistrationcontroller import RobotRegistrationController
from udpcommandcontroller import UdpCommandController

robot_list = list()

# Global city builder
city_builder = CityBuilder()

command_controller = UdpCommandController()

robot_list_lock = threading.Lock()


def run_camera():
    print("RUNNING CAMERA")
    global city_builder
    global robot_list_lock

    # Set up camera
    cap = cv2.VideoCapture(1)
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
            for pp in paired_points:
                # Points have been paired. For each point, select the appropriate robot.
                # TODO: are the points really paired ok?
                # Access robot_list
                robot_list_lock.acquire()
                try:
                    if len(robot_list) > 0:
                        for robot in robot_list:
                            closest_point = robot.leading_point.get_nearest_point(10, lead_points)
                            if closest_point is None:
                                raise AttributeError("Closest point is None. Robot not found!")
                            else:
                                print("new closest point! " + str(closest_point.x) + "," + str(closest_point.y))
                                robot.leading_point = closest_point
                        pass
                finally:
                    robot_list_lock.release()

                mid_point = MapPoint.calculate_mid_point(pp[0], pp[1])
                if mid_point is not None:
                    cv2.circle(frame, (mid_point.x, mid_point.y), 4, (28, 66, 62), -1)
        else:
            print("Length of leading points and length of trailing points not equal. Error occurred.")

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()

'''
# Run async registration service
register_thread = threading.Thread(target=RobotRegistrationController.listen_for_registrations,
                                   args=(command_controller.sock, robot_list, city_builder.streets['D1N'],
                                         robot_list_lock))
# Set as daemon (program can exit even if this thread is still running)
register_thread.daemon = True

register_thread.start()
'''
camera_thread = threading.Thread(target=run_camera)
camera_thread.start()

# Run camera and process frames
# asyncio.get_event_loop().run_until_complete(run_camera())

# asyncio.get_event_loop().run_forever()
