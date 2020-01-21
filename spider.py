from ileg import ILeg
from typing import Tuple


class Spider:
    def __init__(self, legs: Tuple[ILeg, ILeg, ILeg, ILeg]):
        self.legs = legs

    def relax(self):
        for leg in self.legs:
            leg.relax()

    def get_leg(self, index: int) -> ILeg:
        return self.legs[index]

    def stand_pose(self):
        distance = 2.5
        height = -4
        self.get_leg(0).move_instantly(-distance, distance, height)
        self.get_leg(1).move_instantly(distance, distance, height)
        self.get_leg(2).move_instantly(-distance, -distance, height)
        self.get_leg(3).move_instantly(distance, -distance, height)
        pass

    def up_down_animation(self):
        pass
