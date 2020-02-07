from ileg import ILeg
from joint import Joint
import math
import time
from typing import Tuple
import numpy
from operator import sub

class Leg3DOF(ILeg):
    '''
    Representation of single spider leg with three joints
    https://www.google.com/search?client=ubuntu&hs=TAo&biw=1920&bih=953&tbm=isch&sxsrf=ACYBGNTBqmOR50pyd6AqIGbJW0ny0ahEvg%3A1579341537194&sa=1&ei=4dYiXoSjC6v6qwH64prYAQ&q=spider+leg+movement&oq=&gs_l=img.3.2.35i362i39l10.24499.25259..31384...1.0..3.109.1089.10j2......0....1..gws-wiz-img.....10..35i39.6N-3bXDmOSM#imgrc=CjodMRpvTyFDRM:

    Args:
        coxa_length (float): length first joint to second joint
        femur_length (float): length from second to third joint
        tibia_length (float): length from third joint to the end of the leg

    Attributes:
        coxa_length (float): length first joint to second joint
        femur_length (float): length from second to third joint
        tibia_length (float): length from third joint to the end of the leg

    '''
    def __init__(self, coxa_length: float, femur_length: float, tibia_length: float,
                 joints: Tuple[Joint, Joint, Joint]):
        assert joints.count != 3

        self.coxa_length = coxa_length
        self.femur_length = femur_length
        self.tibia_length = tibia_length
        self._joints = joints
        self._actual_position = [0, 0, 0]
        self._next_position = [0, 0, 0]

    def relax(self):
        for joint in self._joints:
            joint.relax()

    def get_joint_angle(self, index: int) -> int:
        return self._joints[index].get_angle()

    def set_joint_angle(self, index: int, angle: int):
        self._joints[index].set_angle(angle)

    def get_actual_position(self):
        return self._actual_position

    def get_next_position(self):
        return self._next_position

    def __set_next_position(self, x: float, y: float, z: float):
        self._next_position = (x, y, z)

    def __set_actual_position(self, x: float, y: float, z: float):
        self._actual_position = (x, y, z)

    def move_joints(self):
        [joint.move() for joint in self._joints]
        self._actual_position = self._next_position

    def shift(self, x_offset: float, y_offset: float, z_offset: float):
        current_position = self.get_actual_position()
        print("current_pos: ", current_position)
        print("next_pos: ", self.get_next_position())
        print(x_offset, y_offset, z_offset)

        self.set_xyz_position(current_position[0] + x_offset, current_position[1] + y_offset, current_position[2] + z_offset)

        print("after_shift_pos: ", self.get_next_position())

    def __set_joints_angles(self, a: int, b: int, c: int):
        if a is not None:
            self._joints[0].set_angle(a)
        if b is not None:
            self._joints[1].set_angle(b)
        if c is not None:
            self._joints[2].set_angle(c)

    def step(self, x: float, y: float, down_height: float, up_height: float = 0, delay: float = 0.4):
        self.move_to_xyz_instantly(x, y, up_height)
        time.sleep(delay)
        self.move_to_xyz_instantly(x, y, down_height)

    def calculate_xyz_position(self, x: float, y: float, z: float):
        result_angles = [0, 0, 0]

        distance = 0

        if x != 0 and y != 0:
            distance = math.sqrt(abs(x) ** 2 + abs(y) ** 2)
        else:
            distance = abs(x) + abs(y)

        if y != 0:
            atan_a = math.atan(abs(x) / abs(y))
            result_angles[0] = math.degrees(atan_a)
        else:
            result_angles[0] = 90

        result_angles[0] = 180 - result_angles[0] if y > 0 else result_angles[0]

        if z == 0:
            cos_b = (distance ** 2 + self.femur_length ** 2 - self.tibia_length ** 2) / (
                    2 * distance * self.femur_length)
            cos_c = (self.femur_length ** 2 + self.tibia_length ** 2 - distance ** 2) / (
                    2 * self.tibia_length * self.femur_length)

            if math.degrees(math.acos(cos_b)) <= 90:
                result_angles[1] = 90 - math.degrees(math.acos(cos_b))
            else:
                result_angles[1] = math.degrees(math.acos(cos_b)) - 90

            result_angles[2] = math.degrees(math.acos(cos_c))
            # print("z==0", result_angles)

        else:
            hypotenuse = math.sqrt(abs(distance) ** 2 + abs(z) ** 2)
            cos_b = (hypotenuse ** 2 + self.femur_length ** 2 - self.tibia_length ** 2) / (
                    2 * hypotenuse * self.femur_length)
            cos_c = (self.femur_length ** 2 + self.tibia_length ** 2 - hypotenuse ** 2) / (
                    2 * self.tibia_length * self.femur_length)

            if z > 0:
                cos_d = distance / hypotenuse

                if (math.degrees(math.acos(cos_b)) + math.degrees(math.acos(cos_d))) <= 90:
                    result_angles[1] = 90 - (math.degrees(math.acos(cos_b)) + math.degrees(math.acos(cos_d)))
                else:
                    result_angles[1] = (math.degrees(math.acos(cos_b)) + math.degrees(math.acos(cos_d))) - 90

            else:
                cos_d = abs(z) / hypotenuse
                result_angles[1] = 180 - (math.degrees(math.acos(cos_b)) + math.degrees(math.acos(cos_d)))

            result_angles[2] = math.degrees(math.acos(cos_c))

            # print(result_angles)

        return result_angles

    def set_xyz_position(self, x: float, y: float, z: float):
        next_angles = self.calculate_xyz_position(x, y, z)
        self.__set_joints_angles(next_angles[0], next_angles[1], next_angles[2])
        self.__set_next_position(x, y, z)

    def move_to_xyz_instantly(self, x: float, y: float, z: float):
        self.set_xyz_position(x, y, z)
        self.move_joints()
        self.__set_actual_position(x, y, z)

    def move_to_xyz_timed(self, x: float, y: float, z: float, time_to_rotate: float):
        current_angles = [joint.get_angle() for joint in self._joints]
        next_angles = self.calculate_xyz_position(x, y, z)
        joints_deltas = list(map(sub, current_angles, next_angles))

        while [int(a) for a in current_angles] != [int(a) for a in next_angles]:
            delay = time_to_rotate / abs(max(joints_deltas))
            time.sleep(delay)

            for i in range(3):
                step_direction = joints_deltas[i] / abs(joints_deltas[i] if joints_deltas[i] != 0 else 1)
                if int(current_angles[i]) != int(next_angles[i]):
                    next_angles[i] += step_direction
                    self._joints[i].set_angle(next_angles[i])
                    self._joints[i].move()

