import torch
from torchvision import models
import os
import sys
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, '../model')
model = torch.hub.load('./yolov5', 'custom', path='../model/best.pt', source='local')
cap = cv2.VideoCapture(0) # 웹캠 사용하기 코드

if cap.isOpened():
  fps = cap.get(cv2.CAP_PROP_FPS)
  f_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
  f_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  f_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  
  print('Frames per second : ', fps, 'FPS')
  print('Frame count : ', f_count)
  print('Frame width : ', f_width)
  print('Frame height : ',f_height)
  
  while cap.isOpened():
    ret, frame = cap.read()
    re_frame = cv2.resize(frame, (round(f_width / 4), round(f_height / 4)), interpolation=cv2.INTER_CUBIC)
    temp = model(re_frame)
    if ret:
        temp_frame = np.squeeze(temp.render())
        cv2.imshow('_Video', temp_frame)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
    else:
        print("Failed to capture frame.")

#메모리 해제 (자원 반납 코드)
cap.release()
cv2.destroyAllWindows()






