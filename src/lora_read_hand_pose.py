#!/usr/bin/env python
import ifroglab_jetson as ifroglab
import rospy
from std_msgs.msg import Int16MultiArray
from time import time
import os
import RPi.GPIO as gpio

os.system('sudo chmod a+rw /dev/ttyUSB0')
LoRa = ifroglab.LoRa()
rospy.init_node('lora_read_hand_pose')

gpio.setmode(gpio.BCM)
gpio.setup(22,gpio.IN)

ser=LoRa.FunLora_initByName("/dev/ttyUSB0")
LoRa.FunLora_0_GetChipID()
LoRa.FunLora_1_Init()
LoRa.FunLora_2_ReadSetup();
LoRa.FunLora_3_RX();
LoRa.debug=False
print("Lora ready!!")

hand_pose = []
pub_pose = Int16MultiArray()
while not rospy.is_shutdown():
    pin2 = gpio.input(22)
    #print("pin2 = ",pin2)
    if pin2 == 1:
        data=LoRa.FunLora_6_readPureData()
        #for i in data:
            #print(chr(i))
        
        if len(data) > 0:
            str_data = []
            for i in data:
                #print(chr(i))
                if i == 43:
                    print "hand_pose = ",hand_pose
                    pub_pose.data = hand_pose
                    pub = rospy.Publisher('hand_pose', Int16MultiArray, queue_size = 10)
                    pub.publish(pub_pose)
                    #print(len(hand_pose))
                    hand_pose = []
                if i >= 44 and i <= 57:
                    #print(chr(i))
                    if i != 44:
                        str_data.append(chr(i))
                        str_data2 = "".join(str_data)  
                    if i == 44:
                        hand_pose.append(int(str_data2))
                        str_data = []
        
LoRa.FunLora_close()
