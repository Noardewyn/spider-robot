from iservo import IServo

class Servo(IServo):
    '''Test implementation of servo'''

    def __init__(self, servo_id: int, debug_log: bool = False):
        self._servo_id = servo_id
        self._angle = 0
        self._debug_log = debug_log

    def move(self, angle: int):
        self._angle = angle

        if self._debug_log:
            print('servo [{0}] moved to {1}'.format(self._servo_id, self._angle))

    def relax(self):
        if self._debug_log:
            print('servo [{0}] relaxed'.format(self._servo_id))
