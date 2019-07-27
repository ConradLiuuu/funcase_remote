#!/usr/bin/env python 
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import UInt8MultiArray

class Joycmd:

    def __init__(self):
        self.axe = []
        self.button = []
        self.sum_button = 0
        self.sum_axe_front = 0
        self.sum_axe_below = 0
        self.boundary = 0.5
        self.sub_joy = rospy.Subscriber("/joy", Joy, self.callback, queue_size=1)
        self.pub_joycmd = rospy.Publisher('/joy_commands', UInt8MultiArray, queue_size = 10)

    def callback(self, data):
        self.axe = data.axes
        self.button = data.buttons
        seg_axes = [0,0,0,0,0,0,0,0]
        enc_axes = [0,0,0,0,0,0,0,0]

        ## processing axes
        for i in range(0,8):
            tmp = self.axe[i]
            if tmp >= self.boundary:
                tmp = 1
            elif tmp < self.boundary and tmp > -self.boundary:
                tmp = 0
            elif tmp <= -self.boundary:
                tmp = -1
            seg_axes[i] = tmp

        if seg_axes[2] <= 1 and seg_axes[2] > -1:
            seg_axes[2] = 0
        elif seg_axes[2] == -1:
            seg_axes[2] = 1
        if seg_axes[5] <= 1 and seg_axes[5] > -1:
            seg_axes[5] = 0
        elif seg_axes[5] == -1:
            seg_axes[5] = 1

        tmp2 = 0
        for i in range(0,8):
            if seg_axes[i] == 0:
                tmp2 = 0
            elif seg_axes[i] == 1:
                tmp2 = 1
            elif seg_axes[i] == -1:
                tmp2 = 2
            enc_axes[i] = tmp2

        ## encoding axes
        self.sum_axe_front = enc_axes[0]*64 + enc_axes[1]*16 + enc_axes[3]*4 + enc_axes[4]*1
        self.sum_axe_below = enc_axes[2]*64 + enc_axes[5]*16 + enc_axes[6]*4 + enc_axes[7]*1
        self.sum_button = self.button[0]*64 + self.button[1]*32 + self.button[2]*16 + self.button[3]*8 + self.button[7]*4 + self.button[6]*2 + self.button[8]*1

        joy_cmddd = UInt8MultiArray()
        joy_cmddd.data = [self.sum_button, self.sum_axe_front, self.sum_axe_below]
        self.pub_joycmd.publish(joy_cmddd)

if __name__ == '__main__':
    rospy.init_node('ros_write_joycommands')
    Joycmd()
    rospy.spin()
