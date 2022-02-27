#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import rospy
import tf


rospy.init_node('kobuki_tf')
br = tf.TransformBroadcaster()
r = rospy.Rate(100)

while not rospy.is_shutdown():
    br.sendTransform((0.0, 0.0, 0.01), (0, 0, 0, 1), rospy.Time.now(), 
        "base_link", "base_footprint")

    br.sendTransform((0.14, 0.0, 0.24), (0, 0, 0, 1), rospy.Time.now(), 
        "base_scan", "base_link")

    r.sleep()

