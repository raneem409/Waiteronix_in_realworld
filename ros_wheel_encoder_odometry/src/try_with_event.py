#!/usr/bin/env python

import rospy
import serial
import threading
import time
from std_msgs.msg import Int32

from std_msgs.msg import String

# Function to read data from serial port
def read_from_port(ser, right_publisher,left_publisher):
    while not rospy.is_shutdown():

        # Read a line of data from the serial port
        line = ser.readline().decode().strip()
        d = str(line)
        if(d != ""):
           print (d)
           rospy.loginfo("Received: %s", line)
           values = d.split(',')
           print("Values:", values)  # Add this line to check the content of values
    	   c1 = values[1].split('=')[1]
           c2 = values[2].split('=')[1]
           right_ticks = int(c1)
           left_ticks = int(c2)

           # Publish the received data as a ROS message
           right_publisher.publish(right_ticks)
           left_publisher.publish(left_ticks)
  
# ROS node initialization
rospy.init_node('serial_event_node')

# Open the serial port
try:
    ser = serial.Serial('/dev/ttyUSB1', 9600)  # Change port and baud rate as needed
except serial.SerialException as e:
    rospy.logerr("Error opening serial port: %s", e)
    exit()

# ROS publisher for the received data
right_publisher = rospy.Publisher('right_wheel_ticks', Int32, queue_size=10)
left_publisher = rospy.Publisher('left_wheel_ticks', Int32, queue_size=10)

# Create a thread to continuously read from the serial port
read_thread = threading.Thread(target=read_from_port, args=(ser, right_publisher,left_publisher))
read_thread.daemon = True
read_thread.start()

# ROS spin loop
rospy.spin()

# Close the serial port when the node is shutdown
ser.close()
