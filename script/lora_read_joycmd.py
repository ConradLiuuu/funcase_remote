#!/usr/bin/env python
import RPi.GPIO as GPIO
import ifroglab_jetson
from std_msgs.msg import UInt8MultiArray
import rospy

class lora_read_joycmd:

    def __init__(self):
        ## RPi.GPIO setting
        self.lora_in = 18
        self.pin2 = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lora_in,GPIO.IN)
        ## LoRa init and setup
        self.data
        self.LoRa = ifroglab_funcase.LoRa()
        self.ser = self.LoRa.FunLora_initByName("/dev/ttyUSB0")
        self.LoRa.FunLora_0_GetChipID()
        self.LoRa.FunLora_1_Init()
        self.LoRa.FunLora_2_ReadSetup()
        self.LoRa.FunLora_3_RX()
        print "LoRa is ready !!!"
        ## ros init
        self.pub = rospy.Publisher('/joy_commands', UInt8MultiArray, queue_size = 10)
        self.joy_cmd = UInt8MultiArray()

    def read(self):
        joy = []
        self.pin2 = GPIO.input(self.lora_in)
        if self.pin2 == 1:
            self.data = LoRa.FunLora_6_readPureData()
            if len(self.data) > 0 and self.data[0] == 42:
                str_data = []
                for i in self.data:
                    if i == 42:
                        print "joy_cmd = ", joy
                        self.joy_cmd.data = joy
                        pub.publish(self.joy_cmd)
                        joy = []
                    if i >= 44 and i <= 57:
                        if i != 44:
                            str_data.append(chr(i))
                            str_data2 = "".join(str_data)
                        if i == 44:
                            joy.append(int(str_data2))
                            str_data = []

if __name__ == '__main__':
    rospy.init_node("lora_read_joycmd")
    read = lora_read_joycmd()
    read.read()
