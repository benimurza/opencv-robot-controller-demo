from trafficlightcontroller import TrafficlightController


class CommandLineInterpreter:
    traffic_light_controller = TrafficlightController()

    def set_traffic_light(self, input_text):
        # format input_Text (remove unnecessary whitespaces
        input_text = " ".join(input_text.split())
        # split string
        split = input_text.split(" ")
        if split[0] == "set":
            trafficlight = split[1]
            try:
                number = int(trafficlight)
                if 0 < number < 33:
                    color = split[2]
                    if color in ('green', 'red'):
                        self.traffic_light_controller.set_trafficlight(number, color)
                        success = "Trafficlight " + trafficlight + " is set to " + color
                        return True, success
                    else:
                        error = "Error: " + color + " is not possible. Choose 'green' or 'red'"
                        return False, error
                else:
                    error = "Error: There is no Trafficlight with number " + trafficlight
                    return False, error
            except ValueError:
                error = "Error NaN: '" + trafficlight + "' is not a number"
                return False, error
        else:
            error = "Error: Command not found '" + split[0] + "'"
            return False, error
