import math
from maputils import MapHeading, MapPoint
from trafficlightstatusprovider import TrafficLightStatusProvider, TrafficLightStatus
from udpcommandcontroller import RobotCommands


# TODO: clean up class attributes (switch to instance attributes!)
class Robot:
    # Class-wide parameter
    traffic_lights_status_provider = TrafficLightStatusProvider()

    def __init__(self):
        self.leading_point = MapPoint(0, 0)
        self.trailing_point = MapPoint(0, 0)
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

        self.duty_cycle_forward = 60
        self.duty_cycle_direction = 35

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

    def move_robot_to_next_position(self, command_controller, city_builder):
        if self.is_on_collision_course:
            return
        if self.is_robot_on_street:
            self.current_road_component = self.current_street.road_component_list[self.current_road_component_index]
        else:
            self.current_road_component = \
                self.current_intersection.road_component_list[self.current_road_component_index]
        used_road = self.current_road_component
        print(str(self.leading_point.x) + " " + str(self.leading_point.y))
        print(str(self.trailing_point.x) + " " + str(self.trailing_point.y))

        if used_road.has_end_been_reached(self):
            if self.is_robot_on_street:
                print(self.robot_name + "Robot at the end of street. Checking traffic light (if existent)")
                # TODO: multi-threaded...
                if self.current_street.traffic_light_number is not None:
                    if self.traffic_lights_status_provider.get_status_of_traffic_light(
                            self.current_street.traffic_light_number) != TrafficLightStatus.LIGHT_GREEN:
                        print(self.robot_name + "Light is still red")
                        return
                else:
                    print(self.robot_name + "No traffic light number. Assuming green...")

            print(self.robot_name + "FULL STOP. END OF STREET")
            # command_controller.send_command_stop(self.ip_address)

            if self.is_robot_on_street:
                # TODO: check if street has multiple road components!
                # Mark next street
                next_street = city_builder.get_adjacent_street(self.current_street.street_name)

                print(self.robot_name + "Next street is: " + next_street.street_name)

                # Robot is now in intersection
                self.is_robot_on_street = False

                # Move on to the next road component
                self.current_intersection = city_builder.get_intersection_between_streets(
                    self.current_street.street_name, next_street.street_name)

                # Mark next street
                self.current_street = next_street

                # Reset component index
                self.current_road_component_index = 0
            else:
                print(self.robot_name + "Robot in intersection")
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
        if used_road.is_robot_in_tolerance_area(self):
            print(self.robot_name + "FORWARD - TOL AREA")
            command_controller.send_command_forward(self.ip_address, self.duty_cycle_forward)
        else:
            if used_road.is_robot_headed_towards_road_component(self):
                print(self.robot_name + "HEADED - FORWARD")
                command_controller.send_command_forward(self.ip_address, self.duty_cycle_forward)
            else:
                command = used_road.get_correct_direction_for_robot(self)
                if command == RobotCommands.GO_LEFT:
                    print(self.robot_name + "C LEFT")
                    # robot_move_left()
                    command_controller.send_command_left_one_wheel(self.ip_address, self.duty_cycle_direction)
                    # command_controller.send_command_left(self.ip_address)
                elif command == RobotCommands.GO_RIGHT:
                    print(self.robot_name + "C RIGHT")
                    # robot_move_right()
                    command_controller.send_command_right_one_wheel(self.ip_address, self.duty_cycle_direction)
                    # command_controller.send_command_right(self.ip_address)
                elif command == RobotCommands.GO_FORWARD:
                    print(self.robot_name + "C FORWARD")
                    command_controller.send_command_forward(self.ip_address, self.duty_cycle_forward)
