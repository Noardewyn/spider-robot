from spider import Spider
from leg_3dof import Leg3DOF
from joint import Joint
from test_servo import Servo

coxa_length = 1
femur_length = 4
tibia_length = 5


def build_joint(joint_id: id, reverse_direction: int):
    servo = Servo(joint_id, True)
    joint = Joint(servo, min_angle=0, max_angle=180, reverse_direction=reverse_direction)
    return joint


def build_spider():

    joints = (build_joint(0, True), build_joint(1, True), build_joint(2, True))
    front_left_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(4, False), build_joint(5, False), build_joint(6, False))
    front_right_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(8, True), build_joint(9, False), build_joint(10, False))
    back_left_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    joints = (build_joint(12, False), build_joint(13, True), build_joint(14, True))
    back_right_leg = Leg3DOF(coxa_length, femur_length, tibia_length, joints)

    spider = Spider((front_left_leg, front_right_leg, back_left_leg, back_right_leg))

    return spider


def main():
    spider = build_spider()
    # spider.get_leg(0).move_instantly(5, 5, 0)
    spider.get_leg(1).move_timed(5, 0, 0, 3)


if __name__ == "__main__":
    main()
