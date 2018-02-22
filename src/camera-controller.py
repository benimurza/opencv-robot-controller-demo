import asyncio
import time

import cv2
import websockets

import robot
# Callback for mouse click
from citybuilder import CityBuilder
from colordetection import ColorDetection
from gamewebinterface import GameInterfaceCarPosition, GameInterfaceCarPositionList
from maputils import PointPairing
from robotcollisioncontroller import RobotCollisionController, RobotCollisionIdentification
from udpcommandcontroller import UdpCommandController

# Global city builder
city_builder = CityBuilder()

out_queue = asyncio.Queue(maxsize=1)
command_controller = UdpCommandController()
color_detection = ColorDetection()
robot_collision_controller = RobotCollisionController()


async def capture():
    # Create city builder
    global city_builder
    global color_detection
    global out_queue
    test_street = city_builder.streets['D1N']
    main_robot = robot.Robot()
    main_robot.robot_id, main_robot.ip_address = command_controller.get_next_pending_registration()
    main_robot.current_street = test_street
    main_robot.robot_name = "MAINROBOT: "
    main_robot.duty_cycle_direction = 50
    main_robot.duty_cycle_forward = 100
    main_robot.game_interface_id = 1
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # cv2.namedWindow('frame')
    # cv2.setMouseCallback('frame', draw_circle)
    print("SECOND")
    # Secondary Robot
    second_street = city_builder.streets['C2W']
    second_robot = robot.Robot()
    second_robot.robot_id, second_robot.ip_address = command_controller.get_next_pending_registration()
    second_robot.current_street = second_street
    second_robot.robot_name = "SECONDROBOT: "
    second_robot.duty_cycle_forward = 85
    second_robot.duty_cycle_direction = 60
    second_robot.game_interface_id = 2
    print("SECOND DONE")
    warm_up_count = 0
    while warm_up_count < 2:
        _, frame = cap.read()
        time.sleep(1)
        warm_up_count += 1

    while 1:
        # Take each frame
        _, frame = cap.read()

        color_detection.process_frame(frame, main_robot, second_robot)

        # Update heading for each robot
        main_robot.update_heading()
        second_robot.update_heading()

        # Check for collisions
        robot_collision_result = robot_collision_controller.are_robots_in_collision_course(main_robot, second_robot)
        if robot_collision_result != RobotCollisionIdentification.NO_ROBOT:
            if robot_collision_result.FIRST_ROBOT:
                print("Green/Blue robot on collision course. Stopping.")
                main_robot.is_on_collision_course = True
            else:
                print("Pink/Red robot on collision course. Stopping.")
                second_robot.is_on_collision_course = True
            print("Robots on collision course!")
        else:
            main_robot.is_on_collision_course = False
            second_robot.is_on_collision_course = False

        print("Putting in queue.")
        game_interface_position_list = GameInterfaceCarPositionList()
        main_robot_game_interface = GameInterfaceCarPosition()
        main_robot_game_interface.carId = main_robot.game_interface_id
        main_robot_game_interface.pos_x = main_robot.leading_point.x
        main_robot_game_interface.pos_y = main_robot.leading_point.y
        main_robot_game_interface.rotation = main_robot.get_heading_in_degrees()

        second_robot_game_interface = GameInterfaceCarPosition()
        second_robot_game_interface.carId = second_robot.game_interface_id
        second_robot_game_interface.pos_x = second_robot.leading_point.x
        second_robot_game_interface.pos_y = second_robot.leading_point.y
        second_robot_game_interface.rotation = second_robot.get_heading_in_degrees()

        game_interface_position_list.list_of_cars.append(main_robot_game_interface)
        game_interface_position_list.list_of_cars.append(second_robot_game_interface)

        await out_queue.put(game_interface_position_list.to_json().replace("'", "\""))

        main_robot.move_robot_to_next_position(command_controller, city_builder)

        second_robot.move_robot_to_next_position(command_controller, city_builder)

        k = cv2.waitKey(40) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


async def handler(websocket, path):
    while True:
        message = await out_queue.get()
        print("Received from WS queue.")
        await websocket.send(message)


asyncio.get_event_loop().run_until_complete(websockets.serve(handler, 'localhost', 8081))
asyncio.get_event_loop().run_until_complete(capture())
asyncio.get_event_loop().run_forever()
