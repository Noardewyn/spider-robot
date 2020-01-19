from abc import ABCMeta, abstractmethod


class IServo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self, angle: int):
        """Move servo with specified id(e.g. gpio) to angle"""

    @abstractmethod
    def relax(self):
        """power off servo"""
