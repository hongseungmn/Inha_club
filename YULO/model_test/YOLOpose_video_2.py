#라이브러리 import 
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
from ultralytics import YOLO


from fastapi.middleware.cors import CORSMiddleware

import threading, time
from functools import partial
from datetime import datetime

# FastAPI 앱 인스턴스 생성
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 허용
    allow_methods=["GET", "POST", "OPTIONS"],  # 허용할 메서드 지정
    allow_headers=["*"],  # 허용할 헤더 지정
)

def get_stream_video(model,count,label):
  global detected_count  # 전역 변수로 카운트 저장
  # camera 정의
  cam = cv2.VideoCapture(0)

  try:
    while True:
      # 카메라 값 불러오기
      success, frame = cam.read()

      if not success:
        break
      else:
        results = model(frame,verbose=False, classes=[0])
        detected_count = sum(len(r.boxes.cls) for r in results)
        ret, buffer = cv2.imencode('.jpg', results[0].plot())
        if ret:
          frame = buffer.tobytes()
          yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame + b'\r\n')
        else:
        # yield로 하나씩 넘겨준다.
          frame = buffer.tobytes()
          yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(frame) + b'\r\n')
  finally:
    cam.release() # 카메라 자원 해제

@app.get("/count")
def get_count():
  data = generate_data()  # 샘플 데이터 생성
  return data

# 샘플 데이터 생성
def generate_data():
  global detected_count
  now = datetime.now()
  formatted_time = now.strftime("%H:%M:%S")
  
  # 데이터 예시: 시간, pv, amt
  data = {
    "dateTime": formatted_time,
    "pv": detected_count,  # PV값 예시
  }

  return [data]


@app.get('/get_url')
def get_url():
  return {
    "url":"http://127.0.0.1:8000/video"
  }
  
  
def video_streaming(count, label):
  model = YOLO('yolov8n.pt')
  model.classes = [label]
  return get_stream_video(model,count, label)
  
@app.get('/video')
def main(count: int, label: str):
    #StringResponse 함수를 return하고,
    #인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(video_streaming(count, label), media_type="multipart/x-mixed-replace; boundary=frame")