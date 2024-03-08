import cv2
import matplotlib.pyplot as plt
import numpy as np

class Point: # 각 객체별 점을 저장할 클래스
  def __init__(self, arr, img):
    #각 좌표에 맞게 키포인트를 초기화한다
    self.point_all = arr # 전체 배열을 담음
    self.img = img # 도형을 그리기 위해 이미지 변수 초기화
    # self.point_0 = arr[0] # 코
    # self.point_1 = arr[1] # 왼쪽 눈
    # self.point_2 = arr[2] # 오른쪽 눈
    # self.point_3 = arr[3] # 왼쪽 귀
    # self.point_4 = arr[4] # 오른쪽 귀
    # self.point_5 = arr[5] # 왼쪽 어깨
    # self.point_6 = arr[6] # 오른쪽 어깨
    # self.point_7 = arr[7] # 왼쪽 팔꿈치
    # self.point_8 = arr[8] # 오른쪽 팔꿈치
    # self.point_9 = arr[9] # 왼쪽 손목
    # self.point_10 = arr[10] # 오른쪽 손목
    # self.point_11 = arr[11] # 왼쪽 엉덩이
    # self.point_12 = arr[12] # 오른쪽 엉덩이
    # self.point_13 = arr[13] # 왼쪽 무릎
    # self.point_14 = arr[14] # 오른쪽 무릎
    # self.point_15 = arr[15] # 왼쪽 발목
    # self.point_16 = arr[16] # 오른쪽 발목
    
    #각 배열에 들어있는 원소에 맞게 키 포인트를 표시해주는 함수
    self.drawPoints()
    

  def drawImg(self): # 그려진 포인트 이미지를 출력하는 메소드
    #cv2.imshow('Frame', self.img)
    #plt.show()
    return self.img

  def drawPoints(self): # 포인트들을 그리는 메소드
    for index, point in enumerate(self.point_all):
      # print(f"추가된 포인트 : {index} -> {point}")
      if index < 17:
        self.img = cv2.circle(self.img, (int(point[0]),int(point[1])), 3, (0,255,255), 2)
        self.img = cv2.putText(self.img, str(index) ,(int(point[0]),int(point[1])), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)
      else:
        self.img = cv2.circle(self.img, (int(point[0]),int(point[1])), 3, (255,0,0), 2)
        self.img = cv2.putText(self.img, str(index) ,(int(point[0]),int(point[1])), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)

  def drawNewPoints_17(self): #17번 포인트를 새로 구하는 메소드
    x1, y1 = self.point_5
    x2, y2 = self.point_6
    average_x = (x1 + x2) / 2
    average_y = (y1 + y2) / 2
    self.point_17 = [average_x, average_y]
    self.point_all = np.append(self.point_all, [self.point_17], axis=0)

  def drawNewPoints_18(self): #18번 포인트를 새로 구하는 메소드
    x1, y1 = self.point_11
    x2, y2 = self.point_12
    average_x = (x1 + x2) / 2
    average_y = (y1 + y2) / 2
    self.point_18 = [average_x, average_y]
    self.point_all = np.append(self.point_all, [self.point_18], axis=0)

  def drawNewPoints_19(self): #19번 포인트를 새로 구하는 메소드
    x1, y1 = self.point_15
    x2, y2 = self.point_16
    average_x = (x1 + x2) / 2
    average_y = (y1 + y2) / 2
    self.point_19 = [average_x, average_y]
    self.point_all = np.append(self.point_all, [self.point_19], axis=0)

  def drawNewPoints_20(self): #20번 포인트를 새로 구하는 메소드
    x1, y1 = self.point_13
    x2, y2 = self.point_14
    average_x = (x1 + x2) / 2
    average_y = (y1 + y2) / 2
    self.point_20 = [average_x, average_y]
    self.point_all = np.append(self.point_all, [self.point_20], axis=0)

  def drawConnectPoint(self): #17, 18, 19, 20 포인트를 연결하는 메소드
    self.img = cv2.line(self.img, (int(self.point_17[0]),int(self.point_17[1])), (int(self.point_18[0]),int(self.point_18[1])), (255,255,255), 4)
    self.img = cv2.line(self.img, (int(self.point_18[0]),int(self.point_18[1])), (int(self.point_19[0]),int(self.point_19[1])), (255,255,255), 4)