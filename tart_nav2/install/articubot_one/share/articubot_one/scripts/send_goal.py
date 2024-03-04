#!/usr/bin/env python3

import time

from geometry_msgs import PoseStamped, Pose
from rclpy.duration import Duration
import rclpy

from robot_navigator import BasicNavigator, TaskResult


def main():
    rclpy.init()

    navigator = BasicNavigator()
    navigator.wautUntilNav2Active()

    goal_poses = []

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = -2.0
    goal_pose.pose.position.y = 0.0
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    goal_poses.append(goal_pose)


    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 0.0
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    goal_poses.append(goal_pose)
    navigator.goThroughPoses(goal_poses)  
    i = 0
  # Keep doing stuff as long as the robot is moving towards the goal poses
    while not navigator.isNavComplete():
    ################################################
    #
    # Implement some code here for your application!
    #
    ################################################    # Do something with the feedback
        i = i + 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('Distance remaining: ' + '{:.2f}'.format(
                feedback.distance_remaining) + ' meters.')      # Some navigation timeout to demo cancellation
        if Duration.from_msg(feedback.navigation_time) > Duration(seconds=1000000.0):
            navigator.cancelNav()      # Some navigation request change to demo preemption

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')  # Close the ROS 2 Navigation Stack
    navigator.lifecycleShutdown()  
    exit(0)

if __name__ == '__main__':
    main()