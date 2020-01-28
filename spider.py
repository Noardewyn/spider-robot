from ileg import ILeg
from typing import Tuple
import time
import numpy


def delay(t):
    time.sleep(t)


class Spider:
    def __init__(self, legs: Tuple[ILeg, ILeg, ILeg, ILeg]):
        self.legs = legs

    def relax(self):
        for leg in self.legs:
            leg.relax()

    def get_leg(self, index: int) -> ILeg:
        return self.legs[index]

    def move_legs(self):
        self.get_leg(0).move_joints()
        self.get_leg(1).move_joints()
        self.get_leg(2).move_joints()
        self.get_leg(3).move_joints()

    def stand_pose(self, x_distance: float = 2.5, y_distance: float = 2.5, height=-4):

        self.get_leg(0).set_xyz_position(-x_distance, y_distance, height)
        self.get_leg(1).set_xyz_position(x_distance, y_distance, height)
        self.get_leg(2).set_xyz_position(-x_distance, -y_distance, height)
        self.get_leg(3).set_xyz_position(x_distance, -y_distance, height)
        self.move_legs()

    def up_down_animation(self, delay, step):
        for height in numpy.arange(-6, -3, step):
            self.stand_pose(3, height)
            time.sleep(delay)

        for height in numpy.arange(-3, -6, -step):
            self.stand_pose(3, height)
            time.sleep(delay)

    def shift(self, x_offset: float, y_offset: float, z_offset: float):

        self.get_leg(0).shift(x_offset, y_offset, z_offset)
        self.get_leg(1).shift(x_offset, y_offset, z_offset)
        self.get_leg(2).shift(x_offset, y_offset, z_offset)
        self.get_leg(3).shift(x_offset, y_offset, z_offset)
        self.move_legs()

    def creep_walk(self):

        step_distance_factor = 0.5

        delay_between_steps = 0.8
        down_height = -7
        up_height = -5

        step_delay = 0.1
        stand_leg_distance_x = 4 #3
        stand_leg_distance_y = 4 * step_distance_factor #2
        shift_distance_y = -4 * step_distance_factor

        small_step_distance_y = 3 * step_distance_factor #1
        long_step_distance_y = 11 * step_distance_factor #4

        self.stand_pose(stand_leg_distance_x, stand_leg_distance_y, down_height)

        delay(1)

        self.get_leg(3).step(stand_leg_distance_x, small_step_distance_y, down_height, up_height, step_delay)
        delay(delay_between_steps)

        self.get_leg(1).step(stand_leg_distance_x, long_step_distance_y, down_height, up_height, step_delay)
        delay(delay_between_steps)

        # self.get_leg(0).set_xyz_position(-stand_leg_distance_x, -small_step_distance_y, down_height)
        # self.get_leg(1).set_xyz_position(stand_leg_distance_x,  stand_leg_distance_y, down_height)
        # self.get_leg(2).set_xyz_position(-stand_leg_distance_x, -long_step_distance_y, down_height)
        # self.get_leg(3).set_xyz_position(stand_leg_distance_x, -stand_leg_distance_y, down_height)
        # self.move_legs()

        self.shift(0, shift_distance_y, 0)

        delay(delay_between_steps)

        self.get_leg(2).step(-stand_leg_distance_x, small_step_distance_y, down_height, up_height, step_delay)
        delay(delay_between_steps)

        self.get_leg(0).step(-stand_leg_distance_x, long_step_distance_y, down_height, up_height, step_delay)
        delay(delay_between_steps)

        # self.get_leg(0).set_xyz_position(-stand_leg_distance_x, stand_leg_distance_x, down_height)
        # self.get_leg(1).set_xyz_position(stand_leg_distance_x,  -small_step_distance_y, down_height)
        # self.get_leg(2).set_xyz_position(-stand_leg_distance_x, -stand_leg_distance_x, down_height)
        # self.get_leg(3).set_xyz_position(stand_leg_distance_x, -long_step_distance_y, down_height)
        # self.move_legs()
        self.shift(0, shift_distance_y, 0)

        delay(delay_between_steps)