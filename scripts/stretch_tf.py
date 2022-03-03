#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import rospy
import tf
import math

rospy.init_node('kobuki_tf')
br = tf.TransformBroadcaster()
r = rospy.Rate(100)

rot = tf.transformations.quaternion_from_euler(0, 0, -math.pi/2 )

while not rospy.is_shutdown():
    br.sendTransform((-0.1, 0.0, 0.0), rot, rospy.Time.now(), 
        "hokuyo_laer", "base_link")

    r.sleep()

