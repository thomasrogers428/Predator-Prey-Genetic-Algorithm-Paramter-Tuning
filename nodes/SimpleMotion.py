#!/usr/bin/env python

# import of relevant libraries.
import rospy # module for ROS APIs

# import msg/action/srv
from geometry_msgs.msg import Twist # message type for cmd_vel


FREQUENCY = 10 #Hz.
LASER_ANGLE_FRONT = 0 # radians
MIN_THRESHOLD_DISTANCE = 0.8 # m, threshold distance.

# Rotate in place method adapted from simple_motion class
def rotate_in_place(rotation_angle, cmd_pub, angular_velocity):
    """
    Rotate in place the robot of rotation_angle (rad) based on fixed velocity.
    Assumption: Counterclockwise rotation.
    """
    twist_msg = Twist()
    twist_msg.angular.z = angular_velocity
    
    duration = rotation_angle / twist_msg.angular.z
    start_time = rospy.get_rostime()
    rate = rospy.Rate(FREQUENCY)
    while not rospy.is_shutdown():
        # Check if done
        if rospy.get_rostime() - start_time >= rospy.Duration(duration):
            break
            
        # Publish message.
        cmd_pub.publish(twist_msg)
        
        # Sleep to keep the set frequency.
        rate.sleep()

    # Rotated the required angle, stop.
    stop(cmd_pub)

# Move forward method adapted from simple_motion class
def move_forward(distance, cmd_pub, linear_velocity):
    """Function to move_forward for a given distance."""
    # Rate at which to operate the while loop.
    rate = rospy.Rate(FREQUENCY)

    # Setting velocities. 
    twist_msg = Twist()
    twist_msg.linear.x = linear_velocity
    start_time = rospy.get_rostime()
    duration = rospy.Duration(distance/twist_msg.linear.x)

    # Loop.
    while not rospy.is_shutdown():
        # Check if traveled of given distance based on time.
        if rospy.get_rostime() - start_time >= duration:
            break

        cmd_pub.publish(twist_msg)

        # Sleep to keep the set publishing frequency.
        rate.sleep()

    # Traveled the required distance, stop.
    stop(cmd_pub)
    
def stop(cmd_pub):
    """Stop the robot."""
    twist_msg = Twist()
    cmd_pub.publish(twist_msg)