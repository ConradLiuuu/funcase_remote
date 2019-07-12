#!/usr/bin/env python
import sys
from time import sleep
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/GPIO')
import Jetson.GPIO as gpio
import rospy
#from funcase_client.msg import JoyCmd
from std_msgs.msg import Bool

gpio.setmode(gpio.BCM)
switch = 18
gpio.setup(switch, gpio.OUT, initial = gpio.LOW)
#gpio.setwarnings(False)
swit = False

def callback(data):
    global swit
    #joy_cmd = data
    #button = joy_cmd.joy[0].encode("hex")
    sum_ = data.data
    #print(c)
    
    if sum_ == True:
        swit = True
        gpio.output(switch,gpio.HIGH)
    if sum_ == False:
        swit = False
        gpio.output(switch,gpio.LOW)
    print(swit)
     
def listener():
    rospy.init_node('switch_camera')
    rospy.Subscriber("/switch_camera", Bool, callback, queue_size=1)

while not rospy.is_shutdown():
    listener()
    rospy.spin()

