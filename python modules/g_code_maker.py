import operator
from enum import Enum
import subprocess
import serial
from time import sleep


class Direction(Enum):
    X = 0,
    Y = 1

class g_sender:
    def __init__(self, curr_loc, port):
        self.curr_loc = curr_loc
        self.port = port
        self.serial = serial.Serial(port,115200)

    def get_curr_loc(self):
        return self.curr_loc

    def set_curr_loc(self, new_loc):
        self.curr_loc = new_loc


    def activate_pump(self):
        g_cmd = ["M08\n"]
        self.send_g_code_to_arduino(self.port, g_cmd)


    def deactivate_pump(self):
        g_cmd = ["M09\n"]
        self.send_g_code_to_arduino(self.port, g_cmd)

    def set_zero_coaardinates(self):
        g_cmd = ["G10 P0 L20 X0 Y0 Z0"]
        self.send_g_code_to_arduino(self.port, g_cmd)

    def reset_to_zero(self):
        g_cmds = ["G21G90 G0Z5", "G90 G0 X0 Y0", "G90 G0 Z0"]
        self.send_g_code_to_arduino(self.port, g_cmds)

    def move_servo_up(self):
        g_cmd = ["M03 S30\n"]
        self.send_g_code_to_arduino(self.port, g_cmd)

    def move_servo_down(self):
        g_cmd = ["M03 S00\n"]
        self.send_g_code_to_arduino(self.port, g_cmd)




    def move_robot_realtive(self, new_loc, step_size):
        steps = tuple(map(operator.sub, new_loc, self.curr_loc))
        g_cmds = [self.generate_g_cmd(steps, step_size), "G90 G21"]
        self.send_g_code_to_arduino(self.port, g_cmds)
        self.set_curr_loc(new_loc)

    def move_robot_absolute(self, new_absolute_loc):
        pass

    def generate_g_cmd(self, steps, step_size):
        ret_string = "G21G91G1"
        ret_string += "X" + str(steps[0]*step_size)
        ret_string += "Y" + str(steps[1] * step_size)
        ret_string += "F2000\n"
        return ret_string


    def removeComment(string):
        if (string.find(';') == -1):
            return string
        else:
            return string[:string.index(';')]


    def send_g_code_to_arduino(self, port, g_cmds):
        # Open serial port

        # Wake up
        self.serial.write(bytes("\r\n\r\n", encoding='utf8'))  # Hit enter a few times to wake the Printrbot
        sleep(2)  # Wait for Printrbot to initialize
        self.serial.flushInput()  # Flush startup text in serial input

        # Stream g-code
        for cmd in g_cmds:
            self.serial.write((bytes(cmd, encoding='utf8')))  # Send g-code block









