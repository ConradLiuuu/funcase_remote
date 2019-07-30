#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt8MultiArray
import ifroglab_funcase

LoRa =  ifroglab_funcase.LoRa()
rospy.init_node('lora_joycmd_hand')

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
    #array = []
    array = data.data
    #print "array = ", array.data
    front = header + str(array[0]) + sep + str(array[1]) + sep + str(array[2]) + sep #+ str(array[3]) + sep
    #print front
    button = str(array[4]) + sep + str(array[5]) + sep + str(array[6]) + sep + str(array[7]) + sep
    below = str(array[8]) + sep + str(array[9]) + sep

    LoRa.FunLora_5_write16bytesArrayString(front)
    #LoRa.FunLora_5_write16bytesArrayString(button)
    #LoRa.FunLora_5_write16bytesArrayString(below)

def listener():
    rospy.Subscriber("xbox_and_small_arm", UInt8MultiArray, callback, queue_size=1)
    rospy.spin()

while not rospy.is_shutdown():
    listener()

'''
class Lora_joycmd_hand:

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
        self.array = []
        self.sub_joycmd_hand = rospy.Subscriber("/xbox_and_small_arm", UInt8MultiArray, self.callback, queue_size=1)

    def callback(self, data):
        self.array = data.data
        print "array = ", self.array
        print chr(self.array[0])
        
        array_send = self.header + str(array[0]) + self.sep + str(array[1]) + self.sep + str(array[2]) + self.sep + str(array[3]) + self.sep + str(array[4]) + self.sep + str(array[5]) + self.sep + str(array[6]) + self.sep + str(array[7]) + self.sep + str(array[8]) + self.sep + str(array[9]) + self.sep
        #print "send : ", array_send

        front = self.header + str(array[0]) + self.sep + str(array[1]) + self.sep + str(array[2]) + self.sep + str(array[3]) + self.sep
        button = str(array[4]) + self.sep + str(array[5]) + self.sep + str(array[6]) + self.sep + str(array[7]) + self.sep
        below = str(array[8]) + self.sep + str(array[9]) + self.sep

        self.LoRa.FunLora_5_write16bytesArrayString(front)
        self.LoRa.FunLora_5_write16bytesArrayString(button)
        self.LoRa.FunLora_5_write16bytesArrayString(below)
        
if __name__ == '__main__':
    rospy.init_node('lora_joycmd_hand')
    Lora_joycmd_hand()
    rospy.spin()
'''
