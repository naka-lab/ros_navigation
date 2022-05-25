#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from copy import deepcopy
import math
import os
import yaml
import sys
from tkinter import filedialog, messagebox
import codecs

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
original_img = cv2.imread(image_path)

undo_imgs = []

clicked_pos = None
release_pos = None

# 表示する画像の範囲
offset_x = 0
offset_y = 0
window_width = 640
window_height = 480
scale = 4
scroll = 20

img = cv2.resize( original_img, dsize=None, fx=scale, fy=scale )

if img.shape[0]>window_height:
    offset_y = int(img.shape[0]/2-window_height/2)
else:
    window_height = img.shape[0]

if img.shape[1]>window_width:
    offset_x = int(img.shape[1]/2-window_width/2)
else:
    window_widthe = img.shape[1]


def clip_img():
    img = cv2.resize( original_img, dsize=None, fx=scale, fy=scale )
    cliped_img = deepcopy(img[offset_y:offset_y+window_height, offset_x:offset_x+window_width])
    cv2.putText(cliped_img, text='q: quit', org=(10, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    cv2.putText(cliped_img, text='i, j, k, m: scroll', org=(10, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    cv2.putText(cliped_img, text='z: undo', org=(10, 65), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    cv2.putText(cliped_img, text='s: save', org=(10, 90), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,  color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
    return cliped_img

def mouse_event(event, x, y, flags, param):
    global clicked_pos, release_pos

    # 左クリックイベント
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_pos = (x, y)
    elif event==cv2.EVENT_LBUTTONUP:
        release_pos = (x, y)

        color = cv2.getTrackbarPos("Color", "map")
        size = cv2.getTrackbarPos("Size", "map")

        p1 = ( (clicked_pos[0]+offset_x)/scale, (clicked_pos[1]+offset_y)/scale )
        p2 = ( (release_pos[0]+offset_x)/scale, (release_pos[1]+offset_y)/scale )

        undo_imgs.append( deepcopy(original_img) )
        if len(undo_imgs)>5:
            undo_imgs.pop(0)

        cv2.line( original_img, p1, p2, (color,color,color), size )
        cv2.imshow( "map", clip_img() )

        clicked_pos = None
        release_pos = None
    
    if clicked_pos!=None:
        #img_view = deepcopy(img)
        img_view = clip_img()
        size = cv2.getTrackbarPos("Size", "map")
        cv2.line( img_view, clicked_pos, (x,y), (0,0,255) , size*scale )
        cv2.imshow( "map", img_view )


def save():
    name_yaml = filedialog.asksaveasfilename(filetypes=[("yaml", "*.yaml")], initialdir="~/")
    if len(name_yaml)==0:
        return 

    name_pgm = name_yaml[:-4]+"pgm"
    print(name_yaml, name_pgm)

    if os.path.exists( name_pgm ) or os.path.exists( name_yaml ):
        ret = messagebox.askquestion('上書き保存', 'ファイルはすでに存在します．上書きしてもいいですか？', icon='warning')
        if ret=="no":
            return

    new_yaml = deepcopy( map_yaml )
    new_yaml["image"]=name_pgm
    cv2.imwrite( name_pgm, original_img[:,:,0] )

    with codecs.open( name_yaml, 'w', 'utf-8') as f:
        yaml.dump(new_yaml, f, encoding='utf-8', allow_unicode=True)


cv2.namedWindow("map")
cv2.setMouseCallback("map", mouse_event)
cv2.createTrackbar('Color','map',0,255, lambda x: None )
cv2.createTrackbar('Size','map',2,20,lambda x: None )
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

    # 編集機能
    if key==122: # z
        if len(undo_imgs)>0:
            original_img = deepcopy( undo_imgs[-1] )
            undo_imgs.pop(-1)
        else:
            print("これ以上は戻せません")
    elif key==115: # s
        save()


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
