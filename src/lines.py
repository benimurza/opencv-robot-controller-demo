# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines-in-python
import vectors
import numpy as np
import cv2


def intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        print(line1, line2)
        demo = np.zeros([720, 1280, 3], dtype=np.uint8)
        cv2.line(demo, vectors.as_int(line1[0]), vectors.as_int(line1[1]), (0, 0, 255), thickness=5)
        cv2.line(demo, vectors.as_int(line2[0]), vectors.as_int(line2[1]), (0, 255, 0), thickness=5)
        cv2.imshow("demo", demo)
        cv2.waitKey(0)
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def offset_point(point, rotate_function, offset_length, predecessor, successor):
    pre_offset_vector = None
    suc_offset_vector = None
    if predecessor:
        pre_direction = vectors.unit(vectors.sub(point, predecessor))
        pre_offset_vector = vectors.mult(rotate_function(pre_direction), offset_length)
    if successor:
        suc_direction = vectors.unit(vectors.sub(successor, point))
        suc_offset_vector = vectors.mult(rotate_function(suc_direction), offset_length)

    if predecessor and successor:
        return intersection((vectors.add(predecessor, pre_offset_vector), vectors.add(point, pre_offset_vector)),
                            (vectors.add(point, suc_offset_vector), vectors.add(successor, suc_offset_vector)))
    elif predecessor:
        return vectors.add(point, pre_offset_vector)
    elif successor:
        return vectors.add(point, suc_offset_vector)
    else:
        raise Exception('at least one of predecessor and successor have to be set')


def offset_all(path, rotate_function, offset_length):
    if len(path) < 2:
        return path
    offset_path = []
    for i in range(0, len(path)):
        predecessor = successor = None
        point = path[i]
        if i - 1 >= 0:
            predecessor = path[i - 1]
        if i + 1 < len(path):
            successor = path[i + 1]
        offset_path.append(offset_point(point, rotate_function, offset_length, predecessor, successor))
    return offset_path
