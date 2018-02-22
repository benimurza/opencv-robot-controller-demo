class Street:
    # Tolerance in pixels for the X axis
    tolerance_y_axis = 3

    # Traffic light number at the end of the street (corresponding to this street)
    traffic_light_number = None

    # Location
    start_point = None
    end_point = None
    heading = None

    # Name, as string
    street_name = None

    # Each street has at least one road component
    road_component_list = None

    def __init__(self):
        self.road_component_list = list()

    def add_road_component(self, road_component):
        self.road_component_list.append(road_component)

    def get_number_of_road_components(self):
        return len(self.road_component_list)