from enum import Enum

import requests
import socket
import json
import ast


class TrafficLightStatus(Enum):
    LIGHT_RED = 0
    LIGHT_GREEN = 1
    LIGHT_NA = 2


class TrafficLightStatusProvider:
    # Including 0
    __max_no_of_traffic_lights__ = 32

    # IP Address of beaglebone - works faster instead of DNS
    __ip_address_of_beaglebone__ = None

    def __init__(self):
        self.__ip_address_of_beaglebone__ = socket.gethostbyname("beaglebone.local")
        if self.__ip_address_of_beaglebone__ is None:
            print("Unable to find IP of beaglebone (traffic light controller). Exiting!")
            exit(-1)

        pass

    def get_status_of_traffic_light(self, traffic_light_number):
        if traffic_light_number > self.__max_no_of_traffic_lights__:
            print("Traffic light number too high.")
            return TrafficLightStatus.LIGHT_NA
        r = requests.get(
            "http://" + str(self.__ip_address_of_beaglebone__) + ":5000/trafficLights/" + str(traffic_light_number))
        if r.content == bytearray('green', 'utf-8'):
            return TrafficLightStatus.LIGHT_GREEN
        elif r.content == bytearray('red', 'utf-8'):
            return TrafficLightStatus.LIGHT_RED
        else:
            return TrafficLightStatus.LIGHT_NA

    def set_status_of_traffic_light(self, traffic_light, color):
        url = "http://" + str(self.__ip_address_of_beaglebone__) + \
              ":5000/trafficLights/" + str(traffic_light) + "/" + color
        r = requests.put(url)
        print(r)

    def set_status_of_traffic_lights(self, traffic_light_array):
        url = "http://" + str(self.__ip_address_of_beaglebone__) + \
              ":5000/trafficLights"
        payload = {
            'trafficlights': traffic_light_array
        }
        r = requests.put(url, data=json.dumps(payload), headers={
            'content-type': "application/json"
        })
        print(r.text)

    def get_status_of_all_traffic_lights(self):
        r = requests.get(
            "http://" + str(self.__ip_address_of_beaglebone__) + ":5000/trafficLights")

        string_array = str(r.content.decode("utf-8"))
        x = ast.literal_eval(string_array)
        values = [TrafficLightStatus.LIGHT_NA]
        for index, item in enumerate(x):
            if item == 'green':
                values.append(TrafficLightStatus.LIGHT_GREEN)
            else:
                values.append(TrafficLightStatus.LIGHT_RED)
        return values
