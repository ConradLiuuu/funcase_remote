#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
switch_pin = 17

gpio.setup(switch_pin,gpio.OUT)
gpio.output(switch_pin,0)
switch = False

def callback(data):
    global switch
    swit = data.data

    if swit == True:
        switch = True
        gpio.output(switch_pin, 1)
    if swit == False:
        switch = False
        gpio.output(switch_pin, 0)
    print "switch is ",switch

def listener():
    rospy.init_node("switch_camera")
    rospy.Subscriber("/switch_camera", Bool, callback, queue_size=1)

while not rospy.is_shutdown():
    listener()
    rospy.spin()
