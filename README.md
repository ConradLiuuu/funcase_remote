At PC:

Encode joystick and send commanad via LoRa:
roslaunch funcase_remote lora_write_joystick.launch

Encode joystick and send commanad via ROS:
roslaunch funcase_remote ros_write_joystick.launch


At robot:

Receive Encode joystick command via LoRa:
roslaunch funcase_remote lora_rec_joycmd.launch

