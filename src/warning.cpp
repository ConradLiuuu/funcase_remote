#include <stdio.h>
#include <ros/ros.h>
#include "std_msgs/Bool.h"

void callback(const std_msgs::Bool::ConstPtr& msg)
{
  if (msg -> data == true)
  {
    ROS_INFO("play warning one");
    system("omxplayer -o /home/aaaaa/catkin_ws/src/funcase_remote/src/local warning1.mp3");
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

