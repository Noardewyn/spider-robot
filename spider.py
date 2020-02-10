from ileg import ILeg
from typing import Tuple
import time
import numpy


def delay(t):
    time.sleep(t)


class Spider:
    def __init__(self, legs: Tuple[ILeg, ILeg, ILeg, ILeg], z_position=0):
        self.legs = legs
        self.z_position = z_position
        self._current_side = 0
        self._legs_wide_x = 4
        self._legs_wide_y = 2
        self._legs_narrowly_x = 4
        self._legs_narrowly_y = -0.5
        self._legs_rotate_x = 0.5
        self._legs_rotate_y = 2
        self._shift_size = self._legs_wide_y + abs(self._legs_narrowly_y)
        self._down_heigth = -9
        self._up_height = -5
        self.delay_between_steps = 0.3
        self.step_delay = 0.15

    def assembly_leg_init(self):
        for i in range(4):
            for j in range(3):
                self.get_leg(i).set_joint_angle(j, 90)
            self.get_leg(i).move_joints()

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

    def stand_pose(self, x_distance: float = 4, y_distance: float = 4, height=-4):
        self.z_position = height
        self.get_leg(0).set_xyz_position(-x_distance, y_distance, height)
        self.get_leg(1).set_xyz_position(x_distance, y_distance, height)
        self.get_leg(2).set_xyz_position(-x_distance, -y_distance, height)
        self.get_leg(3).set_xyz_position(x_distance, -y_distance, height)
        self.move_legs()

    def lift_to(self, new_z_position: float, x_distance: float, delay_time: float, step: float):
        step = -step if self.z_position > new_z_position else step
        for height in numpy.arange(self.z_position, new_z_position,  step):
            self.stand_pose(x_distance, x_distance, height)
            time.sleep(delay_time)

    def up_down_animation(self, delay_time: float, step: float):
        self.lift_to(-7, delay_time, step)
        self.lift_to(-3, delay_time, step)

    def shift(self, x_offset: float, y_offset: float, z_offset: float):

        self.get_leg(0).shift( x_offset,  y_offset, z_offset)
        self.get_leg(1).shift( x_offset,  y_offset, z_offset)
        self.get_leg(2).shift(-x_offset,  y_offset, z_offset)
        self.get_leg(3).shift(-x_offset,  y_offset, z_offset)
        self.move_legs()

    def __change_wide_side(self):
        if self._current_side == 0:
            self._current_side = 1
        elif self._current_side == 1:
            self._current_side = 0

    def prepare_to_walk(self):
        if self._current_side == 0:
            self.get_leg(0).set_xyz_position(-self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.get_leg(1).set_xyz_position(self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(-self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth)
        elif self._current_side == 1:
            self.get_leg(0).set_xyz_position(-self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth)
            self.get_leg(1).set_xyz_position(self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(-self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(self._legs_wide_x, -self._legs_wide_y, self._down_heigth)

        self.move_legs()

    def move_forward(self):
        if self._current_side == 0:
            self.get_leg(1).step(self._legs_wide_x, self._legs_wide_y + self._shift_size, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

            self.shift(0, -self._shift_size, 0)
            delay(self.delay_between_steps)

            self.get_leg(2).step(-self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        elif self._current_side == 1:
            self.get_leg(0).step(-self._legs_wide_x, self._legs_wide_y + self._shift_size, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

            self.shift(0, -self._shift_size, 0)
            delay(self.delay_between_steps)

            self.get_leg(3).step(self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        self.__change_wide_side()

    def move_backward(self):
        if self._current_side == 0:

            self.get_leg(3).step(self._legs_wide_x, -(self._legs_wide_y + self._shift_size), self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

            self.shift(0, self._shift_size, 0)
            delay(self.delay_between_steps)

            self.get_leg(0).step(-self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        elif self._current_side == 1:
            self.get_leg(2).step(-self._legs_wide_x, -(self._legs_wide_y + self._shift_size), self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

            self.shift(0, self._shift_size, 0)
            delay(self.delay_between_steps)

            self.get_leg(1).step(self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        self.__change_wide_side()

    def turn_left(self):

        if self._current_side == 0:
            self.get_leg(1).move_to_xyz_instantly(self._legs_wide_x, self._legs_wide_y, self._up_height)
            delay(self.delay_between_steps)

            self.get_leg(0).set_xyz_position(self._legs_rotate_x, self._legs_rotate_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(-self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            self.get_leg(1).set_xyz_position(self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.move_legs()

            # self.get_leg(1).move_to_xyz_instantly(self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            delay(self.delay_between_steps)

            self.get_leg(0).step(-self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        elif self._current_side == 1:
            self.get_leg(2).move_to_xyz_instantly(-self._legs_wide_x, -self._legs_wide_y, self._up_height)
            delay(self.delay_between_steps)

            self.get_leg(0).set_xyz_position(-self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.get_leg(1).set_xyz_position(self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(-self._legs_rotate_x, -self._legs_rotate_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(-self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            self.move_legs()

            # self.get_leg(2).move_to_xyz_instantly(-self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            delay(self.delay_between_steps)

            self.get_leg(3).step(self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        self.__change_wide_side()

    def turn_right(self):
        if self._current_side == 0:
            self.get_leg(3).move_to_xyz_instantly(self._legs_wide_x, -self._legs_wide_y, self._up_height)
            delay(self.delay_between_steps)

            self.get_leg(0).set_xyz_position(-self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth)
            self.get_leg(1).set_xyz_position(self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(self._legs_rotate_x, -self._legs_rotate_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            self.move_legs()

            # self.get_leg(3).move_to_xyz_instantly(self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            delay(self.delay_between_steps)

            self.get_leg(2).step(-self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        elif self._current_side == 1:
            self.get_leg(0).move_to_xyz_instantly(-self._legs_wide_x, self._legs_wide_y, self._up_height)
            delay(self.delay_between_steps)

            self.get_leg(1).set_xyz_position(-self._legs_rotate_x, self._legs_rotate_y, self._down_heigth)
            self.get_leg(2).set_xyz_position(-self._legs_wide_x, -self._legs_wide_y, self._down_heigth)
            self.get_leg(3).set_xyz_position(self._legs_narrowly_x, -self._legs_narrowly_y, self._down_heigth)
            self.get_leg(0).set_xyz_position(-self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            self.move_legs()

            # self.get_leg(0).move_to_xyz_instantly(-self._legs_wide_x, self._legs_wide_y, self._down_heigth)
            delay(self.delay_between_steps)

            self.get_leg(1).step(self._legs_narrowly_x, self._legs_narrowly_y, self._down_heigth, self._up_height, self.step_delay)
            delay(self.delay_between_steps)

        self.__change_wide_side()
