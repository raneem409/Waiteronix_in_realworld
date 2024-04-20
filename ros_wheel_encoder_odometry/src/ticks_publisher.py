#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

if __name__ == '__main__':
    rospy.init_node('ticks_publisher')

    left_ticks_pub = rospy.Publisher('left_wheel_ticks', Int32, queue_size=10)
    right_ticks_pub = rospy.Publisher('right_wheel_ticks', Int32, queue_size=10)

    rospy.loginfo("Ticks publisher node started")
    rate = rospy.Rate(10)  # 10 Hz

    left_ticks = 0
    right_ticks = 0

    while not rospy.is_shutdown():   
      # Simulate increasing ticks for left and right wheels 	
      left_ticks += 1
      right_ticks += 1

      # Publish left and right wheel ticks
      left_ticks_pub.publish(left_ticks)
      right_ticks_pub.publish(right_ticks)
      
      rospy.loginfo("Left wheel ticks: %d, Right wheel ticks: %d", left_ticks, right_ticks)
      rate.sleep()

