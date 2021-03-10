from time import sleep
import serial
import g_code_maker
import camera
import cv2
import web_controller
from robot import Robot
import random
import utils

# global vars which might be determined by input later
num_of_pieces = 24
puzzle_num = 1

if __name__ == "__main__":
    my_robot = Robot(camera_device_id=2, arduino_port='COM5',
               station_coaards=(10, 2), json_web_path='./Puzzkey.json', storage_bucket='puzz-a02e2.appspot.com',
               crop_tuple = (238, 100, 241, 100), puzzle_size_tuple = (6,4), puzzle_num= puzzle_num)
    my_robot.camera.show()
    my_robot.web_controller.wait_for_needed_val_input("signals", "playerReady", True)
    #my_robot.g_code_maker.move_robot_realtive(utils.move_on_frame(11), 22)
    #my_robot.g_code_maker.send_g_code_to_arduino('COM5', ["G21G91G1Y5X5F2000\n"])
    for cur_round in range(num_of_pieces):
        my_robot.g_code_maker.move_piece_to_station_and_wait(22, cur_round)
        sleep(1)
        photo_name = "piece_photo_" + str(random.randrange(0, 1000000)) + ".jpg"
        my_robot.camera.take_photo(photo_name)
        my_robot.camera.crop_photo(photo_name)

        public_url = my_robot.web_controller.upload_photo_and_return_public_url(photo_name)
        #my_robot.calculate_piece_loc_and_update(photo_name)
        my_robot.web_controller.update_firebase("signals", "CurrPhotoURL", public_url)
        my_robot.web_controller.update_firebase("signals", "choosePieceReady", True)
        my_robot.calculate_piece_loc_and_update(photo_name)
        my_robot.wait_for_user_piece_choice()
        my_robot.g_code_maker.move_piece_to_station()
        #my_robot.g_code_maker.move_robot_realtive((0,2))
        my_robot.g_code_maker.move_piece_flow(my_robot.user_piece_coaards, 22, -1)
        sleep(0.5)
        #if cur_round > 11 and cur_round < 16:
        #    my_robot.g_code_maker.move_robot_realtive((7, 3), 22)
        my_robot.g_code_maker.move_robot_realtive(utils.move_on_frame(cur_round +1), 22)
        sleep(0.5)
        #my_robot.camera.delete_photo(photo_name)










