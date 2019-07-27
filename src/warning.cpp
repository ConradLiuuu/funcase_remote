#include <stdio.h>
#include <ros/ros.h>
#include "std_msgs/Bool.h"
using namespace ros;

class Warning
{
public:
  Warning()
  {
    sub = nh.subscribe("BZ5", 10, &Warning::callback, this);
  }
  void callback(const std_msgs::Bool::ConstPtr& msg)
  {
    if (msg -> data == true)
    {
      ROS_INFO("Detect target !!!");
      system("omxplayer -o local warning1.mp3");
    }
  }

private:
  NodeHandle nh;
  Subscriber sub;
};

int main(int argc, char **argv)
{
  init(argc,argv,"warning");
  ROS_INFO("Ready to issue target warning");
  Warning warning;
  spin();
  return 0;
}

