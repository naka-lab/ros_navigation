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

# 表示する画像の範囲
offset_x = 0
offset_y = 0
window_width = 640
window_height = 480
scale = 2
scroll = 20

img = cv2.resize( img, dsize=None, fx=scale, fy=scale )

if img.shape[0]>window_height:
    offset_y = int(img.shape[0]/2-window_height/2)
else:
    window_height = img.shape[0]

if img.shape[1]>window_width:
    offset_x = int(img.shape[1]/2-window_width/2)
else:
    window_widthe = img.shape[1]


def clip_img():
    cliped_img = deepcopy(img[offset_y:offset_y+window_height, offset_x:offset_x+window_width])
    cv2.putText(cliped_img, text='q: quit', org=(10, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    cv2.putText(cliped_img, text='i, j, k, m scroll', org=(10, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    return cliped_img

def mouse_event(event, x, y, flags, param):
    global clicked_pos
    # 左クリックイベント
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_pos = (x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        map_x = (clicked_pos[0]+offset_x)/scale*map_yaml["resolution"]+map_yaml["origin"][0]
        map_y = (img.shape[0]-clicked_pos[1]-offset_y)/scale*map_yaml["resolution"]+map_yaml["origin"][1]
        theta = -math.atan2( y-clicked_pos[1], x-clicked_pos[0] )

        print('"指定位置" : (%lf, %lf, %lf),'%(map_x, map_y, theta))

        clicked_pos = None
        img_view = None
    
    if clicked_pos!=None:
        #img_view = deepcopy(img)
        img_view = clip_img()
        cv2.circle( img_view, clicked_pos, 5, (0,0,255), 2 )
        theta = math.atan2( y-clicked_pos[1], x-clicked_pos[0] )
        end_pos = ( int(clicked_pos[0]+8*math.cos(theta)), int(clicked_pos[1]+8*math.sin(theta)) )
        cv2.line( img_view, clicked_pos, end_pos, (0,0,255) ,2 )
        cv2.imshow( "map", img_view )

cv2.namedWindow("map")
cv2.setMouseCallback("map", mouse_event)
cv2.imshow( "map", clip_img() )


while 1:
    key = cv2.waitKey(500)

    # フリーズ対策
    if key==-1:
        continue

    # 終了
    if key==113: # q
        break

    # マップ移動
    if key==105: # i
        offset_y -= scroll
    elif key==109: # m
        offset_y += scroll
    elif key==107: # k
        offset_x += scroll
    elif key==106: # j
        offset_x -= scroll

    # 移動量修正
    if offset_x<0:
        offset_x = 0
    if offset_y<0:
        offset_y = 0

    if offset_y+window_height>img.shape[0]:
        offset_y = img.shape[0] - window_height

    if offset_x+window_width>img.shape[1]:
        offset_x = img.shape[1] - window_width

    cv2.imshow( "map",  clip_img() )

cv2.destroyAllWindows()
