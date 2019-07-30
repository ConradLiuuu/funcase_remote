#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray
import random
from time import sleep

rospy.init_node('pub_int16_arr')

pose = Int16MultiArray()
pose.data = [0,0,0,0,0,0,0,0,0]
#pose.data = [145,100,223,348,402,54,26,37,8]

for i in range(0,9):
    pose.data[i] = random.randint(1,300)
print "pose = ", pose.data
for i in range(0,2):
    pub = rospy.Publisher('/hand_pose', Int16MultiArray, queue_size = 10)
    pub.publish(pose)
    sleep(1)
