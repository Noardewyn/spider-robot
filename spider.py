from ileg import ILeg
from typing import Tuple


class Spider:
    def __init__(self, legs: Tuple[ILeg, ILeg, ILeg, ILeg]):
        self.legs = legs

    def get_leg(self, index: int) -> ILeg:
        return self.legs[index]

    def stand_pose(self):
        pass

    def up_down_animation(self):
        pass
