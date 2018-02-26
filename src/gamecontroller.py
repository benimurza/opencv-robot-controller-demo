from enum import Enum
import logging

from maputils import MapPoint
from robot import RobotRole

logger = logging.getLogger("GameController")


class GameDifficulty(Enum):
    EASY = 0
    HARD = 1


class GameController:
    @staticmethod
    def select_robot_furthest_away(police_robot, robot_list):
        robber_robot = None
        max_distance = 0
        for robot in robot_list:
            if robot is not police_robot:
                distance_between_robots = MapPoint.calculate_distance_between_points(robot.leading_point,
                                                                                     police_robot.leading_point)
                if distance_between_robots > max_distance:
                    max_distance = distance_between_robots
                    robber_robot = robot

        return robber_robot

    @staticmethod
    def get_robber_street_name(robot_list):
        for robot in robot_list:
            if robot.role == RobotRole.ROBBER:
                return robot.current_street.street_name
        return None

    @staticmethod
    def select_robber(robot_list, game_difficulty):
        if game_difficulty != GameDifficulty.EASY:
            logger.error("Game difficulty " + str(game_difficulty) + " not implemented.")
            return
        if len(robot_list) < 2:
            logger.error("Cannot select robber, since robot list only contains one robot!")
        else:
            robber_robot = None
            police_robot = None
            # Retrieve police robot
            for robot in robot_list:
                if robot.role == RobotRole.POLICE:
                    police_robot = robot
                    break

            if game_difficulty == GameDifficulty.EASY:
                robber_robot = GameController.select_robot_furthest_away(police_robot, robot_list)

            if robber_robot is not None:
                logger.info("Robot " + robber_robot.robot_name + " was chosen as the new robber!")

                # Assign robber role to robot with the greatest distance
                robber_robot.role = RobotRole.ROBBER
            else:
                logger.warning("No robot could be selected as the new robber.")
