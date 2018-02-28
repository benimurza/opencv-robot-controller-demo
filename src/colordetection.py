import cv2
import numpy as np
import logging
from maputils import MapPoint

logger = logging.getLogger("ColorDetection")


class ColorDetection:

    @staticmethod
    def get_blue_and_green_points_from_frame(frame):
        """
        Process an opencv frame and return a list of blue and a list of green points.
        :param frame: Input frame. Frame will be changed in the function.
        :return: List of blue and a list of green points.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100, 150, 0], np.uint8)
        upper_blue = np.array([140, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_mask = cv2.erode(blue_mask, None, iterations=1)
        blue_mask = cv2.dilate(blue_mask, None, iterations=3)

        contour_blue = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[-2]
        blue_points = []
        if len(contour_blue) > 0:
            try:
                for contour in contour_blue:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    M = cv2.moments(contour)
                    center_blue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    blue_points.append(MapPoint(center_blue[0], center_blue[1]))

                    if radius > 5:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, center_blue, 2, (0, 0, 255), -1)

            except ZeroDivisionError as z:
                logger.error("Blue not ready: zero div error.")
        else:
            logger.debug("Blue not ready.")

        lower_green = np.array([50, 50, 120])
        upper_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)  # I have the Green threshold image.

        green_mask = cv2.erode(green_mask, None, iterations=1)
        green_mask = cv2.dilate(green_mask, None, iterations=3)

        contour_green = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)[-2]

        green_points = []
        if len(contour_green) > 0:
            try:
                for contour in contour_green:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    M = cv2.moments(contour)
                    center_green = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    green_points.append(MapPoint(center_green[0], center_green[1]))

                    if radius > 5:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, center_green, 2, (0, 0, 255), -1)

                    # cv2.arrowedLine(frame, center_green, center_blue, (0, 0, 255))
            except ZeroDivisionError as z:
                logger.error("Green not ready: zero div error.")

        else:
            logger.debug("Green not ready.")

        return blue_points, green_points
