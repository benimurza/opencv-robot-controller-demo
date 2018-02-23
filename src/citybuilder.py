# Constructs the city with default parameters
# TODO: read params from a file
import cv2
import xml.etree.cElementTree as XmlParser

from intersection import Intersection
from maputils import MapPoint, MapHeading
from roadcomponent import RoadComponent
from street import Street
import logging

logger = logging.getLogger("CityBuilder")


class CityBuilder:
    def __init__(self):
        # Dictionary containing a street object for each street name (key)
        self.streets = dict()
        self.corresponding_intersections = dict()
        self.adjacent_street_names = dict()

        street_config_root = XmlParser.parse("streetconfig.xml").getroot()
        xml_street_list = street_config_root[0]
        for xml_street in xml_street_list:
            street = Street()
            street.street_name = xml_street.attrib['name']
            street.traffic_light_number = int(xml_street.attrib['trafficLightNumber'])
            for xml_street_child in xml_street.iter('RoadComponent'):
                start_point = MapPoint(int(xml_street_child[0].attrib['x']), int(xml_street_child[0].attrib['y']))
                end_point = MapPoint(int(xml_street_child[1].attrib['x']), int(xml_street_child[1].attrib['y']))
                road_component = RoadComponent(heading=MapHeading[xml_street_child.attrib['heading']],
                                               start=start_point, end=end_point)
                street.road_component_list.append(road_component)
            # Insert adjacent streets
            self.adjacent_street_names[street.street_name] = list()
            for xml_adjacent_street in xml_street.iter('AdjacentStreet'):
                self.adjacent_street_names[street.street_name].append(xml_adjacent_street.attrib['streetName'])
            # Append street to dictionary
            self.streets[street.street_name] = street

        self.build_intersections()

    def __init__1(self):
        # TODO: build streets...
        # Test street D1N
        # Start, end, heading
        road_component_d1n = RoadComponent(MapPoint(951, 50), MapPoint(763, 50), MapHeading.NORTH)
        d1n_street = Street()
        d1n_street.add_road_component(road_component_d1n)
        d1n_street.street_name = 'D1N'
        # TODO: do this for all streets
        d1n_street.traffic_light_number = 10
        self.streets['D1N'] = d1n_street
        self.corresponding_intersections['D1N'] = dict()
        # Possible streets after this one
        self.adjacent_street_names['D1N'] = list()
        # TODO: remove comment after test
        # self.adjacent_street_names['D1N'].append('B1N')
        self.adjacent_street_names['D1N'].append('C2W')

        # Test street C2W
        road_component_c2w = RoadComponent(MapPoint(672, 149), MapPoint(672, 230), MapHeading.WEST)
        c2w_street = Street()
        c2w_street.traffic_light_number = 16
        c2w_street.add_road_component(road_component_c2w)
        c2w_street.street_name = 'C2W'
        self.streets['C2W'] = c2w_street
        self.corresponding_intersections['C2W'] = dict()
        self.adjacent_street_names['C2W'] = list()
        self.adjacent_street_names['C2W'].append('D3S')

        # Create street D3S
        road_component_d3s = RoadComponent(MapPoint(767, 345), MapPoint(945, 349), MapHeading.SOUTH)
        d3s_street = Street()
        d3s_street.traffic_light_number = 7
        d3s_street.add_road_component(road_component_d3s)
        d3s_street.street_name = 'D3S'
        self.streets['D3S'] = d3s_street
        self.corresponding_intersections['D3S'] = dict()
        self.adjacent_street_names['D3S'] = list()
        self.adjacent_street_names['D3S'].append('E2E')

        # Create street E2E
        road_component_e2e = RoadComponent(MapPoint(1047, 255), MapPoint(1047, 151), MapHeading.EAST)
        e2e_street = Street()
        e2e_street.traffic_light_number = 2
        e2e_street.add_road_component(road_component_e2e)
        e2e_street.street_name = 'E2E'
        self.streets['E2E'] = e2e_street
        self.corresponding_intersections['E2E'] = dict()
        self.adjacent_street_names['E2E'] = list()
        self.adjacent_street_names['E2E'].append('D1N')

        # Test street B1N
        # TODO: do something with it
        # Start, end, heading
        road_component_b1n = RoadComponent(MapPoint(316, 48), MapPoint(202, 48), MapHeading.NORTH)
        b1n_street = Street()
        b1n_street.add_road_component(road_component_b1n)
        b1n_street.street_name = 'B1N'
        self.streets['B1N'] = b1n_street
        self.corresponding_intersections['B1N'] = dict()

        # Create intersection between D1N and B1N
        d1n_b1n_intersection = Intersection()
        road_component_d1n_b1n_intersection = RoadComponent(MapPoint(397, 48), MapPoint(316, 48), MapHeading.NORTH)
        d1n_b1n_intersection.add_road_component(road_component_d1n_b1n_intersection)
        self.corresponding_intersections['D1N']['B1N'] = d1n_b1n_intersection

        # Create intersection between D1N and C2W
        d1n_c2w_intersection = Intersection()
        road_component_d1n_c2w_a_intersection = RoadComponent(MapPoint(763, 50), MapPoint(680, 50), MapHeading.NORTH)
        road_component_d1n_c2w_b_intersection = RoadComponent(MapPoint(680, 50), MapPoint(680, 149), MapHeading.WEST)
        d1n_c2w_intersection.add_road_component(road_component_d1n_c2w_a_intersection)
        d1n_c2w_intersection.add_road_component(road_component_d1n_c2w_b_intersection)
        self.corresponding_intersections['D1N']['C2W'] = d1n_c2w_intersection

        # Create intersection between C2W and D3S
        c2w_d3s_intersection = Intersection()
        road_component_c2w_d3s_a_intersection = RoadComponent(MapPoint(675, 239), MapPoint(675, 330), MapHeading.WEST)
        road_component_c2w_d3s_b_intersection = RoadComponent(MapPoint(675, 330), MapPoint(767, 330), MapHeading.SOUTH)
        c2w_d3s_intersection.add_road_component(road_component_c2w_d3s_a_intersection)
        c2w_d3s_intersection.add_road_component(road_component_c2w_d3s_b_intersection)
        self.corresponding_intersections['C2W']['D3S'] = c2w_d3s_intersection

        # Create intersection between D3S and E2E
        d3s_e2e_intersection = Intersection()
        road_component_d3s_e2e_a_intersection = RoadComponent(MapPoint(945, 340), MapPoint(1040, 340), MapHeading.SOUTH)
        road_component_d3s_e2e_b_intersection = RoadComponent(MapPoint(1040, 340), MapPoint(1040, 255), MapHeading.EAST)
        d3s_e2e_intersection.add_road_component(road_component_d3s_e2e_a_intersection)
        d3s_e2e_intersection.add_road_component(road_component_d3s_e2e_b_intersection)
        self.corresponding_intersections['D3S']['E2E'] = d3s_e2e_intersection

        # Create intersection between E2E and D1N
        e2e_d1n_intersection = Intersection()
        road_component_e2e_d1n_a_intersection = RoadComponent(MapPoint(1047, 151), MapPoint(1047, 56), MapHeading.EAST)
        road_component_e2e_d1n_b_intersection = RoadComponent(MapPoint(1047, 56), MapPoint(951, 56), MapHeading.NORTH)
        e2e_d1n_intersection.add_road_component(road_component_e2e_d1n_a_intersection)
        e2e_d1n_intersection.add_road_component(road_component_e2e_d1n_b_intersection)
        self.corresponding_intersections['E2E']['D1N'] = e2e_d1n_intersection

    def get_intersection_between_streets(self, current_street_name, next_street_name):
        return self.corresponding_intersections[current_street_name][next_street_name]

    def get_adjacent_street(self, street_name):
        key = self.adjacent_street_names.get(street_name, None)
        if key is None:
            logger.fatal("No street found. Exiting!")
            exit(0)
        # TODO: not 0! but streets...
        return self.streets[self.adjacent_street_names[street_name][0]]

    def draw_streets_on_opencv_frame(self, frame):
        for street in self.streets:
            for component in self.streets[street].road_component_list:
                cv2.arrowedLine(frame, (component.start_point.x,
                                        component.start_point.y),
                                (component.end_point.x,
                                 component.end_point.y), (0, 0, 255), 2)
                cv2.putText(frame, street, (component.start_point.x, component.start_point.y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (15, 191, 141), 1, cv2.LINE_AA)

    def build_intersections(self):
        for street_name in self.streets.keys():
            for adjacent_street_name in self.adjacent_street_names[street_name]:
                current_street = self.streets[street_name]
                adjacent_street = self.streets[adjacent_street_name]

                current_street_heading = current_street.road_component_list[
                    len(current_street.road_component_list) - 1].heading
                adjacent_street_heading = adjacent_street.road_component_list[0].heading

                end_point_incoming_street = current_street.road_component_list[
                    len(current_street.road_component_list) - 1].end_point
                start_point_outgoing_street = adjacent_street.road_component_list[0].start_point
                # Always take the last road component
                if current_street_heading == adjacent_street_heading:
                    # Current street and adjacent street have the same heading. Intersection will have only one
                    # road component; it starts where the incoming street ends, and ends where the outgoing street
                    # starts.
                    intersection_road_component = RoadComponent(heading=adjacent_street.road_component_list[0].heading,
                                                                start=end_point_incoming_street,
                                                                end=start_point_outgoing_street)
                    intersection = Intersection()
                    intersection.add_road_component(intersection_road_component)

                    # Place the intersection in the intersection dictionary
                    if street_name not in self.corresponding_intersections:
                        self.corresponding_intersections[street_name] = dict()
                    self.corresponding_intersections[street_name][adjacent_street_name] = intersection
                else:
                    # Streets have different heading, meaning 2 road components (90 degree turn)
                    intersection = Intersection()
                    intersection_first_line_start = end_point_incoming_street
                    if current_street_heading in (MapHeading.NORTH, MapHeading.SOUTH):
                        intersection_first_line_end = MapPoint(x=start_point_outgoing_street.x,
                                                               y=end_point_incoming_street.y)
                    else:
                        intersection_first_line_end = MapPoint(x=end_point_incoming_street.x,
                                                               y=start_point_outgoing_street.y)
                    intersection_first_road_component = RoadComponent(heading=current_street_heading,
                                                                      start=intersection_first_line_start,
                                                                      end=intersection_first_line_end)
                    intersection.add_road_component(intersection_first_road_component)

                    intersection_second_line_start = intersection_first_line_end
                    intersection_second_line_end = start_point_outgoing_street
                    intersection_second_road_component = RoadComponent(heading=adjacent_street_heading,
                                                                       start=intersection_second_line_start,
                                                                       end=intersection_second_line_end)
                    intersection.add_road_component(intersection_second_road_component)

                    if street_name not in self.corresponding_intersections:
                        self.corresponding_intersections[street_name] = dict()
                    self.corresponding_intersections[street_name][adjacent_street_name] = intersection
