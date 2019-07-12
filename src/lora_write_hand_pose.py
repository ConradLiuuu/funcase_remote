#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray
import ifroglab_funcase

rospy.init_node('lora_write_hand_pose')
LoRa =  ifroglab_funcase.LoRa()

# LoRa setup
ser=LoRa.FunLora_initByName("/dev/ttyACM0")
LoRa.FunLora_0_GetChipID()
LoRa.FunLora_1_Init()
LoRa.FunLora_2_ReadSetup()
LoRa.FunLora_3_TX()
print("LoRa Ready!!!")

header = '*'
sep = ','

def callback(data):
    pose = data.data
    #print(pose)
    str_pose = str(pose[0]) + sep + str(pose[1]) + sep + str(pose[2]) + sep + str(pose[3]) + sep + str(pose[4]) + sep + str(pose[5]) + sep + str(pose[6]) + sep + str(pose[7]) + sep + str(pose[8]) + sep
    #print(str_pose)
    #print(len(str_pose))

    if len(str_pose) <= 16:
        LoRa.FunLora_5_write16bytesArrayString(header)
        LoRa.FunLora_5_write16bytesArrayString(str_pose)
        print(str_pose)
    if len(str_pose) > 16 and len(str_pose) <= 32:
        front = str_pose[0:16]
        below = str_pose[16:len(str_pose)]
        print(front)
        print(below)
        LoRa.FunLora_5_write16bytesArrayString(header)
        LoRa.FunLora_5_write16bytesArrayString(front)
        LoRa.FunLora_5_write16bytesArrayString(below)        
    if len(str_pose) > 32:
        front = str_pose[0:16]
        midd = str_pose[16:32]
        below = str_pose[32:len(str_pose)]
        print(front)
        print(midd)
        print(below)
        LoRa.FunLora_5_write16bytesArrayString(header)
        LoRa.FunLora_5_write16bytesArrayString(front)
        LoRa.FunLora_5_write16bytesArrayString(midd)
        LoRa.FunLora_5_write16bytesArrayString(below)

def listener():
    rospy.Subscriber("hand_pose", Int16MultiArray, callback)
    rospy.spin()

while not rospy.is_shutdown():
    listener()
