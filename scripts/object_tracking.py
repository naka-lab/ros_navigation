#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

cmd_pub = None
def callback(data):
    global cmd_pub
    twist = Twist()
    twist.linear.x = 0
    twist.angular.z = 0
    if len(data.data):
        id = data.data[0]
        w = data.data[1]
        h = data.data[2]
        x = data.data[9]+w/2
        y = data.data[10]+h/2
        print("(id, x, y):" , id, x, y )

        if x<260:
            print("left")
            twist.linear.x = 0.05
            twist.angular.z = 0.3

        elif x>360:
            print("right")
            twist.linear.x = 0.05
            twist.angular.z = -0.3
        else:
            print("right")
            twist.linear.x = 0.1
            twist.angular.z = 0
    else:
        print("lost")
        twist.linear.x = 0
        twist.angular.z = 0
    cmd_pub.publish( twist )

def main():
    global cmd_pub
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("objects", Float32MultiArray, callback)
    cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.spin()
        
if __name__ == '__main__':
    main()