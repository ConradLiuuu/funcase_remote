#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray
import RPi.GPIO as gpio

class Sg90:

    def __init__(self):
        self.src_pin_axe3 = 23
        self.src_pin_axe4 = 24
        self.src_pin_axe8 = 25
        #self.src_pin = rospy.get_param("/src_pin")
        self.freq = 100
        gpio.setmode(gpio.BCM)
        gpio.setup(self.src_pin_axe3, gpio.OUT)
        gpio.setup(self.src_pin_axe4, gpio.OUT)
        gpio.setup(self.src_pin_axe8, gpio.OUT)

        self.pwm_axe3 = gpio.PWM(self.src_pin_axe3, self.freq) ## value:1~30
        self.pwm_axe4 = gpio.PWM(self.src_pin_axe4, self.freq)
        self.pwm_axe8 = gpio.PWM(self.src_pin_axe8, self.freq)
        self.pwm_axe3.start(1) ## init pwm value
        self.pwm_axe4.start(3)
        self.pwm_axe8.start(1)
        self.sub = rospy.Subscriber("/funcasebot/arm_controller/move_arm", Int16MultiArray, self.callback, queue_size=1)
        print "Ready to control sg90"

    def callback(self, data):
        self.pwm_axe3.ChangeDutyCycle(data.data[3])
        self.pwm_axe4.ChangeDutyCycle(data.data[4])
        self.pwm_axe8.ChangeDutyCycle(data.data[8])

if __name__ == '__main__':
    rospy.init_node("sg90")
    Sg90()
    rospy.spin()

