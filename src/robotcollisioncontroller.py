import math
from enum import Enum

from maputils import MapHeading, MapPoint


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

    @staticmethod
    def calculate_distance(robot1, robot2):
        # calculate distance between leading_point of robot1 and leading_point of robot2
        distance_to_leading_point = MapPoint.calculate_distance_between_points(robot1.leading_point,
                                                                               robot2.leading_point)

        # calculate distance between leading_point of robot1 and trailing_point of robot2
        distance_to_trailing_point = MapPoint.calculate_distance_between_points(robot1.leading_point,
                                                                                robot2.trailing_point)

        # return the smaller distance
        return min(distance_to_trailing_point, distance_to_leading_point)

    @staticmethod
    def is_collision_detection_relevant(robot1, robot2):
        first = robot1.get_heading()
        second = robot2.get_heading()
        if first == second:
            # if robot1 is behind robot2:
            heading = robot1.get_heading()
            if heading == MapHeading.NORTH:
                if robot1.leading_point.x > robot2.trailing_point.x:
                    return True
                else:
                    return False
            elif heading == MapHeading.EAST:
                if robot1.leading_point.y > robot2.trailing_point.y:
                    return True
                else:
                    return False
            elif heading == MapHeading.SOUTH:
                if robot1.leading_point.x < robot2.trailing_point.x:
                    return True
                else:
                    return False
            elif heading == MapHeading.WEST:
                if robot1.leading_point.y < robot2.trailing_point.y:
                    return True
                else:
                    return False
        elif first == MapHeading.NORTH:
            if second in (MapHeading.WEST, MapHeading.EAST):
                if robot1.leading_point.x > robot2.leading_point.x:
                    return True
                else:
                    return False
            else:
                return False
        elif first == MapHeading.EAST:
            if second in (MapHeading.NORTH, MapHeading.SOUTH):
                if robot1.leading_point.y > robot2.leading_point.y:
                    return True
                else:
                    return False
            else:
                return False
        elif first == MapHeading.SOUTH:
            if second in (MapHeading.EAST, MapHeading.WEST):
                if robot1.leading_point.x < robot2.leading_point.x:
                    return True
                else:
                    return False
            else:
                return False
        elif first == MapHeading.WEST:
            if second in (MapHeading.SOUTH, MapHeading.NORTH):
                if robot1.leading_point.y < robot2.leading_point.y:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_robot1_in_collision_with_robot2(self, robot1, robot2):
        if robot1 is robot2:
            return robot1.is_on_collision_course

        # if the heading is either the same or not parallel (N-S, S-N, E-W, W-E)
        if self.is_collision_detection_relevant(robot1, robot2):
            distance = abs(self.calculate_distance(robot1, robot2))
            if distance <= self.distance_threshold:
                return True
        return False

    def are_robots_in_collision_course(self, robot_a, robot_b):
        if robot_a.get_heading() == robot_b.get_heading():
            distance = abs(self.calculate_distance_between_two_robots(robot_a, robot_b))

            if distance <= self.distance_threshold:
                # Calculate which robot is ahead
                if robot_a.get_heading() == MapHeading.EAST:
                    # compare y values
                    if robot_a.leading_point.y < robot_b.leading_point.y:
                        # Robot A is forward
                        return RobotCollisionIdentification.FIRST_ROBOT
                    return RobotCollisionIdentification.SECOND_ROBOT
                elif robot_a.get_heading() == MapHeading.WEST:
                    # compare y values
                    if robot_a.leading_point.y < robot_b.leading_point.y:
                        # Robot A is forward
                        return RobotCollisionIdentification.SECOND_ROBOT
                    return RobotCollisionIdentification.FIRST_ROBOT
                elif robot_a.get_heading() == MapHeading.NORTH:
                    # compare x values
                    if robot_a.leading_point.x < robot_b.leading_point.x:
                        return RobotCollisionIdentification.FIRST_ROBOT
                    return RobotCollisionIdentification.SECOND_ROBOT
                elif robot_a.get_heading() == MapHeading.SOUTH:
                    # compare x values
                    if robot_a.leading_point.x < robot_b.leading_point.x:
                        return RobotCollisionIdentification.SECOND_ROBOT
                    return RobotCollisionIdentification.FIRST_ROBOT
        return RobotCollisionIdentification.NO_ROBOT
