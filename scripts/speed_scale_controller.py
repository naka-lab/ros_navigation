#! /usr/bin/env python
import geometry_msgs.msg
import numpy as np
import rospy
import std_msgs.msg

class SpeedScalingController:
    def __init__(self):
        rospy.init_node( "speed_scaling_controller" )

        self.pub_scaled_vel = rospy.Publisher("scaled_cmd_vel", geometry_msgs.msg.Twist, queue_size=10)
        self.sub_vel_sub = rospy.Subscriber('cmd_vel', geometry_msgs.msg.Twist, self.cmd_vel_callback  )
        rospy.spin()


    def cmd_vel_callback( self, msg ):
        trans_scaling_factor = rospy.get_param( rospy.get_name()+"/trans_scaling_factor", 1.0) 
        rot_scaling_factor = rospy.get_param( rospy.get_name()+"/rot_scaling_factor", 1.0) 

        if msg.linear.x>0.15:
            msg.linear.x *= trans_scaling_factor
            msg.angular.z *= rot_scaling_factor

            print( trans_scaling_factor, rot_scaling_factor , msg.linear.x, msg.angular.z )

        self.pub_scaled_vel.publish(msg)


def main():
    SpeedScalingController()

if __name__ == '__main__':
    main()