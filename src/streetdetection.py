import cv2
import numpy as np
import math

import lines
import vectors


def extract_strips(strip_image):
    roi = np.zeros(strip_image.shape[:2], dtype=np.uint8)
    dx = cv2.Sobel(strip_image, cv2.CV_32F, 1, 0)
    dy = cv2.Sobel(strip_image, cv2.CV_32F, 0, 1)
    dist = cv2.distanceTransform(strip_image, cv2.DIST_L2, 5)
    _, th, _, _ = cv2.minMaxLoc(dist)

    tmp = strip_image.copy()
    _, strip_contours, _ = cv2.findContours(tmp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    strip_paths = []
    for strip_contour in strip_contours:
        poly = cv2.approxPolyDP(strip_contour, th, False)
        for point in poly:
            ptx = point[0, 0]
            pty = point[0, 1]
            x = dx[pty, ptx]
            y = dy[pty, ptx]
            n = math.sqrt(x ** 2 + y ** 2)

            pt2 = (int(ptx + 2.5 * th * x / n), int(pty + 2.5 * th * y / n))
            pt1 = (int(ptx - 0.5 * th * x / n), int(pty - 0.5 * th * y / n))
            cv2.line(roi, pt1, pt2, 255, 2)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        roi = cv2.morphologyEx(roi, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=1)
        roi = cv2.bitwise_and(roi, strip_image)

        _, regions, _ = cv2.findContours(roi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        roi[:] = 0

        path_approximation = []
        for contour_point in strip_contour:
            point = (contour_point[0, 0], contour_point[0, 1])
            for region in regions:
                if -1 != cv2.pointPolygonTest(region, point, False):
                    cv2.drawContours(roi, [region], 0, (255, 255, 255), -1)
                    _, _, _, max_loc = cv2.minMaxLoc(dist, roi)
                    if max_loc not in path_approximation:
                        path_approximation.append(max_loc)
                    break
            roi[:] = 0

        added = False
        for i in range(0, len(path_approximation)):
            rotation = rotate(path_approximation, i)
            if is_valid_path(rotation, strip_image):
                strip_paths.append(rotation)
                added = True
                break
        if not added:
            print("Path may be invalid", path_approximation)
            strip_paths.append(path_approximation)
    return strip_paths


def is_valid_path(path, image):
    for p1, p2 in zip(path, path[1:]):
        midpoint = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
        midpoint_is_on_street = image[midpoint[1], midpoint[0]] > 0
        if not midpoint_is_on_street:
            return False
    return True


def rotate(array, n):
    return array[n:] + array[:n]


def find_street_paths(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("binary", binary)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    opened_binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow("opened", opened_binary)

    _, contours, _ = cv2.findContours(opened_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    strips_only = np.zeros(opened_binary.shape[:2], dtype=np.uint8)
    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 10000:
            cv2.drawContours(strips_only, [contour], 0, 255, cv2.FILLED)
    cv2.imshow("strips_only", strips_only)

    paths = extract_strips(strips_only)

    for path in paths:
        for a, b, c in zip(list(path), list(path)[1:], list(path)[2:]):
            if is_between2(a, c, b) and b in path:
                path.remove(b)
            if is_between(b, c, a) and a in path:
                path.remove(a)
            if is_between(a, b, c) and c in path:
                path.remove(c)

    return paths


def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def is_between(a, b, p, epsilon=10):
    total_distance = vectors.distance(a, b)
    part_distance1 = vectors.distance(a, p)
    part_distance2 = vectors.distance(b, p)
    return abs(part_distance1 + part_distance2 - total_distance) < epsilon


def is_between2(a, b, p, epsilon=10):
    if abs(a[0] - b[0]) < epsilon and abs(a[0] - p[0]) < epsilon and (a[1] < p[1] < b[1] or a[1] > p[1] > b[1]):
        return True
    if abs(a[1] - b[1]) < epsilon and abs(a[1] - p[1]) < epsilon and (a[0] < p[0] < b[0] or a[0] > p[0] > b[0]):
        return True


def get_list_of_street_lines(frame):
    offset_x = 10
    offset_y = 20
    streets = frame[offset_y:630, offset_x:1067]
    street_paths = find_street_paths(streets)

    left_streets = [lines.offset_all(path, vectors.rotate_left, 23) for path in street_paths]
    right_streets = [lines.offset_all(path, vectors.rotate_right, 23) for path in street_paths]

    for path in street_paths:
        # asphalt
        for p1, p2 in zip(path, path[1:]):
            cv2.line(streets, p1, p2, (0, 0, 0), thickness=90)
        # marking
        for p1, p2 in zip(path, path[1:]):
            cv2.line(streets, p1, p2, (255, 255, 255), thickness=5)
        # start & end
        cv2.circle(streets, path[0], 5, (0, 255,), thickness=cv2.FILLED)
        cv2.circle(streets, path[len(path) - 1], 5, (0, 0, 255), thickness=cv2.FILLED)

    list_of_lines = list()

    for path in left_streets:
        for p1, p2 in zip(path, path[1:]):
            offset_p1 = (p1[0] + offset_x, p1[1] + offset_y)
            offset_p2 = (p2[0] + offset_x, p2[1] + offset_y)

            list_of_lines.append((vectors.as_int(offset_p1), vectors.as_int(offset_p2)))
    for path in right_streets:
        for p1, p2 in zip(path, path[1:]):
            offset_p1 = (p1[0] + offset_x, p1[1] + offset_y)
            offset_p2 = (p2[0] + offset_x, p2[1] + offset_y)

            list_of_lines.append((vectors.as_int(offset_p2), vectors.as_int(offset_p1)))

    return list_of_lines


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
_, frame = cap.read()
lol = get_list_of_street_lines(frame)
for line in lol:
    cv2.arrowedLine(frame, line[0], line[1], (0, 0, 255), thickness=5)
cv2.imshow("final", frame)

cv2.waitKey(0)
cv2.destroyAllWindows()
