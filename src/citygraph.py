import networkx as nx
import logging
from citybuilder import CityBuilder

city_builder = CityBuilder()

logger = logging.getLogger("CityGraph")


class CityGraph:
    dynamicGraph = nx.DiGraph()
    dyPath = dict()

    def __init__(self):
        self.dynamicGraph = nx.DiGraph()
        self.dynamicGraph.add_nodes_from(list(city_builder.streets.keys()))

        for key, values in city_builder.adjacent_street_names.items():
            for item in values:
                self.dynamicGraph.add_edge(key, item)

        self.dyPath = dict(nx.all_pairs_shortest_path(self.dynamicGraph))

    def get_shortest_path(self, source_street_name, destination_street_name):
        logger.debug("Shortest path: " + ', '.join(self.dyPath[source_street_name][destination_street_name]))
        return self.dyPath[source_street_name][destination_street_name]

    def get_next_position(self, police_street_name, robber_street_name):
        path = self.dyPath[police_street_name][robber_street_name]
        if police_street_name == robber_street_name:
            logger.debug("Police at <" + police_street_name + ">, robber at <" + robber_street_name + ">, next step: " + path[0])
            return path[0]
        else:
            logger.debug("Police at <" + police_street_name + ">, robber at <" + robber_street_name + ">, next step: " + path[1])
            return path[1]
