from trafficlightstatusprovider import TrafficLightStatusProvider, TrafficLightStatus
import cv2


class TrafficLightDrawUtility:
    traffic_light_status_provider = TrafficLightStatusProvider()
    colors = {
        'green': (0, 255, 0),
        'red': (0, 0, 255)
    }
    positions = {
        1: (1086, 25),
        2: (1086, 147),
        3: (1086, 390),
        4: (1086, 519),
        5: (965, 144),
        6: (965, 268),
        7: (965, 388),
        8: (965, 518),
        9: (965, 636),
        10: (750, 25),
        11: (750, 143),
        12: (750, 267),
        13: (750, 390),
        14: (750, 513),
        15: (630, 143),
        16: (630, 264),
        17: (630, 390),
        18: (630, 510),
        19: (630, 631),
        20: (425, 25),
        21: (425, 138),
        22: (425, 263),
        23: (425, 382),
        24: (425, 516),
        25: (310, 141),
        26: (310, 264),
        27: (310, 380),
        28: (310, 508),
        29: (310, 617),
        30: (146, 262),
        31: (146, 378),
        32: (36, 263)
    }
    text_positions = {
        1: (1084, 27),
        2: (1084, 149),
        3: (1084, 392),
        4: (1084, 521),
        5: (963, 146),
        6: (963, 270),
        7: (963, 390),
        8: (963, 520),
        9: (963, 638),
        10: (745, 27),
        11: (745, 145),
        12: (745, 269),
        13: (745, 392),
        14: (745, 515),
        15: (625, 145),
        16: (625, 266),
        17: (625, 392),
        18: (625, 512),
        19: (625, 633),
        20: (420, 27),
        21: (420, 140),
        22: (420, 265),
        23: (420, 384),
        24: (420, 518),
        25: (305, 143),
        26: (305, 266),
        27: (305, 382),
        28: (305, 510),
        29: (305, 619),
        30: (141, 264),
        31: (141, 380),
        32: (31, 265)
    }

    def draw_traffic_light_status(self, frame):
        trafficlights = self.traffic_light_status_provider.get_status_of_all_traffic_lights()
        for item in self.positions:
            coordinates = self.positions[item]
            text_coordinates = self.text_positions[item]
            color = (0, 0, 0)
            if trafficlights[item] == TrafficLightStatus.LIGHT_GREEN:
                color = self.colors['green']
            elif trafficlights[item] == TrafficLightStatus.LIGHT_RED:
                color = self.colors['red']
            cv2.circle(frame, coordinates, 10, color, -1)
            cv2.putText(frame, str(item), text_coordinates, 0, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
