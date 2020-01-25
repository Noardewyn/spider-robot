from abc import ABCMeta, abstractmethod


class ILeg:
    __metaclass__ = ABCMeta

    @abstractmethod
    def relax(self):
        """relax all leg joints"""

    @abstractmethod
    def move_joints(self):
        """move joint to to a previously established position"""

    @abstractmethod
    def set_xyz_position(self, x: float, y: float, z: float):
        """set new leg position in xyz coords"""

    @abstractmethod
    def move_to_xyz_instantly(self, x: float, y: float, z: float):
        """move leg to specified point in space instantly"""

    @abstractmethod
    def move_to_xyz_timed(self, x: float, y: float, z: float, time_to_rotate: float):
        """move leg to pointed dot in space for the specified time"""

    @abstractmethod
    def step(self, x, y, down_height, delay=0.2):
        """up leg then down to specified point"""
