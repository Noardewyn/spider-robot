from abc import ABCMeta, abstractmethod


class ILeg:
    __metaclass__ = ABCMeta

    @abstractmethod
    def relax(self):
        """relax all leg joints"""

    @abstractmethod
    def move_instantly(self, x: float, y: float, z: float):
        """move leg to specified point in space instantly"""

    @abstractmethod
    def move_timed(self, x: float, y: float, z: float, time: float):
        """move leg to pointed dot in space for the specified time"""

