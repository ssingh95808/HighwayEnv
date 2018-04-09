from __future__ import division, print_function

from highway_env.envs.abstract import AbstractEnv
from highway_env.road.road import Road
from highway_env.vehicle.behavior import IDMVehicle
from highway_env.vehicle.control import MDPVehicle


class HighwayEnv(AbstractEnv):
    metadata = {'render.modes': ['human']}

    COLLISION_COST = 10
    LANE_CHANGE_COST = 0.0
    RIGHT_LANE_REWARD = 0.5
    HIGH_VELOCITY_REWARD = 1.0

    def __init__(self):
        road = Road.create_random_road(lanes_count=4, lane_width=4.0, vehicles_count=20, vehicles_type=IDMVehicle)
        vehicle = MDPVehicle.create_random(road, 25)
        road.vehicles.append(vehicle)
        super(HighwayEnv, self).__init__(road, vehicle)

    def observation(self):
        return 1

    def reward(self, action):
        action_reward = {0: -self.LANE_CHANGE_COST, 1: 0, 2: -self.LANE_CHANGE_COST, 3: 0, 4: 0}
        state_reward = \
            - self.COLLISION_COST * self.vehicle.crashed \
            + self.RIGHT_LANE_REWARD * self.vehicle.lane_index \
            + self.HIGH_VELOCITY_REWARD * self.vehicle.speed_index()
        return action_reward[action] + state_reward

    def is_terminal(self):
        """
        :return: Whether the current state is a terminal state
        """
        return self.vehicle.crashed

    def reset(self):
        pass