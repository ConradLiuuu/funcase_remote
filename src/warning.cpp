#include <stdio.h>
#include <ros/ros.h>
#include "std_msgs/Int8.h"

void callback(const std_msgs::Int8::ConstPtr& msg)
{
  if (msg -> data == 0)
  {
    ROS_INFO("play warning one");
    system("omxplayer -o local warning1.mp3");
  }
  if (msg -> data == 1)
  {
    ROS_INFO("play music two");
    system("omxplayer -o local warning2.mp3");
  }
  if (msg -> data == 2)
  {
    ROS_INFO("play music three");
    system("omxplayer -o local warning3.mp3");
  }
}
int main(int argc, char** argv)
{
  ros::init(argc,argv,"warning");
  ROS_INFO("Ready to make warning");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("BZ5",10,callback);
  ros::spin();
  return 0;
}

