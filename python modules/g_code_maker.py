import operator
from enum import Enum
import subprocess
import serial
from time import sleep


class Direction(Enum):
    X = 0,
    Y = 1

class g_sender:
    def __init__(self, port, station_coaards):
        self.curr_loc = (0,0)
        self.port = port
        self.station_coaards = station_coaards
        self.serial = serial.Serial(port,115200)
        self.homing()

    def homing(self):
        self.move_servo_up_without_piece()
        self.move_robot_absolute((10, 0))
        sleep(0.5)
        self.serial.close()
        self.serial.open()
        self.move_servo_up_without_piece()
        self.move_robot_absolute((0, 10))
        sleep(0.5)
        self.serial.close()
        self.serial.open()


    def get_curr_loc(self):
        return self.curr_loc

    def set_curr_loc(self, new_loc):
        self.curr_loc = new_loc

    def move_robot_to_station(self):
        self.move_robot_realtive(self.station_coaards, 22)

    def move_piece_to_station_and_wait(self, step_size, cur_round):
        self.move_piece_flow(self.station_coaards, step_size, cur_round)
        sleep(0.1)
        self.move_robot_realtive((10,0), step_size)

    def move_piece_to_station(self):
        self.move_robot_realtive(self.station_coaards, 22)

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

    def move_servo_up_without_piece(self):
        g_cmd = ["M03 S20\n"]
        self.send_g_code_to_arduino(self.port, g_cmd, 5)
        g_cmd = ["M03 S40\n"]
        self.send_g_code_to_arduino(self.port, g_cmd, 1)

    def move_servo_up_with_piece(self):
        g_cmd = ["M03 S40\n"]
        self.send_g_code_to_arduino(self.port, g_cmd, 1)

    def move_servo_down(self):
        g_cmd = ["M03 S5\n"]
        self.send_g_code_to_arduino(self.port, g_cmd)


    def read_serial(self):
        return self.serial.readline()

    def home(self):
        g_cmds = ["$22 = 1\n","$H\n"]
        self.send_g_code_to_arduino(self.port, g_cmds)




    def move_piece_flow(self, new_coaards, step_size, cur_round):
        self.move_servo_down()
        #self.send_g_code_to_arduino(self.port, ["?\n"])
        self.activate_pump()
        self.move_servo_up_with_piece()
        if 11 < cur_round < 16:
            self.move_robot_realtive((7, 3), 22)
        #self.send_g_code_to_arduino(self.port, ["?\n"])
        self.move_robot_realtive(new_coaards, step_size)
        self.send_g_code_to_arduino(self.port, ["?\n"], 20)
        self.move_servo_down()
        self.deactivate_pump()
        #self.send_g_code_to_arduino(self.port, ["?\n"], 20)
        self.move_servo_up_without_piece()



    def move_robot_realtive(self, new_loc, step_size):
        #print("Moving robot to %s" % new_loc )
        steps = tuple(map(operator.sub, new_loc, self.curr_loc))
        next_position = (self.curr_loc[0] + steps[0]*step_size, self.curr_loc[1] + steps[1]*step_size)
        g_cmds = [self.generate_g_cmd(steps, step_size), "G90 G21"]
        self.send_g_code_to_arduino(self.port, g_cmds)
        #while next_position != self.curr_loc:
        #    sleep(0.5)
        self.set_curr_loc(new_loc)
        print("Moved!!!")

    def move_robot_absolute(self, new_absolute_loc):
        next_position = (new_absolute_loc[0], new_absolute_loc[1])
        g_cmds = [self.generate_g_cmd(next_position, 1), "G90 G21"]
        self.send_g_code_to_arduino(self.port, g_cmds)
        pass

    def generate_g_cmd(self, steps, step_size):
        ret_string = "G21G91G1"
        ret_string += "X" + str(steps[0]*step_size)
        ret_string += "Y" + str(steps[1] * step_size)
        ret_string += "F4000\n"
        return ret_string


    def removeComment(string):
        if (string.find(';') == -1):
            return string
        else:
            return string[:string.index(';')]


    def send_g_code_to_arduino(self, port, g_cmds, num_of_m400 = 5):
        # Open serial port

        # Wake up
        self.serial.write(bytes("\r\n\r\n", encoding='utf8'))  # Hit enter a few times to wake the Printrbot
        sleep(2)  # Wait for Printrbot to initialize
        self.serial.flushInput()  # Flush startup text in serial input

        # Stream g-code
        for cmd in g_cmds:
            self.serial.write((bytes(cmd, encoding='utf8')))  # Send g-code block
            for i in range(num_of_m400):
                self.serial.write((bytes("M400\n", encoding='utf8')))
           # my_str = self.serial.readline()
            #print(my_str)
           # other_Str = bytes('ok\r\n',encoding='utf8')
            #while my_str != other_Str:
             #   sleep(0.5)
              #  my_str = self.serial.readline()








