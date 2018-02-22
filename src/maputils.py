from enum import Enum
from math import sqrt


class MapHeading(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


class PointPairing:
    # TODO: what if some points are not paired?
    @staticmethod
    def pair_point_lists(list_a, list_b, max_plausible_distance):
        """
        Given two equally long lists of MapPoints, this function returns a list of paired points
        (leading points paired to their corresponding trailing point)
        :param max_plausible_distance: the maximal plausible distance between two points, in pixels
        :param list_a: leading points
        :param list_b: trailing points
        :returns list of paired points, as list of MapPoint tuples.
        """
        if len(list_a) != len(list_b):
            raise AttributeError("Lists are not of equal length!")

        paired_points = list()

        for point in list_a:
            closest_point = point.get_nearest_point(max_plausible_distance, list_b)
            # TODO: some sanity checks (is return None?)
            paired_points.append((point, closest_point))

        return paired_points


class MapPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_equal_with(self, point):
        if self.x == point.x and self.y == point.y:
            return True
        else:
            return False

    @staticmethod
    # TODO: maybe int? Although float is more exact
    def calculate_distance_between_points(point_a, point_b) -> float:
        return sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)

    def get_nearest_point(self, max_plausible_distance, point_list: list):
        max_distance = max_plausible_distance
        closest_point = None
        for point_to_search in point_list:
            distance = MapPoint.calculate_distance_between_points(self, point_to_search)
            if distance < max_distance:
                closest_point = point_to_search
                max_distance = distance
        return closest_point

    @staticmethod
    def calculate_mid_point(point_a, point_b):
        return MapPoint(int((point_a.x + point_b.x) / 2), int((point_a.y + point_b.y) / 2))
