class GameInterfaceCar:
    def to_json(self):
        return "[{'id':'1'},{'id':'2'}]"


class GameInterfaceCarPosition:
    carId = None
    pos_x = None
    pos_y = None
    rotation = None

    def __calc_offset_rotation__(self):
        return (self.rotation + 270) % 360

    def to_json(self):
        return "{'carId':'" + str(self.carId) + "', 'rotation':'" + str(
            self.__calc_offset_rotation__()) + "','position':{'x':'" + str(
            self.pos_x) + "', 'y':'" + str(self.pos_y) + "'}}"


class GameInterfaceCarPositionList:
    list_of_cars = None

    def __init__(self):
        self.list_of_cars = list()

    def to_json(self):
        json_string = "["
        for car in self.list_of_cars:
            json_string += car.to_json()
            json_string += ','
        json_string = json_string[:-1]
        json_string += "]"
        return json_string
