class Street:
    def __init__(self):
        # Each street has at least one road component
        self.road_component_list = list()
        # Traffic light number at the end of the street (corresponding to this street)
        self.traffic_light_number = None

        # Name, as string
        self.street_name = None

    def add_road_component(self, road_component):
        self.road_component_list.append(road_component)

    def get_number_of_road_components(self):
        return len(self.road_component_list)