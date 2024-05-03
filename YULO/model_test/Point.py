import cv2
import matplotlib.pyplot as plt
import numpy as np

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

class Point: # 각 객체별 점을 저장할 클래스
  def __init__(self, point_arr, img, bbox):
    #각 좌표에 맞게 키포인트를 초기화한다
    self.point_all = point_arr # 전체 포인트 배열을 담음
    self.img = img # 도형을 그리기 위해 이미지 변수 초기화
    self.bbox = bbox # 검출 객체 bbox
    self.group = {
      'A':set(range(0, 7)),
      'B':set(range(11, 13)),
      'C':set(range(13, 15)),
      'D':set(range(15, 17))
    } # 포인트 그룹을 담을 딕셔너리
    
    #각 배열에 들어있는 원소에 맞게 키 포인트를 표시해주는 함수
    #self.defineNdrawPoints()
    self.definePoints()
    self.drawGroup()
    #self.calcAngle()
    self.calcSlope()
    #self.drawPoints()
    

  def drawImg(self): # 그려진 포인트 이미지를 출력하는 메소드
    #cv2.imshow('Frame', self.img)
    #plt.show()
    # 딕셔너리 출력하는 로직
    # for key, value in self.group.items():
    #   print(f"Key: {key}")
    #   print("Values:")
    #   for item in value:
    #       print(item)
    
    return self.img
  
  #[A] 0 ~ 6 -> 메인 포인트 :(0, 5, 6) , 서브 포인트 :(1, 2, 3, 4)
  #[B] 11, 12 -> 메인 포인트 :(11, 12)
  #[C] 13, 14 -> 메인 포인트 :(13, 14)
  #[D] 15, 16 -> 메인 포인트 :(15, 16)
  def drawGroup(self): # 그룹 포인트들을 그리는 메소드
    self.group_points = np.zeros((len(self.group), 2)) # group_point를 넣을 넘파이 배열 생성
    for idx, (group_name, group_set) in enumerate(self.group.items()): # 저장한 그룹을 순회
      if group_name == 'A' and all(x not in group_set for x in [0, 5, 6]): # 그룹 A 메인 포인트에서 절점이 발생한 경우
        #print('group_set : ',self.group.items())
        # 다른 서브포인트,메인포인트들의 평균값을 통해 그룹 포인트를 구한다
        group_point = np.empty((4,2))
        for index in group_set: #group_A의 모든 포인트들을 넘파이 배열로
          #print('Point : ', self.point_all[index])
          point = self.point_all[index]
          group_points = np.append(group_points,point, axis=0)
          #print('groupA : ',group_point)
      
      #나머지 그룹의 경우 평균값을 구하면 된다 -> 서브포인트가 없으므로 (if)만약 절점이 발생한 경우 좌표값 1개를 이용해 그룹 포인트를 지정?
      group_point = np.empty((0, 2))  # 비어 있는 (0행, 2열) 크기의 2차원 배열 생성
      if len(self.point_all) == 0:
        continue
      for index in group_set:
        print('Point : ', self.point_all[index])
        point = self.point_all[index]
        # x, y 좌표값을 가지는 1차원 배열을 (1, 2) 크기의 2차원 배열로 변경하여 추가
        point_resized = np.reshape(point, (1, 2))
        group_point = np.append(group_point, point_resized, axis=0)
      
      #print(f'group_{group_name} : \n{group_point}')
      self.group_points[idx] = np.mean(group_point, axis=0) #평균 계산
    #print('최종 group_point\n',self.group_points)
    # 이전 점의 좌표 초기화
    prev_point = None
    for index,(group_point_x, group_point_y) in enumerate(self.group_points): # 그룹 포인트 출력
      print(f'최종 group_point: (x,y)-> {group_point_x},{group_point_y}')
      self.img = cv2.circle(self.img, (int(group_point_x),int(group_point_y)), 3, (0,255,255), 2)
      self.img = cv2.putText(self.img, str(index) ,(int(group_point_x),int(group_point_y)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),2)
      # 이전 점이 있을 경우에만 선 그리기
      if prev_point is not None:
        # 이전 점과 현재 점을 연결하는 선 그리기
        self.img = cv2.line(self.img, (int(prev_point[0]), int(prev_point[1])), (int(group_point_x), int(group_point_y)), (255, 0, 0), 2)
        # 현재 점과 이전 점을 통해 각도를 계산한다
      
      # 현재 점을 이전 점으로 설정
      prev_point = (group_point_x, group_point_y)
    
  def definePoints(self):
    for index, point in enumerate(self.point_all):
      if point[0] == 0 and point[1] == 0: # point를 잘못 잡은 경우(절점의 경우)
        #self.img = cv2.putText(self.img, "Point Error! " ,(int(self.bbox[0][0]),int(self.bbox[0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0),2)
        for group_name, group_set in self.group.items(): # 반복을 돌면서 각 포인트 그룹에 존재하는 index를 제거해준다
          if index in group_set:
            group_set.remove(index)
            break
        continue
      #print('definePoint : ', point)
    keys_to_delete = []  # 삭제할 키를 저장할 임시 리스트 생성
    for group_name, group_set in self.group.items():
        if len(group_set) == 0:
            keys_to_delete.append(group_name)  # 삭제할 키를 임시 리스트에 추가
    # 임시 리스트에 추가된 키들을 딕셔너리에서 삭제
    for key in keys_to_delete:
        del self.group[key]
  
  def calcAngle(self):
    vector_list = []
    for index,(group_point_x, group_point_y) in enumerate(self.group_points): # 그룹 포인트 출력
      if index + 1 < len(self.group_points):
        vector_list = []
        for index, (group_point_x, group_point_y) in enumerate(self.group_points):
          if index + 1 < len(self.group_points):
            next_group_point_x, next_group_point_y = self.group_points[index + 1]
            # 현재 점과 다음 점을 벡터로 표현
            vector = np.array([next_group_point_x - group_point_x, next_group_point_y - group_point_y])
            vector_list.append(vector)
    # 벡터 간의 각도 계산
    angle_list = []
    for i in range(len(vector_list) - 1):
      vector1 = vector_list[i]
      vector2 = vector_list[i + 1]
      # 내적 계산
      dot_product = np.dot(vector1, vector2)
      # 벡터의 크기 계산
      norm_vector1 = np.linalg.norm(vector1)
      norm_vector2 = np.linalg.norm(vector2)
      # 각도 계산 (라디안 단위)
      angle_rad = np.arccos(dot_product / (norm_vector1 * norm_vector2))
      # 라디안을 도 단위로 변환
      angle_deg = np.degrees(angle_rad)
      angle_list.append(angle_deg)
    
    
    
    
  def calcSlope(self):
    slope_list = []
    for index, (group_point_x, group_point_y) in enumerate(self.group_points):
      if index + 1 < len(self.group_points):
        next_group_point_x, next_group_point_y = self.group_points[index + 1]
        # 두 점을 지나는 직선의 기울기 계산
        slope = (next_group_point_y - group_point_y) / (next_group_point_x - group_point_x)
        # 기울기가 음수인 경우 양수로 변환
        if slope < 0:
          slope = abs(slope)
        slope_list.append(slope)
    # 기울기들의 평균값 계산
    print('slope_list : ',slope_list)
    if len(slope_list) != 0:
      average_slope = sum(slope_list) / len(slope_list)
      #print('Average Slope : ',average_slope)
      if average_slope < 0.5:
        print('낙상 발생!!!')
        self.img = cv2.putText(self.img, "Fall Down!!! " ,(int(self.bbox[0][0]),int(self.bbox[0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),3)
        
          
          
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