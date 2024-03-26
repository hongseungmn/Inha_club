from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np
from Point import Point
#from PointResult import Point


cap = cv2.VideoCapture('./data/people.mp4') # 웹캠 사용하기 코드
model = YOLO('yolov8n-pose.pt')  # 모델 불러오기 코드

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
    re_frame = cv2.resize(frame, (round(f_width*4), round(f_height*4)), interpolation=cv2.INTER_CUBIC)
    # Predict with the model
    results = model.predict(re_frame,conf=0.1)  # predict on an image
    #Extract keypoint
    result_keypoint_group = results[0].keypoints.xy.cpu().numpy()
    result_bbox = results[0].boxes.xywh.cpu().numpy()
    point_list = list()
    #print('result_keypoint_group : ',result_keypoint_group)
    #result_keypoint_group 개체별 point 좌표 들어있음
    print('검출된 사람 수 : ',len(result_keypoint_group))
    for arr in result_keypoint_group:
      #각 개체별 검출된 키포인트 좌표를 리스트에 담는다
      point = Point(arr, re_frame, result_bbox)
      point_list.append(point)
      re_frame = point.drawImg()

    
    cv2.imshow('_Video', re_frame)
    plt.show()
    key = cv2.waitKey(30)
    if key == ord('q'):
      break;

#메모리 해제 (자원 반납 코드)
cap.release()
cv2.destroyAllWindows()






