# Constructs the city with default parameters
# TODO: read params from a file
import random

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

    def get_intersection_between_streets(self, current_street_name, next_street_name):
        return self.corresponding_intersections[current_street_name][next_street_name]

    def get_adjacent_street(self, street_name):
        key = self.adjacent_street_names.get(street_name, None)
        if key is None:
            logger.fatal("No street found. Exiting!")
            exit(0)
        # TODO: not 0! but streets...
        return self.streets[self.adjacent_street_names[street_name][
            random.randint(0, len(self.adjacent_street_names[street_name]) - 1)]]

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
