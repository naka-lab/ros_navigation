#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from copy import deepcopy
import math
import os
import yaml
import sys

yaml_path = sys.argv[1]
with open( yaml_path ) as file:
    try:
        map_yaml = yaml.safe_load(file)
        print(map_yaml)
        print("--------------")
    except:
        print("ファイルの読み込みに失敗")

dirname = os.path.dirname( os.path.abspath( yaml_path ) )
image_path = os.path.join( dirname, map_yaml["image"] )
img = cv2.imread(image_path)

clicked_pos = None
def mouse_event(event, x, y, flags, param):
    global clicked_pos
    # 左クリックイベント
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_pos = (x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        map_x = clicked_pos[0]*map_yaml["resolution"]+map_yaml["origin"][0]
        map_y = (img.shape[0]-clicked_pos[1])*map_yaml["resolution"]+map_yaml["origin"][1]
        theta = -math.atan2( y-clicked_pos[1], x-clicked_pos[0] )

        print('"指定位置" : (%lf, %lf, %lf),'%(map_x, map_y, theta))

        clicked_pos = None
        img_view = None
    
    if clicked_pos!=None:
        img_view = deepcopy(img)
        cv2.circle( img_view, clicked_pos, 5, (0,0,255), 2 )
        theta = math.atan2( y-clicked_pos[1], x-clicked_pos[0] )
        end_pos = ( int(clicked_pos[0]+8*math.cos(theta)), int(clicked_pos[1]+8*math.sin(theta)) )
        cv2.line( img_view, clicked_pos, end_pos, (0,0,255) ,2 )
        cv2.imshow( "map", img_view )

cv2.namedWindow("map")
cv2.setMouseCallback("map", mouse_event)
cv2.imshow( "map", img )


while 1:
    # ctrl+cで終了できるよう一定間隔でwaitkeyを抜ける
    cv2.waitKey(500)
cv2.destroyAllWindows()
