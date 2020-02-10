from spider import Spider

import socket
import json
import time
from enum import Enum
import threading


class RobotCommand(Enum):
    Stop = 0,
    MoveForward = 1,
    MoveBackward = 2,
    TurnLeft = 3,
    TurnRight = 4,
    MoveLeft = 5,
    MoveRight = 6,
    Relax = 7


robot_state_str = {
                    RobotCommand.Stop: "stop",
                    RobotCommand.MoveForward: "forward",
                    RobotCommand.MoveBackward: "backward",
                    RobotCommand.TurnLeft: "turn_left",
                    RobotCommand.TurnRight: "turn_right",
                    RobotCommand.MoveLeft: "move_left",
                    RobotCommand.MoveRight: "move_right",
                    RobotCommand.Relax: "relax",
                  }


def str_to_command(command: str):
    for robot_command, str_command in robot_state_str.items():
        if str_command == command:
            return robot_command


class Server:
    def __init__(self, spider: Spider, port: int):
        self._sock = socket.socket()
        self._sock.bind(('', port))
        self._performing_worker = threading.Thread(target=self.__commands_perform_loop, daemon=True)
        self._lock = threading.Lock()
        self._spider = spider
        self._current_message = {}
        self._next_message = {}
        self._end = False

    def listen_loop(self):
        self._performing_worker.start()
        self._sock.listen(1)

        while not self._end:
            conn, addr = self._sock.accept()

            with conn:
                print('Connected by', addr)
                while conn:
                    message = conn.recv(2048)
                    if message:
                        print('Received: ', message)
                        self.__queue_message(self. __encode_message(message))
                    time.sleep(0.1)

            print("connection closed")

    def __queue_message(self, message: dict):
        with self._lock:
            self._next_message = message

    def __dequeue_message(self):
        with self._lock:
            message = self._next_message
            self._next_message = None
            return message

    def __is_next_message(self) -> bool:
        return self._next_message is not None

    def __commands_perform_loop(self):
        while not self._end:
            message = self.__dequeue_message()

            if message:
                self.__perform_command(message)
            else:
                time.sleep(0.1)

    def __encode_message(self, message: bytes) -> dict:
        return json.loads(message)

    def __perform_command(self, message: dict):
        self._current_message = message

        command = str_to_command(message["command"])

        print("command", message["command"])
        print(command)
        if command == RobotCommand.MoveForward:
            if message["args"]["endless"]:
                while not self.__is_next_message():
                    self._spider.move_forward()
            else:
                self._spider.move_forward()
        elif command == RobotCommand.MoveBackward:
            if message["args"]["endless"]:
                while not self.__is_next_message():
                    self._spider.move_backward()
            else:
                self._spider.move_backward()
        elif command == RobotCommand.TurnLeft:
            if message["args"]["endless"]:
                while not self.__is_next_message():
                    self._spider.turn_left()
            else:
                self._spider.turn_left()
        elif command == RobotCommand.TurnRight:
            if message["args"]["endless"]:
                while not self.__is_next_message():
                    self._spider.turn_right()
            else:
                self._spider.turn_right()
        elif command == RobotCommand.Relax:
            self._spider.relax()
        elif command == RobotCommand.Stop:
            pass

        self._current_message = None
