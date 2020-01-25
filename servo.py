from iservo import IServo
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo


class Servo(IServo):
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
    max_pulse = 500
    min_pulse = 2600

    def __init__(self, servo_id: int, debug_log: bool = False):
        self._servo_id = servo_id
        self._angle = 0
        self._debug_log = debug_log
        self._driver = servo.Servo(Servo.pca.channels[self._servo_id], min_pulse=Servo.min_pulse, max_pulse=Servo.max_pulse)

    def move(self, angle: int):
        self._angle = angle
        self._driver.angle = angle
        if self._debug_log:
            print('servo [{0}] moved to {1}'.format(self._servo_id, self._angle))

    def get_angle(self):
        return self._angle

    def relax(self):
        self._driver.angle = None
        if self._debug_log:
            print('servo [{0}] relaxed'.format(self._servo_id))
