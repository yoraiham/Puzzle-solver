from time import sleep
import serial
import g_code_maker
import camera



g_sender = g_code_maker.g_sender((0,0), 'COM5')

#g_sender.reset_to_zero()

g_sender.move_servo_up()

#g_sender.move_robot_realtive((1,2), 20)

g_sender.move_servo_down()

g_sender.activate_pump()

g_sender.move_servo_up()
g_sender.move_robot_realtive((1,1), 20)


g_sender.move_servo_down()

g_sender.deactivate_pump()









my_camera = camera.camera(2, "yorai.jpeg")

img1 = my_camera.take_photo("hi")

print(my_camera.find_matching_coaards(img1, 4, 4))










