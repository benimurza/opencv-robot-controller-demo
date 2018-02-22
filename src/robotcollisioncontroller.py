import math
from enum import Enum

from maputils import MapHeading


class RobotCollisionIdentification(Enum):
    FIRST_ROBOT = 0
    SECOND_ROBOT = 1
    NO_ROBOT = 2


class RobotCollisionController:
    distance_threshold = 65

    @staticmethod
    def calculate_distance_between_two_robots(robot_a, robot_b):
        distance = math.sqrt(((robot_a.leading_point.x - robot_b.leading_point.x) ** 2) + (
                (robot_a.leading_point.y - robot_b.leading_point.y) ** 2))
        return distance

    def are_robots_in_collision_course(self, robot_a, robot_b):
        if robot_a.heading == robot_b.heading:
            distance = abs(self.calculate_distance_between_two_robots(robot_a, robot_b))

            if distance <= self.distance_threshold:
                # Calculate which robot is ahead
                if robot_a.heading == MapHeading.EAST:
                    # compare y values
                    if robot_a.leading_point.y < robot_b.leading_point.y:
                        # Robot A is forward
                        return RobotCollisionIdentification.FIRST_ROBOT
                    return RobotCollisionIdentification.SECOND_ROBOT
                elif robot_a.heading == MapHeading.WEST:
                    # compare y values
                    if robot_a.leading_point.y < robot_b.leading_point.y:
                        # Robot A is forward
                        return RobotCollisionIdentification.SECOND_ROBOT
                    return RobotCollisionIdentification.FIRST_ROBOT
                elif robot_a.heading == MapHeading.NORTH:
                    # compare x values
                    if robot_a.leading_point.x < robot_b.leading_point.x:
                        return RobotCollisionIdentification.FIRST_ROBOT
                    return RobotCollisionIdentification.SECOND_ROBOT
                elif robot_a.heading == MapHeading.SOUTH:
                    # compare x values
                    if robot_a.leading_point.x < robot_b.leading_point.x:
                        return RobotCollisionIdentification.SECOND_ROBOT
                    return RobotCollisionIdentification.FIRST_ROBOT
        return RobotCollisionIdentification.NO_ROBOT
