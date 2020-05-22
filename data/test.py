import os
import sys
import math
import time
import cv2
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
# %matplotlib inline 
from matplotlib.patches import Rectangle

# import pytorch
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

path = './Project04_ObjectDetection/data/'

# 이미지
# img = cv2.imread(path + 'jennie.jpg')
# img = cv2.imread(path + 'jennie_eye.jpg') # 눈색깔이 다름
# img = cv2.imread(path + 'jennie_makeup.jpg')# 진한화장
img        = cv2.imread(path + 'hong.jpeg') # 옆모습
# 영상
# video = path+'jennie.mp4'
video      = path+'jennie_grayscale.mp4' # 흑백
cap        = cv2.VideoCapture(video)
ret, frame = cap.read() 
# frame      = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # 캡쳐.
frame      = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # 사진. yolo안돌아갈수있음
# plt.imshow(frame)
# print( type(frame) )



# warm up
_ = get_blazeface_face(frame)
_ = get_mtcnn_face(frame)
_ = get_mobilenet_face(frame)
# _ = get_yolo_face(frame)

# speed comparison
blaze_time,     blaze_bboxes     = get_blazeface_face(frame)
mtcnn_time,     mtcnn_bboxes     = get_mtcnn_face(frame)
mobilenet_time, mobilenet_bboxes = get_mobilenet_face(frame)
# yolo_time,      yolo_bboxes      = get_yolo_face(frame)

print( "MTCNN Detection Time:"     + str(mtcnn_time) )
print( "Yolo Detection Time:"      + str(yolo_time) )
print( "Mobilenet Detection Time:" + str(mobilenet_time) )
print( "BlazeFace Detection Time:" + str(blaze_time) )

# Ability to Detect Face
if blaze_bboxes==[]:
    print('⚠️BlazeFace is unable to detect face in this frame.')
if mtcnn_bboxes==[]:
    print('⚠️MTCNN is unable to detect face in this frame.')
if mobilenet_bboxes==[]:
    print('⚠️mobilenet is unable to detect face in this frame.')
if yolo_bboxes==[]:
    print('⚠️mobilenet is unable to detect face in this frame.')

# Accuracy Comparison
# Annotated Images
annotated=annotate_image(frame,mobilenet_bboxes,(255,0,0)) # Red: Mobilenet
annotated=annotate_image(annotated,mtcnn_bboxes,(0,255,0))# Green: MTCNN
annotated=annotate_image(annotated,blaze_bboxes,(0,0,255))# Blue: BlazeFace
annotated=annotate_image(annotated,yolo_bboxes,(255,0,255))# Purple: YOLO
plt.imshow(annotated)

