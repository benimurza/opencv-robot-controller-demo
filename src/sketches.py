import cv2

from colordetection import ColorDetection
from maputils import *

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# List of robots
robot_list = list()


while 1:
    # Take each frame
    _, frame = cap.read()

    lead_points, trail_points = ColorDetection.get_blue_and_green_points_from_frame(frame)

    if len(lead_points) == len(trail_points):
        paired_points = PointPairing.pair_point_lists(lead_points, trail_points, 20)
        for pp in paired_points:
            mid_point = MapPoint.calculate_mid_point(pp[0], pp[1])
            if mid_point is not None:
                cv2.circle(frame, (mid_point.x, mid_point.y), 4, (28, 66, 62), -1)

    k = cv2.waitKey(40) & 0xFF
    if k == 27:
        break

    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()