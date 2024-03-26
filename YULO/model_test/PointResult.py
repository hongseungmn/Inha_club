import cv2
import matplotlib.pyplot as plt
import numpy as np


class Point: # 각 객체별 점을 저장할 클래스
  def __init__(self, arr, img):
    #각 좌표에 맞게 키포인트를 초기화한다
    self.point_all = arr # 전체 포인트 배열을 담음
    self.img = img # 도형을 그리기 위해 이미지 변수 초기화
    self.group = {
      'A':set(range(0, 7)),
      'B':set(range(11, 13)),
      'C':set(range(13, 15)),
      'D':set(range(15, 17))
    } # 포인트 그룹을 담을 딕셔너리
    
    #각 배열에 들어있는 원소에 맞게 키 포인트를 표시해주는 함수
    self.definePoints()
    self.defineGroup()
    self.drawGroupLineNText()
    
  
  def definePoints(self):
    for index, point in enumerate(self.point_all):
      if point[0] == 0 and point[1] == 0: # point를 잘못 잡은 경우(절점의 경우)
        for group_name, group_set in self.group.items(): # 반복을 돌면서 각 포인트 그룹에 존재하는 index를 제거해준다
          if index in group_set:
            group_set.remove(index)
            break
        continue
    
  
  #[A] 0 ~ 6 -> 메인 포인트 :(0, 5, 6) , 서브 포인트 :(1, 2, 3, 4)
  #[B] 11, 12 -> 메인 포인트 :(11, 12)
  #[C] 13, 14 -> 메인 포인트 :(13, 14)
  #[D] 15, 16 -> 메인 포인트 :(15, 16)
  def defineGroup(self): # 그룹 포인트들을 그리는 메소드
    self.group_points = np.zeros((len(self.group), 2)) # group_point를 넣을 넘파이 배열 생성
    for idx, (group_name, group_set) in enumerate(self.group.items()): # 저장한 그룹을 순회
      # if group_name == 'A' and all(x not in group_set for x in [0, 5, 6]): # 그룹 A 메인 포인트에서 절점이 발생한 경우
      #   # 다른 서브포인트,메인포인트들의 평균값을 통해 그룹 포인트를 구한다
      #   group_point = np.empty((4,2))
      #   for index in group_set: #group_A의 모든 포인트들을 넘파이 배열로
      #     point = self.point_all[index]
      #     group_points = np.append(group_points,point, axis=0)
      
      #나머지 그룹의 경우 평균값을 구하면 된다 -> 서브포인트가 없으므로 (if)만약 절점이 발생한 경우 좌표값 1개를 이용해 그룹 포인트를 지정?
      group_point = np.empty((0, 2))  # 비어 있는 (0행, 2열) 크기의 2차원 배열 생성
      for index in group_set:
        point = self.point_all[index]
        # x, y 좌표값을 가지는 1차원 배열을 (1, 2) 크기의 2차원 배열로 변경하여 추가
        point_resized = np.reshape(point, (1, 2))
        group_point = np.append(group_point, point_resized, axis=0)
      
      self.group_points[idx] = np.mean(group_point, axis=0) #평균 계산
    
    
    
  def drawGroupLineNText(self):
    for index,(group_point_x, group_point_y) in enumerate(self.group_points): # 그룹 포인트 출력
      self.img = cv2.circle(self.img, (int(group_point_x),int(group_point_y)), 3, (0,255,255), 2)
      self.img = cv2.putText(self.img, str(index) ,(int(group_point_x),int(group_point_y)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)
    
    point_a = self.group_points[0]
    point_b = self.group_points[1]
    point_c = self.group_points[2]
    point_d = self.group_points[3]
    
    self.img = cv2.line(self.img, (int(point_a[0]),int(point_a[1])), (int(point_b[0]),int(point_b[1])), (255,255,255), 1)
    self.img = cv2.line(self.img, (int(point_b[0]),int(point_b[1])), (int(point_c[0]),int(point_c[1])), (255,255,255), 1)
    self.img = cv2.line(self.img, (int(point_c[0]),int(point_c[1])), (int(point_d[0]),int(point_d[1])), (255,255,255), 1)
    
      
      
      
  def drawPoints(self): # 포인트들을 그리는 메소드
    for index, point in enumerate(self.point_all):
      # point가 0이 아닌경우 그대로 그려준다
      self.img = cv2.circle(self.img, (int(point[0]),int(point[1])), 3, (0,255,255), 2)
      self.img = cv2.putText(self.img, str(index) ,(int(point[0]),int(point[1])), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)

  def defineNdrawPoints(self):
    for index, point in enumerate(self.point_all):
      if point[0] == 0 and point[1] == 0: # point를 잘못 잡은 경우(절점의 경우)
        for group_name, group_set in self.group.items(): # 반복을 돌면서 각 포인트 그룹에 존재하는 index를 제거해준다
          if index in group_set:
            group_set.remove(index)
            break
        continue
      # point가 0이 아닌경우 그대로 그려준다
      self.img = cv2.circle(self.img, (int(point[0]),int(point[1])), 3, (0,255,255), 2)
      self.img = cv2.putText(self.img, str(index) ,(int(point[0]),int(point[1])), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)

  def drawImg(self): # 그려진 포인트 이미지를 출력하는 메소드
    return self.img