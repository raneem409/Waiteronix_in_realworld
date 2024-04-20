# ros_wheel_encoder_odometry

# Wheel Encoder and Odometry ROS Package

This ROS package simulates wheel encoder ticks and calculates odometry for a differential drive robot.

## Description

This package consists of two nodes:
- `ticks_publisher`: Simulates wheel encoder ticks.
- `odom_node`: Calculates odometry and broadcasts transformations.

## Setup

1. Create a URDF file (`odom_baselink.xacro`) with the following frames:
   - Parent frame: odom
   - Child frame: base_link

2. Write a Python node (`ticks_publisher.py`) to simulate wheel encoder ticks.

3. Write another Python node (`odom_noder.py`) to calculate odometry and broadcast transformations. Set parameters such as wheel base, wheel radius, and ticks per revolution in this node.

4. Create a launch file (`odometry.launch`) to run both nodes and RViz together.

## Usage

1. Modify the values of ticks in the `ticks_publisher.py` node to control the movement of the robot.
   
2. Launch the nodes using the provided launch file:
    ``` bash
   roslaunch wheel_encoder odometry.launch
   ```
    
3. Set the fixed frame to `base_link` in RViz and visualize TF and the robot model to see the movement of the robot.


https://github.com/raneem409/ros_wheel_encoder_odometry/assets/72455839/3c3520bf-c2da-4a30-b399-851406504681

Users have the flexibility to control the robot's movement by changing the values of the ticks in `ticks_publisher node`

