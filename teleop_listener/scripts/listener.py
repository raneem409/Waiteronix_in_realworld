#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
import serial

wheel_base = 0.5  # Distance between the two wheels
wheel_radius = 0.1  # Radius of the wheels
serial_msg = ""

# Define serial port and baudrate
ser = serial.Serial('/dev/ttyUSB1', 9600)  # Assuming USB0 is the port and baudrate is 9600

def convert_cmd_to_pwm():
    global linear_velocity
    global angular_velocity
    global vel_l
    global vel_r
    global dir_l
    global dir_r

    # Calculate the wheel velocities
    vel_l = linear_velocity - (angular_velocity * wheel_base / 2)
    vel_r = linear_velocity + (angular_velocity * wheel_base / 2)

    # Determine the direction of the wheel velocities
    dir_l = 1 if vel_l >= 0 else 0
    dir_r = 1 if vel_r >= 0 else 0

    # Take the absolute values of the wheel velocities
    vel_l = abs(vel_l)
    vel_r = abs(vel_r)


def format_serialmsg():
    global serial_msg
    serial_msg = '$' + str(dir_r) + str(dir_l) + str(int(vel_r * 15.085)) + 's'  # Assuming you need integer values for velocity


def callback(twist_msg):
    rospy.loginfo(rospy.get_caller_id() + "Received Data")
    rospy.loginfo('Sending ' + repr(twist_msg))
    global linear_velocity
    global angular_velocity
    linear_velocity = twist_msg.linear.x
    angular_velocity = twist_msg.angular.z
    convert_cmd_to_pwm()
    format_serialmsg()
    rospy.loginfo(serial_msg)
    ser.write(serial_msg.encode())  # Send the serial message


def listener():
    rospy.init_node('twist_listener')
    rospy.Subscriber('/cmd_vel', Twist, callback)
    rospy.loginfo('Twist Listener started')
    rospy.spin()


if __name__ == '__main__':
    listener()
