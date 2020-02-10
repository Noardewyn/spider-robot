from spider import Spider
from leg_3dof import Leg3DOF
from joint import Joint
from servo import Servo
from server import Server

import time

coxa_length = 2.8
femur_length = 5.5
tibia_length = 8


def build_joint(joint_id: id, reverse_direction: int):
    servo = Servo(joint_id, False)
    joint = Joint(servo, min_angle=0, max_angle=180, reverse_direction=reverse_direction, instant_move=False)
    return joint


def build_spider():

    joints = (build_joint(0, False), build_joint(1, False), build_joint(2, False))
    front_left_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(4, True), build_joint(5, True), build_joint(6, True))
    front_right_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(8, False), build_joint(9, True), build_joint(10, True))
    back_left_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(12, True), build_joint(13, False), build_joint(14, False))
    back_right_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    spider = Spider((front_left_leg, front_right_leg, back_left_leg, back_right_leg))

    return spider


def main():
    spider = build_spider()
    spider.prepare_to_walk()
    server = Server(spider, 8050)
    server.listen_loop()
    spider.relax()
    print("done")


if __name__ == "__main__":
    main()
