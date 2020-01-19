from ileg import ILeg
from joint import Joint
import math
import time
from typing import Tuple
import threading
from tkinter import *

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
        self.position = [0.0, 0.0, 0.0]
        self.joints = joints
        self.__angle_changed
        self.__change_handler_thread = threading.Thread(target=change_handler, daemon=True)

    def change_handler(self):
        condition.acquire()
        condition.wait()
        condition.release()

    def relax(self):
        for joint in self.joints:
            joint.relax()

    def __get_joint_angle(self, index: int) -> int:
        return self.joints[index].get_angle()

    def __set_joint_angle(self, index: int, angle: int):
        self.joints[index].set_angle(angle)

    def __set_joints_angles(self, a: int, b: int, c: int):
        if a is not None:
            self.joints[0].set_angle(a)
        if b is not None:
            self.joints[1].set_angle(b)
        if c is not None:
            self.joints[2].set_angle(c)

    def move_instantly(self, x: float, y: float, z: float):
        next_angles = [0, 0, 0]

        hypotenuse = math.sqrt(x ** 2 + abs(y) ** 2)
        # print(hypotenuse)

        if y != 0:
            atan_a = math.atan(abs(x) / abs(y))
            next_angles[0] = math.degrees(atan_a)
        else:
            next_angles[0] = 90

        # print("next_angles[0]1 " + str(next_angles[0]))
        next_angles[0] = 180 - next_angles[0] if y > 0 else next_angles[0]

        # print("next_angles[0]2 " + str(next_angles[0]))

        cos_b = (hypotenuse ** 2 + self.femur_length ** 2 - self.tibia_length ** 2) / (2 * hypotenuse * self.femur_length)
        cos_c = (self.femur_length ** 2 + self.tibia_length ** 2 - hypotenuse ** 2) / (2 * self.tibia_length * self.femur_length)

        next_angles[1] = abs(math.degrees(math.acos(cos_b)))
        next_angles[2] = abs(math.degrees(math.acos(cos_c)))

        # print("next_angles[1] " + str(next_angles[1]))
        # print("next_angles[2] " + str(next_angles[2]))

        height_offset_angle = 90 - math.degrees(math.acos(z / hypotenuse))
        # print("height_offset_angle " + str(height_offset_angle))

        next_angles[1] = 90 - next_angles[1] + height_offset_angle
        next_angles[2] = next_angles[2]

        # print("next_angles[1] " + str(next_angles[1]))
        # print("next_angles[2] " + str(next_angles[2]))

        self.__set_joints_angles(next_angles[0], next_angles[1], next_angles[2])

    def move_joint_timed(self, joint_index: int, angle: int, time_to_rotate: float):
        current_angle = self.__get_joint_angle(joint_index)
        delta = abs(current_angle - angle)

        if delta == 0:
            # time.sleep(time_to_rotate)
            return

        delay = time_to_rotate / delta
        step = 1 if angle - current_angle > 0 else -1

        for a in range(delta):
            time.sleep(delay)
            self.__set_joint_angle(joint_index, self.__get_joint_angle(joint_index) + step)

    def move_timed(self, x: float, y: float, z: float, time_to_rotate: float):
        self.move_joint_timed(0, 3, time_to_rotate)
