import cv2
import sys

#웹캠 로드
cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
  print("웹 캠을 실행할 수 없습니다")

#저장할 파일 속성 정의
videoFileName = 'output.mp4'

fps = cap.get(cv2.CAP_PROP_FPS)
f_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
f_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
f_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'avc1')
delay = round(1000/fps) # 프레임 설정

#비디오 저장
out = cv2.VideoWriter(videoFileName, fourcc=fourcc, fps= fps, frameSize=(f_width, f_height))
if not (out.isOpened()):
  print("파일이 열리지 않습니다")
  cap.release()
  sys.exit()
  
#프레임을 로드하고 저장
while(True):
  ret, frame = cap.read() 
  
  if ret:
    out.write(frame)
    
    cv2.imshow('Video', frame)
    
    key = cv2.waitKey(30)
    if key == ord('q'):
      break;  
  
  else:
    print('이미지를 읽어드릴 수 없음')
    break

# 자원 반납
cap.release()
out.release()
cv2.destroyAllWindows()