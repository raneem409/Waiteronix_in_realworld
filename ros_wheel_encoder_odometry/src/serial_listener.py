#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import serial

def serial_listener():
    # Initialize ROS node
    rospy.init_node('serial_listener_node', anonymous=True)

    # Serial port configuration
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate accordingly

    # ROS publishers
    right_wheel_ticks_pub = rospy.Publisher('right_wheel_ticks', Int32, queue_size=10)
    left_wheel_ticks_pub = rospy.Publisher('left_wheel_ticks', Int32, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # Read data from serial port
        data = ser.readline().decode().strip()
	d = str(data)

        # Split data into integers
        try:
  	    values = d.split(',')
   	    print("Values:", values)  # Add this line to check the content of values

    	    c1 = values[1].split('=')[1]
    	    c2 = values[2].split('=')[1]

            print("c1:", c1)
            print("c2:", c2)
 
            right_ticks = 0
            left_ticks = 0

            print("c1:", int(c1))
            print("c2:", int(c2))

# Extract integer values from each part
	    #values = [int(part.split('=')[1]) for part in parts]

# Assign the values to variables
            #r, right_ticks, left_ticks = values
            
        except ValueError:
            rospy.logerr("Failed to parse serial data: {}".format(data))
            continue

        # Publish data to topics
        right_wheel_ticks_pub.publish(right_ticks)
        left_wheel_ticks_pub.publish(left_ticks)

        rate.sleep()

    # Close serial port when the node is shutting down
    ser.close()

if __name__ == '__main__':
    try:
        serial_listener()
    except rospy.ROSInterruptException:
        pass




#right_ticks, left_ticks = map(int, data.split(','))  # Assuming data format is 'right,left'

