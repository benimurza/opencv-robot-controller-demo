from citygraph import CityGraph

graph = CityGraph()
print(graph.get_shortest_path('D1N', 'D3S'))
print(graph.get_next_position('D1N', 'D3S'))
