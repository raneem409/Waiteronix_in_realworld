# ros_wheel_encoder_odometry

# Wheel Encoder and Odometry ROS Package

This ROS package simulates wheel encoder ticks and calculates odometry for a differential drive robot.

## Description

This package consists of two nodes:
- `odom_node`: Calculates odometry and broadcasts transformations.
- `try_with_event`: recieve the real ticks of encoder and publish them using event.

## Setup

1. Create a URDF file (`odom_baselink.xacro`) with the following frames:
   - Parent frame: odom
   - Child frame: base_link

3. Write another Python node (`odom_noder.py`) to calculate odometry and broadcast transformations. Set parameters such as wheel base, wheel radius, and ticks per revolution in this node.

4. Write a Python node (`try_with_event.py`) it is event node takes the real ticks values from encoder by serial conniction and split them then publish the results in right ticks and left ticks topics.  

5. Create a launch file (`odometry.launch`) to run both nodes and RViz together.

## Usage

1. Modify the values of your encoder in (`try_with_event.py`) node
   
2. Launch the nodes using the provided launch file:
    ``` bash
   roslaunch wheel_encoder odometry.launch
   ```
    
3. Run RViz then Set the fixed frame to `base_link` and visualize TF and the robot model to see the movement of the robot.
