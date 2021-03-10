from g_code_maker import g_sender
from camera import camera
from time import sleep
from web_controller import web_controller
import utils


class Robot:
    def __init__(self, camera_device_id, arduino_port, station_coaards, json_web_path, storage_bucket, crop_tuple, puzzle_size_tuple, puzzle_num):
        self.puzzle_size_tuple = puzzle_size_tuple
        self.user_piece_chosen = -1
        self.user_piece_coaards = -1
        self.camera = camera(camera_device_id, crop_tuple, puzzle_size_tuple, puzzle_num)
        self.g_code_maker = g_sender(arduino_port, station_coaards)
        self.web_controller = web_controller(json_web_path, storage_bucket)
        self.web_controller.update_firebase("signals", "gameReady", "true")
        self.web_controller.update_firebase("signals", "puzzleNumber", puzzle_num)
        self.g_code_maker.move_servo_up_without_piece()
        sleep(1)
        self.g_code_maker.move_robot_absolute((5, 25))

        # update to rest of init phase (g-sender?)



    def wait_for_user_piece_choice(self):
        self.web_controller.wait_for_new_val_input("signals", "pieceChosen", self.user_piece_chosen)
        self.user_piece_chosen = self.web_controller.get_value_from_firebase("signals", "pieceChosen")
        self.user_piece_coaards = utils.piece_to_coaards(self.user_piece_chosen)

    def calculate_piece_loc_and_update(self, photo_path):
        piece_num = self.camera.find_matching_coaards(photo_path)
        self.web_controller.update_firebase("signals", "hint", piece_num)

    def take_piece_to_station_and_take_photo(self, photo_name):
        self.g_code_maker.move_piece_flow(self.g_code_maker.station_coaards, 20)
        self.camera.take_photo(photo_name)
        self.camera.crop_photo(photo_name)
        clue = self.camera.find_matching_coaards(photo_name, self.puzzle_size_tuple)
        public_url = self.web_controller.upload_photo_and_return_public_url(photo_name)
        self.web_controller.update_firebase("signals", "CurrPhotoURL",public_url)









