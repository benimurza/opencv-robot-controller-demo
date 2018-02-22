import cv2
import numpy as np

from maputils import MapPoint

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while 1:
    _, frame = cap.read()

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

                print("Blue center: " + str(center_blue))
                if radius > 5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, center_blue, 2, (0, 0, 255), -1)

        except ZeroDivisionError as z:
            print("ZDE in blue. Blue not ready.")
    else:
        print("Blue not ready.")

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

                print("Green center: " + str(center_green))

                if radius > 5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, center_green, 2, (0, 0, 255), -1)

                # cv2.arrowedLine(frame, center_green, center_blue, (0, 0, 255))
        except ZeroDivisionError as z:
            print("ZDE in green. Green not ready.")

    else:
        print("Green not ready.")

    if len(blue_points) == len(green_points):
        # Pair points
        for blue_point in blue_points:
            nearest_green_point = blue_point.get_nearest_point(green_points)
            mid_point = MapPoint.calculate_mid_point(blue_point, nearest_green_point)
            cv2.circle(frame, (mid_point.x, mid_point.y), 2, (0, 0, 255), -1)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(40) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
