from citygraph import CityGraph
from trafficlightcontroller import TrafficlightController
from trafficlightstatusprovider import TrafficLightStatusProvider
from cmd_interpreter import CommandLineInterpreter

graph = CityGraph()
print(graph.get_shortest_path('D1N', 'D3S'))
print(graph.get_next_position('D1N', 'D3S'))

#c = TrafficlightController()
#c.start_automatic_trafficlight_algorithm()
#c.set_trafficlight(19, "red")

#p = TrafficLightStatusProvider()
#p.get_status_of_all_traffic_lights()

i = CommandLineInterpreter()
print(i.set_traffic_light("set 20 green"))