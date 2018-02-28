import logging
import math
from enum import Enum

from citygraph import CityGraph
from maputils import MapHeading, MapPoint
from trafficlightstatusprovider import TrafficLightStatusProvider, TrafficLightStatus
from udpcommandcontroller import RobotCommands

logger = logging.getLogger("RoadComponent")


class RobotRole(Enum):
    CITIZEN = 0
    POLICE = 1
    ROBBER = 2


# TODO: clean up class attributes (switch to instance attributes!)
class Robot:
    # Class-wide parameter
    traffic_lights_status_provider = TrafficLightStatusProvider()
    city_graph = CityGraph()

    def __init__(self):
        # Current command counter for this robot
        # TODO: check overflow!
        self.command_counter = 0

        self.robot_id = None

        # Position information
        self.heading = None
        self.leading_point = None
        self.trailing_point = None

        # IP Address of robot, retrieved upon registering
        self.ip_address = None

        # Street the robot is currently on
        self.current_street = None

        # The intersection the robot is currently on
        self.current_intersection = None

        # Road component the robot is currently on
        self.current_road_component = None

        # Flag - if robot is on a street, it is true. If the robot is in an intersection, it is false.
        self.is_robot_on_street = True

        # If a street or an intersection has multiple road components, this index keeps track of the current one
        self.current_road_component_index = 0

        # For logging purposes
        self.robot_name = None

        # Game interface ID
        self.game_interface_id = None

        # Signal if this robot is on a collision course and should stop
        self.is_on_collision_course = False

        # Duty cycle used in forward and directional motion
        self.duty_cycle_forward = 55
        self.duty_cycle_direction = 25

        # Flag to signal a chase is taking place in the city. For now only relevant for the police robot
        self.is_police_chase_ongoing = False

        # By default, all robots are citizens
        self.role = RobotRole.CITIZEN

    def update_heading(self):
        self.heading = self.get_heading()

    def get_heading(self):

        theta_degrees = self.get_heading_in_degrees()

        if 45 <= theta_degrees <= 135:
            return MapHeading.EAST
        if 135 <= theta_degrees <= 225:
            return MapHeading.SOUTH
        if 225 <= theta_degrees <= 315:
            return MapHeading.WEST
        return MapHeading.NORTH

    def get_heading_in_degrees(self):
        theta_radians = math.atan2(self.leading_point.y - self.trailing_point.y,
                                   self.leading_point.x - self.trailing_point.x)

        theta_degrees = (theta_radians + math.pi) * 360.0 / (2.0 * math.pi)
        return theta_degrees

    def get_next_street(self, city_builder, robber_street_name=None):
        if self.role == RobotRole.POLICE:
            if robber_street_name is not None:
                # Shortest path to robber
                return city_builder.streets[
                    self.city_graph.get_next_position(self.current_street.street_name, robber_street_name)]
        return city_builder.get_adjacent_street(self.current_street.street_name)

    def should_stop_at_traffic_light(self):
        if self.role == RobotRole.POLICE and self.is_police_chase_ongoing:
            # Police does not have to wait for green light while on chase
            logger.info("Police not waiting for traffic light.")
            return False
        elif self.current_street.traffic_light_number is not None:
            if self.traffic_lights_status_provider.get_status_of_traffic_light(
                    self.current_street.traffic_light_number) != TrafficLightStatus.LIGHT_GREEN:
                logger.debug(self.robot_name + "Light is still red")
                # Traffic light still red. Robot should stop.
                return True
        else:
            logger.warning(self.robot_name + "No traffic light number. Assuming green...")
            return False

    def move_robot_to_next_position(self, command_controller, city_builder, robber_street_name=None):
        if self.is_on_collision_course:
            return
        if self.is_robot_on_street:
            self.current_road_component = self.current_street.road_component_list[self.current_road_component_index]
        else:
            self.current_road_component = \
                self.current_intersection.road_component_list[self.current_road_component_index]
        used_road = self.current_road_component

        if used_road.has_end_been_reached(self):

            if self.is_robot_on_street:

                # Check if there are any road components left on the street, or if it really is the end of street
                if self.current_street.get_number_of_road_components() <= (self.current_road_component_index + 1):

                    # End of street has been reached (end of all road components)
                    logger.debug(self.robot_name + "Robot at the end of street. Checking traffic light (if existent)")

                    # Check if robot should stop at traffic light
                    if self.should_stop_at_traffic_light():
                        # Robot is still waiting for green. Do nothing, return immediately.
                        return

                    # Mark next street
                    next_street = self.get_next_street(city_builder, robber_street_name)

                    logger.info(
                        "Robot is on " + self.current_street.street_name + ", moving on to " + next_street.street_name)

                    # Get intersection between current and next street
                    self.current_intersection = city_builder.get_intersection_between_streets(
                        self.current_street.street_name, next_street.street_name)

                    # End of street, switch to intersection
                    self.is_robot_on_street = False

                    # Reset road component index
                    self.current_road_component_index = 0

                    # Next street is current street
                    self.current_street = next_street

                else:
                    # Street still has road components left. Move on to next road component
                    self.current_road_component_index += 1

            else:
                # Robot is in intersection
                logger.debug(self.robot_name + "Robot in intersection")
                # Check if there are more road components
                if self.current_intersection.get_number_of_road_components() <= (self.current_road_component_index + 1):
                    # End of intersection, switch to street
                    self.is_robot_on_street = True
                    # Reset road component index
                    self.current_road_component_index = 0
                else:
                    # Move on to next road component index
                    self.current_road_component_index += 1
            return
        # Robot is on its way. Direct it so that it stays on the street (in tolerance area)
        if used_road.is_robot_in_tolerance_area(self):
            self.command_counter = command_controller.send_command_forward(self.ip_address, self.duty_cycle_forward,
                                                                           self.command_counter)
        else:
            if used_road.is_robot_headed_towards_road_component(self):
                self.command_counter = command_controller.send_command_forward(self.ip_address, self.duty_cycle_forward,
                                                                               self.command_counter)
            else:
                command = used_road.get_correct_direction_for_robot(self)
                if command == RobotCommands.GO_LEFT:
                    # robot_move_left()
                    self.command_counter = command_controller.send_command_left_one_wheel(self.ip_address,
                                                                                          self.duty_cycle_direction,
                                                                                          self.command_counter)
                    # command_controller.send_command_left(self.ip_address)
                elif command == RobotCommands.GO_RIGHT:
                    # robot_move_right()
                    self.command_counter = command_controller.send_command_right_one_wheel(self.ip_address,
                                                                                           self.duty_cycle_direction,
                                                                                           self.command_counter)
                    # command_controller.send_command_right(self.ip_address)
                elif command == RobotCommands.GO_FORWARD:
                    self.command_counter = command_controller.send_command_forward(self.ip_address,
                                                                                   self.duty_cycle_forward,
                                                                                   self.command_counter)
