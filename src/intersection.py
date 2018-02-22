class Intersection:

    def __init__(self):
        self.road_component_list = list()

    def add_road_component(self, component):
        self.road_component_list.append(component)

    def get_number_of_road_components(self):
        return len(self.road_component_list)
