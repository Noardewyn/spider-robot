from spider import Spider
from leg_3dof import Leg3DOF
from joint import Joint
from servo import Servo
import time

coxa_length = 1
femur_length = 4
tibia_length = 6.1


def build_joint(joint_id: id, reverse_direction: int):
    servo = Servo(joint_id, True)
    joint = Joint(servo, min_angle=0, max_angle=180, reverse_direction=reverse_direction)
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
    spider.stand_pose()
    time.sleep(1)
    spider.get_leg(1).move_instantly(2, 6, -4)
    time.sleep(1)
    spider.relax()


if __name__ == "__main__":
    main()
