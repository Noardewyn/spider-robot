from iservo import IServo


class Joint:
    def __init__(self, servo: IServo, **kwargs):
        self._servo = servo
        self._angle = 0
        self._reverse_direction = False
        self.min_angle = 0
        self.max_angle = 180

        for key, value in kwargs.items():
            if key == "angle":
                self.angle = value
            if key == "reverse_direction":
                self.reverse_direction = value
            if key == "min_angle":
                self.min_angle = value
            if key == "max_angle":
                self.max_angle = value

    def set_angle(self, angle: int):
        if angle < self.min_angle or angle > self.max_angle:
            raise IndexError('Recieved: {0}, but angle must be in range: {1} - {2}'.format(angle, self.min_angle, self.max_angle))

        if self.reverse_direction:
            angle = 180 - angle

        self._servo.move(angle)
        self._angle = angle

    def get_angle(self):
        return self._angle

    def relax(self):
        self._servo.relax()
