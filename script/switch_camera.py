#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
import RPi.GPIO as gpio

class switch_camera:

    def __init__(self):
        self.switch_pin = 17
        self.switch = False
        gpio.setmode(gpio.BCM)
        gpio.setup(self.switch_pin,gpio.OUT)
        gpio.output(self.switch_pin,0)
        self.sub = rospy.Subscriber("/switch_camera", Bool, self.callback, queue_size=1)

    def callback(self, data):
        self.switch = data.data

        if self.switch == True:
            gpio.output(self.switch_pin, 1)
        if self.switch == False:
            gpio.output(self.switch_pin, 0)
        print "switch status is : ", self.switch

if __name__ == '__main__':
    rospy.init_node("switch_camera")
    switch_camera()
    rospy.spin()

