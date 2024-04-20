#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Twist, Vector3
from tf.transformations import quaternion_from_euler
from math import cos, sin
import tf

class WheelEncoderOdom:
    def __init__(self):
        rospy.init_node('wheel_encoder_odom')
        
        self.left_ticks = 0
        self.right_ticks = 0
        self.left_ticks_prev = 0
        self.right_ticks_prev = 0
        
        self.wheelbase = 0.45  # Distance between wheels (adjust as needed)
        self.wheel_radius = 0.08  # Wheel radius (adjust as needed)
        self.ticks_per_revolution = 32  # Ticks per revolution (adjust as needed)
        
        self.pose_x = 0.0
        self.pose_y = 0.0
        self.pose_theta = 0.0
        
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        rospy.Subscriber('/left_wheel_ticks', Int32, self.left_ticks_callback)
        rospy.Subscriber('/right_wheel_ticks', Int32, self.right_ticks_callback)
        
        self.rate = rospy.Rate(10)  # 10 Hz
        
    def left_ticks_callback(self, msg):
        self.left_ticks = msg.data
        
    def right_ticks_callback(self, msg):
        self.right_ticks = msg.data
        
    def calculate_odometry(self):
        delta_left_ticks = self.left_ticks - self.left_ticks_prev
        delta_right_ticks = self.right_ticks - self.right_ticks_prev
        
        distance_left = (delta_left_ticks * 2 * 3.14159 * self.wheel_radius) / self.ticks_per_revolution
        distance_right = (delta_right_ticks * 2 * 3.14159 * self.wheel_radius) / self.ticks_per_revolution
        
        delta_distance = (distance_left + distance_right) / 2
        delta_theta = (distance_right - distance_left) / self.wheelbase
        
        self.pose_x += delta_distance * cos(self.pose_theta)
        self.pose_y += delta_distance * sin(self.pose_theta)
        self.pose_theta += delta_theta
        
        self.left_ticks_prev = self.left_ticks
        self.right_ticks_prev = self.right_ticks
         
    def publish_odometry(self):
        odom_msg = Odometry()
        odom_msg.header.stamp = rospy.Time.now()
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"
        
        odom_msg.pose.pose.position.x = self.pose_x
        odom_msg.pose.pose.position.y = self.pose_y
        odom_msg.pose.pose.position.z = 0.0
        
        quat = quaternion_from_euler(0, 0, self.pose_theta)
        odom_msg.pose.pose.orientation = Quaternion(*quat)
        
        odom_msg.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        
        self.odom_pub.publish(odom_msg)
        
        ##################################################
        ### broadcast the transformations
        ##################################################
        # since all odometry is 6DOF we'll need a quaternion created from yaw
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.pose_theta)
        current_time = rospy.Time.now()
        odom_broadcaster = tf.TransformBroadcaster()
        # first, we'll publish the transform over tf
        odom_broadcaster.sendTransform(
        (self.pose_x, self.pose_y , 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom" )
        ##################################################
        
    def run(self):
        while not rospy.is_shutdown():
            self.calculate_odometry()
            self.publish_odometry()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        wheel_encoder_odom = WheelEncoderOdom()
        wheel_encoder_odom.run()
    except rospy.ROSInterruptException:
        pass

