import cv2
import os
from time import localtime, strftime

def get_image(path:str): 
  print(cv2.__version__)
  print(" ======= 로드할 비디오 경로 : ", path)
  
  # 경로 지정
  if path:
    filepath = path
  else:
    filepath = './output.mp4'

  # 비디오를 경로에서 읽어옴
  video = cv2.VideoCapture(filepath)

  if not video.isOpened():
    print("파일 에러 :", filepath)
    exit(0)

  # 비디오 속성
  length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = video.get(cv2.CAP_PROP_FPS)
  
  print("length :", length)
  print("width :", width)
  print("height :", height)
  print("fps :", fps, "\n")

  currunt_time = localtime()
  timestamp = strftime('%Y_%m_%d_%H', currunt_time)
  try:
    if not os.path.exists(f"images/{timestamp}"):
      os.makedirs(f"images/{timestamp}") # 저장할 경로 지정
  except OSError:
    print("해당 폴더가 이미 존재합니다 : " + timestamp)
  
  count = 0
  
  while(video.isOpened()):
    ret, img = video.read()
    if(int(video.get(1)) % int(fps) == 0): # 1초당 1프레임씩 이미지를 저장
      tm = localtime()
      capturedtime = strftime('%Y%m%d_%H%M%S_', tm)
      cv2.imwrite(f'images/{timestamp}/{capturedtime}{str(int(video.get(1)))}.jpg', img) # 현재 시간으로 파일명을 지정하고 저장
      data = {"image": img, "filename": f"{capturedtime}{str(int(video.get(1)))}"}
      print("Saved frame number:", str(int(video.get(1))))
      count += 1
      yield data
    if(ret == False):
      break

  video.release()
  cv2.destroyAllWindows()

def main():
  for data in get_image('output.mp4'):
    pass

if __name__ == '__main__':
  main()