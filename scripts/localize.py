#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import rospy
from std_srvs.srv import Empty
import time
import sys

rospy.init_node("update_position" )
rospy.wait_for_service("/request_nomotion_update")
update_position = rospy.ServiceProxy("/request_nomotion_update", Empty)

N = int(sys.argv[1])

for i in range(N):
    print( "Localize %d/%d" % (i+1,N) )
    update_position()
    time.sleep(0.1)
