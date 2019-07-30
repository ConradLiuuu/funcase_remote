#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16MultiArray
import ifroglab_funcase
from time import sleep

LoRa =  ifroglab_funcase.LoRa()
rospy.init_node('lora_write_joycmd_handpose')

# LoRa setup
ser=LoRa.FunLora_initByName("/dev/ttyACM0")
LoRa.FunLora_0_GetChipID()
LoRa.FunLora_1_Init()
LoRa.FunLora_2_ReadSetup()
LoRa.FunLora_3_TX()
print("LoRa Ready!!!")

header2 = '*'
sep = ','
seg_axes = []
enc_axes = []
joy_cmd = []

def callback_joycmd(data):
    axe = data.axes
    button = data.buttons
    joy = axe + button
    seg_axes = []
    enc_axes = []

    ## Segment axes
    for i in range(0,8):
        tmp = joy[i]
        if tmp > 0.5:
            tmp = 1
        elif tmp < 0.5 and tmp > -0.5:
            tmp = 0
        elif tmp < -0.5:
            tmp = -1
        seg_axes.append(tmp)
    
    
    if seg_axes[2] <= 1 and seg_axes[2] > -1:
        seg_axes[2] = 0
    elif seg_axes[2] == -1:
        seg_axes[2] = 1
    if seg_axes[5] <= 1 and seg_axes[5] > -1:
        seg_axes[5] = 0
    elif seg_axes[5] == -1:
        seg_axes[5] = 1
    
    #print("Segment axes = ",seg_axes)
    
    for i in range(0,8):
        if seg_axes[i] == 0:
            tmp2 = 0
        elif seg_axes[i] == 1:
            tmp2 = 1
        elif seg_axes[i] == -1:
            tmp2 = 2
        enc_axes.append(tmp2)
    
    ## Encoding axes
    sum_axe_front = enc_axes[0]*64 + enc_axes[1]*16 + enc_axes[3]*4 + enc_axes[4]*1
    #print("axe front part = ",seg_axes[0:4])
    #print("sum of axe front part = ",sum_axe_front)

    sum_axe_below = enc_axes[2]*64 + enc_axes[5]*16 + enc_axes[6]*4 + enc_axes[7]*1
    #print("axe below part = ",seg_axes[4:8])
    #print("sum of axe below part = ",sum_axe_below)
    
    ## Encoding buttons
    sum_button = joy[8]*64 + joy[9]*32 + joy[10]*16 + joy[11]*8 +joy[15]*4 + joy[14]*2 + joy[16]*1
    #print("sum of buttons =",sum_button) 

    #joy_cmd = [header2,sum_button,sum_axe_front,sum_axe_below]
    joy_cmd = header2 + str(sum_button) + sep + str(sum_axe_front) + sep + str(sum_axe_below) +sep
    #print("joy_cmd = ",joy_cmd)
    LoRa.FunLora_5_write16bytesArrayString(joy_cmd)
    print joy_cmd
    

def listener():
    rospy.Subscriber("/joy", Joy, callback_joycmd, queue_size=1)
    rospy.spin()

while not rospy.is_shutdown():
    listener()
