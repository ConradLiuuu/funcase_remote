#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import ifroglab_funcase

class lora_write_joycmd:

    def __init__(self):
        ## LoRa init and setup
        self.LoRa = ifroglab_funcase.LoRa()
        self.ser = self.LoRa.FunLora_initByName("/dev/ttyACM0")
        self.LoRa.FunLora_0_GetChipID()
        self.LoRa.FunLora_1_Init()
        self.LoRa.FunLora_2_ReadSetup()
        self.LoRa.FunLora_3_TX()
        print "LoRa is ready !!!"
        ## init processing tool
        self.header = '*'
        self.sep = ','
        self.axe = []
        self.joy_cmd = []
        self.sum_button = 0
        self.sum_axe_front = 0
        self.sum_axe_below = 0
        self.boundary = 0.5
        self.sub_joy = rospy.Subscriber("/joy", Joy, self.callback, queue_size=1)

    def callback(self, data):
        self.axe = data.axes
        self.button = data.buttons
        seg_axes = []
        enc_axes = []

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

        self.joy_cmd = header + str(self.sum_button) + sep + str(self.sum_axe_front) + sep + str(self.sum_axe_below) +sep
        self.LoRa.FunLora_5_write16bytesArrayString(self.joy_cmd)
        print "joy_cmd = ", self.joy_cmd

if __name__ == '__main__':
    rospy.init_node('lora_write_joycmd')
    lora_write_joycmd()
    rospy.spin()

