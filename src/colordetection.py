import cv2
import numpy as np

from maputils import MapPoint


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

        return blue_points, green_points

    @staticmethod
    def process_frame(frame, green_robot, pink_robot):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        '''
        BLUE
        '''

        lower_blue = np.array([100, 150, 0], np.uint8)
        upper_blue = np.array([140, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_mask = cv2.erode(blue_mask, None, iterations=1)
        blue_mask = cv2.dilate(blue_mask, None, iterations=3)

        contour_blue = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contour_blue) > 0:
            try:
                c = max(contour_blue, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center_blue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                green_robot.leading_point.x = int(M["m10"] / M["m00"])
                green_robot.leading_point.y = int(M["m01"] / M["m00"])

                print("Blue center: " + str(center_blue))
                if radius > 5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, center_blue, 2, (0, 0, 255), -1)

            except ZeroDivisionError as z:
                print("Ups")
        else:
            print("Blue not ready.")

        '''
        GREEN
        '''

        lower_green = np.array([50, 50, 120])
        upper_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)  # I have the Green threshold image.

        green_mask = cv2.erode(green_mask, None, iterations=1)
        green_mask = cv2.dilate(green_mask, None, iterations=3)

        contour_green = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contour_green) > 0:
            c = max(contour_green, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center_green = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("Green center: " + str(center_green))

            green_robot.trailing_point.x = int(M["m10"] / M["m00"])
            green_robot.trailing_point.y = int(M["m01"] / M["m00"])

            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, center_green, 2, (0, 0, 255), -1)

            cv2.arrowedLine(frame, center_green, center_blue, (0, 0, 255))

        else:
            print("Green not ready.")

        '''
        RED
        '''

        # define range of red color in HSV
        lower_red = np.array([0, 150, 150])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        # Upper mask (170-180)
        lower_red = np.array([170, 150, 150])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Join masks
        red_mask = mask0 + mask1
        red_mask = cv2.erode(red_mask, None, iterations=1)
        red_mask = cv2.dilate(red_mask, None, iterations=3)

        contour_red = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contour_red) > 0:
            c = max(contour_red, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center_red = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("Red center: " + str(center_red))

            pink_robot.trailing_point.x = int(M["m10"] / M["m00"])
            pink_robot.trailing_point.y = int(M["m01"] / M["m00"])

            # main_robot.trailing_point.x = int(M["m10"] / M["m00"])
            # main_robot.trailing_point.y = int(M["m01"] / M["m00"])

            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, center_red, 2, (0, 0, 255), -1)

        else:
            print("Red not ready.")

        ''' 
        PINK
        '''

        lower_pink = np.array([152, 104, 150])
        upper_pink = np.array([170, 205, 255])
        pink_mask = cv2.inRange(hsv, lower_pink, upper_pink)  # I have the pink threshold image.

        pink_mask = cv2.erode(pink_mask, None, iterations=1)
        pink_mask = cv2.dilate(pink_mask, None, iterations=3)

        contour_pink = cv2.findContours(pink_mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contour_pink) > 0:
            c = max(contour_pink, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center_pink = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("pink center: " + str(center_pink))

            pink_robot.leading_point.x = int(M["m10"] / M["m00"])
            pink_robot.leading_point.y = int(M["m01"] / M["m00"])

            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, center_pink, 2, (0, 0, 255), -1)

        else:
            print("Pink not ready.")



        cv2.imshow('frame', frame)
