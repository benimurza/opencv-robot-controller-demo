from citygraph import CityGraph
from trafficlightcontroller import TrafficlightController

graph = CityGraph()
print(graph.get_shortest_path('D1N', 'D3S'))
print(graph.get_next_position('D1N', 'D3S'))

c = TrafficlightController()
c.start_automatic_trafficlight_algorithm()