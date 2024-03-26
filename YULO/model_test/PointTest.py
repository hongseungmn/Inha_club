from Point import Point
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy
#from PointResult import Point

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model  # load a custom model

# Predict with the model
results = model.predict('./data/small_person.png')  # predict on an image
result_keypoint_group = results[0].keypoints.xy.cpu().numpy()
result_bbox = results[0].boxes.xywh.cpu().numpy()
print("result bbox : ", result_bbox)
point_list = list()
print('검출된 사람 수 : ',len(result_keypoint_group))
re_frame = cv2.imread('./data/small_person.png')
for arr in result_keypoint_group:
  #각 개체별 검출된 키포인트 좌표를 리스트에 담는다
  point = Point(arr, re_frame,result_bbox)
  point_list.append(point)
  re_frame = point.drawImg()

plt.figure(figsize=(12,12))
plt.imshow(re_frame)
plt.show()
