#!/usr/bin/env python
import RPi.GPIO as GPIO
import ifroglab_jetson
import time
from std_msgs.msg import UInt8MultiArray
#from funcase_client.msg import JoyCmd
import rospy 
import os

os.system('sudo chmod a+rw /dev/ttyUSB0')
LoRa = ifroglab_jetson.LoRa()
rospy.init_node('lora_rec_joy')

GPIO.setmode(GPIO.BCM)
lora_in = 18
GPIO.setup(lora_in,GPIO.IN)

## lora setup
ser=LoRa.FunLora_initByName("/dev/ttyUSB0")
LoRa.FunLora_0_GetChipID()
LoRa.FunLora_1_Init()
LoRa.FunLora_2_ReadSetup()
LoRa.FunLora_3_RX();
print("Lora is ready !!")

joy = []
joy_cmd = UInt8MultiArray()
while not rospy.is_shutdown():
  pin2 = GPIO.input(lora_in)
  #print(pin2)

  if pin2 == 1:
    str_data = []
    data=LoRa.FunLora_6_readPureData()
    if len(data) != 0:  
      if data[0] != 42:
        for i in data:
          if i >= 48 and i <= 57:
            str_data.append(chr(i))
        str_data_ = "".join(str_data) ## list -> str
        joy.append(int(str_data_))
        #print(joy)
      if len(joy) == 3:
        print("array joy = ")
        print(joy)
        joy_cmd.data = joy
        pub = rospy.Publisher('joy_commands', UInt8MultiArray, queue_size = 10)
        pub.publish(joy_cmd)
        joy = []
      
# close lora
LoRa.FunLora_close()
