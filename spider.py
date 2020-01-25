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

    def move_joints(self):
        self.get_leg(0).move_joints()
        self.get_leg(1).move_joints()
        self.get_leg(2).move_joints()
        self.get_leg(3).move_joints()

    def stand_pose(self, distance=2.5, height=-4):

        self.get_leg(0).set_xyz_position(-distance, distance, height)
        self.get_leg(1).set_xyz_position(distance, distance, height)
        self.get_leg(2).set_xyz_position(-distance, -distance, height)
        self.get_leg(3).set_xyz_position(distance, -distance, height)
        self.move_joints()

    def up_down_animation(self, delay, step):
        for height in numpy.arange(-6, -3, step):
            self.stand_pose(3, height)
            time.sleep(delay)

        for height in numpy.arange(-3, -6, -step):
            self.stand_pose(3, height)
            time.sleep(delay)

    def walk(self):
        step_delay = 1
        down_height = -7
        val_a = 3
        val_b = 3
        val_c = 0.5
        val_d = 6

        self.get_leg(3).step(val_a, 1, down_height)
        delay(step_delay)

        self.get_leg(1).step(val_a, val_d, down_height)
        delay(step_delay)

        self.get_leg(0).set_xyz_position(-val_a, val_c, down_height)
        self.get_leg(1).set_xyz_position(val_b,  val_b, down_height)
        self.get_leg(2).set_xyz_position(val_a, -val_d, down_height)
        self.get_leg(3).set_xyz_position(val_b, -val_b, down_height)
        self.move_joints()

        delay(1)

        self.get_leg(2).step(-val_a, -val_c, down_height)
        delay(step_delay)

        self.get_leg(0).step(-val_a, val_d, down_height)
        delay(step_delay)

        self.get_leg(0).set_xyz_position(-val_a, val_b, down_height)
        self.get_leg(1).set_xyz_position(val_a,  val_c, down_height)
        self.get_leg(2).set_xyz_position(-val_a, -val_b, down_height)
        self.get_leg(3).set_xyz_position(val_a, -val_d, down_height)
        self.move_joints()

        delay(1)