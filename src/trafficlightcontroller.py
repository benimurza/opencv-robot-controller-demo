from threading import Timer
from trafficlightstatusprovider import TrafficLightStatusProvider, TrafficLightStatus


class TrafficlightController:
    traffic_lights_status_provider = TrafficLightStatusProvider()
    doc = {}
    intersections_trafficlights = {
        1: [1, 2, 5],
        2: [3, 7, 6],
        3: [4, 9, 8],
        4: [10, 11, 15],
        5: [12, 13, 17, 16],
        6: [14, 19, 18],
        7: [20, 21, 25],
        8: [22, 23, 27, 26],
        9: [24, 29, 28],
        10: [30, 31, 32]
    }

    def set_trafficlight(self, number, color):
        for i in self.intersections_trafficlights:
            if number in self.intersections_trafficlights[i]:
                if color == 'green':
                    self.traffic_lights_status_provider.set_status_of_traffic_light(number, 'green')
                    new_list = self.intersections_trafficlights[i]
                    new_list.remove(number)
                    for val in new_list:
                        self.traffic_lights_status_provider.set_status_of_traffic_light(val, 'red')
                elif color == 'red':
                    index = self.intersections_trafficlights[i].index(number)
                    green = index + 1
                    if green == len(self.intersections_trafficlights[i]):
                        green = 0
                    for ind, val in enumerate(self.intersections_trafficlights[i]):
                        if ind == green:
                            self.traffic_lights_status_provider.set_status_of_traffic_light(val, 'green')
                        else:
                            self.traffic_lights_status_provider.set_status_of_traffic_light(val, 'red')

    def start_automatic_trafficlight_algorithm(self):
        # handle each intersection
        trafficlights = {}
        for intersection in self.intersections_trafficlights:
            my_intersection = self.intersections_trafficlights[intersection]
            green = -1
            for i, trafficlight in enumerate(my_intersection):
                if self.traffic_lights_status_provider.get_status_of_traffic_light(
                        trafficlight) == TrafficLightStatus.LIGHT_GREEN:
                    green = i
            index = green + 1
            if index == len(my_intersection):
                index = 0
            for i, trafficlight in enumerate(my_intersection):
                if i == index:
                    trafficlights[trafficlight] = "green"
                else:
                    trafficlights[trafficlight] = "red"
        array = []
        keylist = sorted(trafficlights)
        for key in keylist:
            array.append(trafficlights[key])
        self.traffic_lights_status_provider.set_status_of_traffic_lights(array)
        t = Timer(8.0, self.start_automatic_trafficlight_algorithm)
        t.start()
