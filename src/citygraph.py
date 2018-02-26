import networkx as nx
from citybuilder import CityBuilder

city_builder = CityBuilder()


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

    def get_shortest_path(self, source, dest):
        return self.dyPath[source][dest]

    def get_next_position(self, police, robber):
        path = self.dyPath[police][robber]
        if police == robber:
            return path[0]
        else:
            return path[1]
