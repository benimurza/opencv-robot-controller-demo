# A road component is a line connecting two points on the map; it could be part of an intersection, or part of a street
from maputils import MapHeading
from udpcommandcontroller import RobotCommands


class RoadComponent:
    tolerance_y_axis = 3
    tolerance_x_axis = 3
    start_point = None
    end_point = None
    heading = None

    def __init__(self, start, end, heading):
        self.start_point = start
        self.end_point = end
        self.heading = heading

    # ALL DIRECTIONS OK
    def has_end_been_reached(self, robot):
        if self.heading == MapHeading.NORTH:
            # only x values must be compared
            if (self.end_point.x >= robot.leading_point.x) or (self.end_point.x >= robot.trailing_point.x):
                return True
            return False
        elif self.heading == MapHeading.WEST:
            # only y values must be compared
            if (self.end_point.y <= robot.leading_point.y) or (self.end_point.y <= robot.leading_point.y):
                return True
            return False
        elif self.heading == MapHeading.SOUTH:
            # Only x values must be compared
            if (self.end_point.x <= robot.leading_point.x) or (self.end_point.x <= robot.trailing_point.x):
                return True
            return False
        elif self.heading == MapHeading.EAST:
            if (self.end_point.y >= robot.leading_point.y) or (self.end_point.y >= robot.trailing_point.y):
                return True
            return False
        else:
            print("No map direction.")

    # ALL DIRECTIONS OK
    def is_robot_in_tolerance_area(self, robot):
        if self.heading in {MapHeading.NORTH, MapHeading.SOUTH}:
            y_min = self.start_point.y - self.tolerance_y_axis
            y_max = self.start_point.y + self.tolerance_y_axis
            # Only look at y values
            # Check if both ys are in range
            if (y_min <= robot.leading_point.y <= y_max) and (y_min <= robot.trailing_point.y <= y_max):
                return True
            else:
                return False
        else:
            # Only look at x values
            x_min = self.start_point.x - self.tolerance_x_axis
            x_max = self.start_point.x + self.tolerance_x_axis
            # Check if xs are in range
            if (x_min <= robot.leading_point.x <= x_max) and (x_min <= robot.trailing_point.x <= x_min):
                return True
            else:
                return False

    # TODO: move method(s) to another class
    # TODO: handle case where robot does a 180 degree turn!!! -> it handles itself, maybe optimize it?
    # ALL DIRECTIONS OK
    def is_robot_headed_towards_road_component(self, robot):
        if self.heading in {MapHeading.NORTH, MapHeading.SOUTH}:
            # Check ys
            if robot.trailing_point.y == robot.leading_point.y:
                return False
            if robot.trailing_point.y < robot.leading_point.y:
                if robot.leading_point.y < self.start_point.y:
                    return True
                else:
                    return False
            if robot.trailing_point.y > robot.leading_point.y:
                if robot.leading_point.y > self.start_point.y:
                    return True
                else:
                    return False
        elif self.heading in {MapHeading.WEST, MapHeading.EAST}:
            if robot.trailing_point.x == robot.leading_point.x:
                # Robot is parallel to the line
                return False
            if robot.trailing_point.x < robot.leading_point.x:
                if robot.leading_point.x < self.start_point.x:
                    return True
                else:
                    return False
            if robot.trailing_point.x > robot.leading_point.x:
                if robot.leading_point.x > self.start_point.x:
                    return True
                else:
                    return False
        else:
            print("What direction?")
            return False

    # TODO: move to better controller
    # TODO: split depending on heading into "private" functions
    # Get correct direction for robot if IT IS NOT HEADED TOWARD THE ROAD!
    # ALL DIRECTIONS OK
    def get_correct_direction_for_robot(self, robot):
        if self.heading == MapHeading.NORTH:
            if robot.trailing_point.y == robot.leading_point.y:
                print("Trailing point same as leading point")
                if robot.leading_point.y < self.start_point.y:
                    return RobotCommands.GO_LEFT
                elif robot.leading_point.y > self.start_point.y:
                    return RobotCommands.GO_RIGHT
                else:
                    return RobotCommands.GO_FORWARD
            if robot.trailing_point.y > robot.leading_point.y:
                # Assume heading has been checked
                return RobotCommands.GO_LEFT
            if robot.trailing_point.y < robot.leading_point.y:
                # Assume heading has been checked
                return RobotCommands.GO_RIGHT
        if self.heading == MapHeading.SOUTH:
            if robot.trailing_point.y == robot.leading_point.y:
                print("Trailing point same as leading point")
                if robot.leading_point.y < self.start_point.y:
                    return RobotCommands.GO_RIGHT
                elif robot.leading_point.y > self.start_point.y:
                    return RobotCommands.GO_LEFT
                else:
                    return RobotCommands.GO_FORWARD
            if robot.trailing_point.y > robot.leading_point.y:
                # Assume heading has been checked
                return RobotCommands.GO_RIGHT
            if robot.trailing_point.y < robot.leading_point.y:
                # Assume heading has been checked
                return RobotCommands.GO_LEFT
        if self.heading == MapHeading.EAST:
            if robot.trailing_point.x == robot.leading_point.x:
                if robot.leading_point.x < self.start_point.x:
                    return RobotCommands.GO_RIGHT
                elif robot.leading_point.x > self.start_point.x:
                    return RobotCommands.GO_LEFT
                else:
                    # Robot is right on the line
                    return RobotCommands.GO_FORWARD
            if robot.trailing_point.x > robot.leading_point.x:
                return RobotCommands.GO_RIGHT
            if robot.trailing_point.x < robot.leading_point.x:
                return RobotCommands.GO_LEFT

        if self.heading == MapHeading.WEST:
            if robot.trailing_point.x == robot.leading_point.x:
                if robot.leading_point.x < self.start_point.x:
                    return RobotCommands.GO_LEFT
                elif robot.leading_point.x > self.start_point.x:
                    return RobotCommands.GO_RIGHT
                else:
                    # Robot is right on the line
                    return RobotCommands.GO_FORWARD
            if robot.trailing_point.x > robot.leading_point.x:
                return RobotCommands.GO_LEFT
            if robot.trailing_point.x < robot.leading_point.x:
                return RobotCommands.GO_RIGHT
