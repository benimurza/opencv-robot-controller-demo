import math


def sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def rotate_right(v):
    return v[1], -v[0]


def rotate_left(v):
    return -v[1], v[0]


def length(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def unit(v):
    vector_length = length(v)
    return v[0] / vector_length, v[1] / vector_length


def mult(v, factor):
    return v[0] * factor, v[1] * factor


def as_int(v):
    return int(v[0]), int(v[1])


def distance(v1, v2):
    return length(sub(v2, v1))