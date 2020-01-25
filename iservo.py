from abc import ABCMeta, abstractmethod


class IServo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self, angle: int):
        """Move servo with specified id(e.g. gpio) to angle"""

    def get_angle(self):
        """return current servo angle"""

    @abstractmethod
    def relax(self):
        """power off servo"""
